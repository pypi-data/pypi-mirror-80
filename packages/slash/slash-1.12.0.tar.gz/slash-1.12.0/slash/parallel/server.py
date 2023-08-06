import copy
import logbook
import time
import threading
from enum import Enum
from six.moves import xmlrpc_server
from ..utils.python import unpickle
from .. import log
from ..ctx import context
from ..runner import _get_test_context
from .. import hooks
from ..conf import config
from .tests_distributer import TestsDistributer

_logger = logbook.Logger(__name__)
log.set_log_color(_logger.name, logbook.NOTICE, 'blue')

NO_MORE_TESTS = "NO_MORE_TESTS"
PROTOCOL_ERROR = "PROTOCOL_ERROR"
WAITING_FOR_CLIENTS = "WAITING_FOR_CLIENTS"

class ServerStates(Enum):
    NOT_INITIALIZED = 1
    WAIT_FOR_CLIENTS = 2
    WAIT_FOR_COLLECTION_VALIDATION = 3
    SERVE_TESTS = 4
    STOP_TESTS_SERVING = 5
    STOP_SERVE = 6

class KeepaliveServer(object):
    def __init__(self):
        super(KeepaliveServer, self).__init__()
        self.clients_last_communication_time = {}
        self.last_request_time = time.time()
        self.state = ServerStates.NOT_INITIALIZED
        self.port = None
        self._lock = threading.Lock()

    def keep_alive(self, client_id):
        with self._lock:
            self.clients_last_communication_time[client_id] = self.last_request_time = time.time()
        _logger.debug("Client_id {} sent keep_alive", client_id)

    def stop_serve(self):
        self.state = ServerStates.STOP_SERVE

    def serve(self):
        server = xmlrpc_server.SimpleXMLRPCServer((config.root.parallel.server_addr, 0), allow_none=True, logRequests=False)
        try:
            self.port = server.server_address[1]
            self.state = ServerStates.WAIT_FOR_CLIENTS
            server.register_instance(self)
            _logger.debug("Starting Keepalive server")
            while self.state != ServerStates.STOP_SERVE:
                server.handle_request()
            _logger.debug("Exiting KeepAlive server loop")
        finally:
            server.server_close()

    def get_workers_last_connection_time(self):
        with self._lock:
            return copy.deepcopy(self.clients_last_communication_time)


class Server(object):
    def __init__(self, tests):
        super(Server, self).__init__()
        self.worker_error_reported = False
        self.interrupted = False
        self.state = ServerStates.NOT_INITIALIZED
        self.port = None
        self.tests = tests
        self.worker_session_ids = []
        self.executing_tests = {}
        self.finished_tests = []
        self.num_collections_validated = 0
        self.start_time = time.time()
        self.worker_to_pid = {}
        self.connected_clients = set()
        self.collection = [[test.__slash__.file_path,
                            test.__slash__.function_name,
                            test.__slash__.variation.dump_variation_dict()]
                           for test in self.tests]
        self._sorted_collection = sorted(self.collection)
        self._tests_distrubuter = TestsDistributer(len(self._sorted_collection))

    def has_connected_clients(self):
        return len(self.connected_clients) > 0

    def get_connected_clients(self):
        return self.connected_clients.copy()

    def has_more_tests(self):
        return len(self.finished_tests) < len(self.tests)

    def report_client_failure(self, client_id):
        self.connected_clients.remove(client_id)
        test_index = self.executing_tests.get(client_id, None)
        if test_index is not None:
            _logger.error("Worker {} interrupted while executing test {}", client_id,
                          self.tests[test_index].__slash__.address, extra={'capture': False})
            with _get_test_context(self.tests[test_index], logging=False) as (result, _):
                result.mark_interrupted()
                self.finished_tests.append(test_index)
        self.state = ServerStates.STOP_TESTS_SERVING
        self._mark_unrun_tests()
        self.worker_error_reported = True

    def get_unstarted_tests(self):
        return self._tests_distrubuter.get_unstarted_tests()

    def _mark_unrun_tests(self):
        unstarted_tests_indexes = self._tests_distrubuter.get_unstarted_tests()
        for test_index in unstarted_tests_indexes:
            with _get_test_context(self.tests[test_index], logging=False):
                pass
            self.finished_tests.append(test_index)
        self._tests_distrubuter.clear_unstarted_tests()

    def _get_worker_session_id(self, client_id):
        return "worker_{}".format(client_id)

    def connect(self, client_id, client_pid):
        _logger.notice("Client_id {} connected", client_id)
        self.connected_clients.add(client_id)
        client_session_id = '{}_{}'.format(context.session.id.split('_')[0], client_id)
        context.session.logging.create_worker_symlink(self._get_worker_session_id(client_id), client_session_id)
        hooks.worker_connected(session_id=client_session_id)  # pylint: disable=no-member
        self.worker_session_ids.append(client_session_id)
        self.worker_to_pid[client_id] = client_pid
        self.executing_tests[client_id] = None
        if len(self.connected_clients) >= config.root.parallel.num_workers:
            _logger.notice("All workers connected to server")
            self.state = ServerStates.WAIT_FOR_COLLECTION_VALIDATION

    def validate_collection(self, client_id, sorted_client_collection):
        if not self._sorted_collection == sorted_client_collection:
            _logger.error("Client_id {} sent wrong collection", client_id, extra={'capture': False})
            return False
        self.num_collections_validated += 1
        _logger.debug("Worker {} validated tests successfully", client_id)
        if self.num_collections_validated >= config.root.parallel.num_workers and self.state == ServerStates.WAIT_FOR_COLLECTION_VALIDATION:
            _logger.notice("All workers collected tests successfully, start serving tests")
            self.state = ServerStates.SERVE_TESTS
        return True

    def disconnect(self, client_id, has_failure=False):
        _logger.notice("Client {} sent disconnect", client_id)
        self.connected_clients.remove(client_id)
        if has_failure:
            self.state = ServerStates.STOP_TESTS_SERVING

    def get_test(self, client_id):
        if not self.executing_tests[client_id] is None:
            _logger.error("Client_id {} requested new test without sending former result", client_id,
                          extra={'capture': False})
            return PROTOCOL_ERROR
        if self.state == ServerStates.STOP_TESTS_SERVING:
            return NO_MORE_TESTS
        elif self.state in [ServerStates.WAIT_FOR_CLIENTS, ServerStates.WAIT_FOR_COLLECTION_VALIDATION]:
            return WAITING_FOR_CLIENTS
        elif self.state == ServerStates.SERVE_TESTS and self._tests_distrubuter.has_unstarted_tests():
            test_index = self._tests_distrubuter.get_next_test_for_client(client_id)
            if test_index is None: #we have omre tests but current worker cannot execute them
                return NO_MORE_TESTS
            test = self.tests[test_index]
            self.executing_tests[client_id] = test_index
            hooks.test_distributed(test_logical_id=test.__slash__.id, worker_session_id=self._get_worker_session_id(client_id)) # pylint: disable=no-member
            _logger.notice("#{}: {}, Client_id: {}", test_index + 1, test.__slash__.address, client_id,
                           extra={'highlight': True, 'filter_bypass': True})
            return (self.collection[test_index], test_index)
        else:
            _logger.debug("No unstarted tests, sending end to client_id {}", client_id)
            self.state = ServerStates.STOP_TESTS_SERVING
            return NO_MORE_TESTS

    def finished_test(self, client_id, result_dict):
        _logger.debug("Client_id {} finished_test", client_id)
        test_index = self.executing_tests.get(client_id, None)
        if test_index is not None:
            self.finished_tests.append(test_index)
            self.executing_tests[client_id] = None
            with _get_test_context(self.tests[test_index], logging=False) as (result, _):
                result.deserialize(result_dict)
                context.session.reporter.report_test_end(self.tests[test_index], result)
                if result.has_fatal_exception() or (not result.is_success(allow_skips=True) and config.root.run.stop_on_error):
                    _logger.debug("Server stops serving tests, run.stop_on_error: {}, result.has_fatal_exception: {}",
                                  config.root.run.stop_on_error, result.has_fatal_exception())
                    self.state = ServerStates.STOP_TESTS_SERVING
                    self._mark_unrun_tests()
        else:
            _logger.error("finished_test request from client_id {} with index {}, but no test is mapped to this worker",
                          client_id, test_index, extra={'capture': False})
            return PROTOCOL_ERROR

    def stop_serve(self):
        self.state = ServerStates.STOP_SERVE

    def session_interrupted(self):
        context.session.results.global_result.mark_interrupted()
        self.interrupted = True
        if self.state != ServerStates.STOP_SERVE:
            self.state = ServerStates.STOP_TESTS_SERVING

    def report_warning(self, client_id, pickled_warning):
        _logger.notice("Client_id {} sent warning", client_id)
        try:
            warning = unpickle(pickled_warning)
            context.session.warnings.add(warning)
        except TypeError:
            _logger.error('Error when deserializing warning, not adding it', extra={'capture': False})

    def report_session_error(self, message):
        self.worker_error_reported = True
        _logger.error(message, extra={'capture': False})

    def should_wait_for_request(self):
        return self.has_connected_clients() or self.has_more_tests()

    def serve(self):
        server = xmlrpc_server.SimpleXMLRPCServer((config.root.parallel.server_addr, config.root.parallel.server_port),\
                                                  allow_none=True, logRequests=False)
        try:
            self.port = server.server_address[1]
            self.state = ServerStates.WAIT_FOR_CLIENTS
            server.register_instance(self)
            _logger.debug("Starting server loop")
            while self.state != ServerStates.STOP_SERVE:
                server.handle_request()
            if not self.interrupted:
                context.session.mark_complete()
            _logger.trace('Session finished. is_success={0} has_skips={1}',
                          context.session.results.is_success(allow_skips=True), bool(context.session.results.get_num_skipped()))
            _logger.debug("Exiting server loop")
        finally:
            server.server_close()
