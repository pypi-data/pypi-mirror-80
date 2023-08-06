import logging
from reportportal_client.helpers import gen_attributes

from .variables import Variables
from .model import Keyword, Test, Suite, LogMessage
from .service import RobotService


class DryRunRP:

    def __init__(self, verbose=False):
        self._logger = logging.getLogger('RP(DRYRUN)')
        if verbose:
            self._logger.setLevel(verbose)

    def __getattr__(self, name):
        def method(*args):
            self._logger.debug("call to " + name)
        return method

class ReportPortal:

    def __init__(self, verbose=False):
        self.items = []
        self._logger = logging.getLogger('RP')
        if verbose:
            self._logger.setLevel(verbose)

    def _gen_attributes_from_robot_tags(self, tags):
        attrs = []
        for tag in tags:
            attrs.append({'value': tag})
        return attrs

    def start_launch(self, launch):
        """Start a new launch at the Report Portal."""
        if not Variables.launch_id:
            launch.doc = Variables.launch_doc
            self._logger.debug("ReportPortal - Start Launch: {0}".format(
                launch.attributes))
            RobotService.start_launch(
                launch_name=Variables.launch_name,
                attributes=gen_attributes(Variables.launch_attributes),
                description=launch.doc)
        else:
            RobotService.rp.launch_id = Variables.launch_id

    def start_suite(self, name, attributes):
        suite = Suite(attributes=attributes)
        if suite.robot_id == "s1":
            RobotService.init_service(Variables.endpoint, Variables.project,
                                    Variables.uuid)
            self.start_launch(suite)
            if not suite.suites:
                attributes['id'] = "s1-s1"
                self.start_suite(name, attributes)
        else:
            self._logger.debug("ReportPortal - Start Suite: {0}".format(attributes))
            parent_id = self.items[-1][0] if self.items else None
            item_id = RobotService.start_suite(
                name=name,
                suite=suite,
                parent_item_id=parent_id)
            self.items.append((item_id, parent_id))

    def end_suite(self, _, attributes):
        suite = Suite(attributes=attributes)
        if suite.robot_id == "s1":
            self._logger.debug(msg="ReportPortal - End Launch: {0}".format(attributes))
            RobotService.finish_launch(launch=suite)
            RobotService.terminate_service()
        else:
            self._logger.debug("ReportPortal - End Suite: {0}".format(attributes))
            RobotService.finish_suite(item_id=self.items.pop()[0], suite=suite)

    def start_test(self, name, attributes):
        test = Test(name=name, attributes=attributes)
        self._logger.debug("ReportPortal - Start Test: {0}".format(attributes))
        parent_item_id = self.items[-1][0]
        self.items.append((
            RobotService.start_test(
                test=test,
                parent_item_id=parent_item_id,
                attributes=gen_attributes(Variables.test_attributes) + self._gen_attributes_from_robot_tags(test.tags),
            ),
            parent_item_id))

    def end_test(self, name, attributes):
        test = Test(name=name, attributes=attributes)
        item_id, _ = self.items.pop()
        self._logger.debug("ReportPortal - End Test: {0}".format(attributes))
        RobotService.finish_test(item_id=item_id, test=test)

    def start_keyword(self, name, attributes):
        parent_type = 'SUITE' if not self.items else 'TEST'
        parent_item_id = self.items[-1][0]
        kwd = Keyword(name=name, parent_type=parent_type, attributes=attributes)
        self._logger.debug("ReportPortal - Start Keyword: {0}".format(attributes))
        self.items.append((
            RobotService.start_keyword(keyword=kwd, parent_item_id=parent_item_id,
                                    has_stats=False),
            parent_item_id))

    def end_keyword(self, name, attributes):
        kwd = Keyword(name=name, attributes=attributes)
        item_id, _ = self.items.pop()
        self._logger.debug("ReportPortal - End Keyword: {0}".format(attributes))
        RobotService.finish_keyword(item_id=item_id, keyword=kwd)

    def log_message(self, message):
        # Check if message comes from our custom logger or not
        if isinstance(message["message"], LogMessage):
            msg = message["message"]
        else:
            msg = LogMessage(message["message"])
            msg.level = message["level"]

        msg.item_id = self.items[-1][0]
        self._logger.debug("ReportPortal - Log Message: {0}".format(message))
        RobotService.log(message=msg)

    def message(self, message):
        self._logger.debug("ReportPortal - Message: {0}".format(message))

    def library_import(self, name, attributes):
        self._logger.debug("ReportPortal - Library Import: {0}".format(attributes))

    def resource_import(self, name, attributes):
        self._logger.debug("ReportPortal - Resource Import: {0}".format(attributes))

    def variables_import(self, name, attributes):
        self._logger.debug("ReportPortal - Variables Import: {0}".format(attributes))

    def output_file(self, path):
        self._logger.debug("ReportPortal - Output File: {0}".format(path))

    def log_file(self, path):
        self._logger.debug("ReportPortal - Log File: {0}".format(path))

    def report_file(self, path):
        self._logger.debug("ReportPortal - Report File: {0}".format(path))

    def xunit_file(self, path):
        self._logger.debug("ReportPortal - XUnit File: {0}".format(path))

    def info_file(self, path):
        self._logger.debug("ReportPortal - info File: {0}".format(path))
