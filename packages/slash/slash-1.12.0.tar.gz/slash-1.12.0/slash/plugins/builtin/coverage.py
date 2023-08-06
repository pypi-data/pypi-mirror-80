from __future__ import absolute_import

from slash import config as slash_config

from ...utils.conf_utils import Cmdline, Doc
from ...utils import parallel_utils
from ..interface import PluginInterface

_DATA_FILENAME = '.coverage'

class Plugin(PluginInterface):

    """Enables saving coverage information for test runs
    For more information see https://slash.readthedocs.org/en/master/builtin_plugins.html#coverage
    """

    def get_name(self):
        return "coverage"

    def get_default_config(self):
        return {
            'config_filename': False // Cmdline(arg='--cov-config') // Doc('Coverage configuration file'),
            'report_type': 'html' // Cmdline(arg='--cov-report') // Doc('Coverage report format'),
            'report': True,
            'append': False // Cmdline(on='--cov-append') // Doc('Append coverage data to existing file'),
            'sources': [] // Cmdline(append='--cov') // Doc('Modules or packages for which to track coverage'),
        }

    def activate(self):
        try:
            import coverage
        except ImportError: # pragma: no cover
            raise RuntimeError('The coverage plugin requires the coverage package to be installed. Please run `pip install coverage` to install it')

        sources = slash_config.root.plugin_config.coverage.sources or None
        data_file_name = _DATA_FILENAME
        if parallel_utils.is_child_session():
            data_file_name += "." + slash_config.root.parallel.worker_id
        self._cov = coverage.Coverage(
            data_file=data_file_name,
            config_file=slash_config.root.plugin_config.coverage.config_filename,
            source=sources,
        )
        if slash_config.root.plugin_config.coverage.append:
            self._cov.load()
        self._reporters = []
        for report_type_name in slash_config.root.plugin_config.coverage.report_type.split(','):
            if report_type_name == 'html':
                self._reporters.append(self._cov.html_report)
            elif report_type_name == 'xml':
                self._reporters.append(self._cov.xml_report)
            else:
                raise RuntimeError('Unknown report type: {!r}'.format(report_type_name))
        self._cov.start()


    def session_end(self):
        from coverage import CoverageException
        self._cov.stop()
        self._cov.save()
        if slash_config.root.plugin_config.coverage.report:
            for reporter in self._reporters:
                try:
                    if parallel_utils.is_child_session():
                        continue
                    elif parallel_utils.is_parent_session():
                        self._cov.combine()
                    reporter()
                except CoverageException as e:
                    if 'no data' not in str(e).lower():
                        raise
