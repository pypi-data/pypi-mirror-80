#!/usr/bin/env python
#  Copyright 2013-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import sys

from robot.errors import DataError
from rpbot.reader import ReaderOptions, RobotResultsParser
from rpbot.reportportal.variables import Variables
from rpbot.reportportal.reporter import DryRunRP, ReportPortal


class RpBot(object):

    def __init__(self):
        self._options = ReaderOptions()
        Variables.check_variables(self._options)
        if self._options.dry_run:
            reporter = DryRunRP(self._options.verbose_level)
        else:
            reporter = ReportPortal(self._options.verbose_level)
        self._parser = RobotResultsParser(reporter, self._options.verbose_level)

    def run(self):
        try:
            for xml_file in self._options.file_paths:
                self._parser.xml_to_db(xml_file)
        except DataError as message:
            sys.stderr.write('rpbot: error: Invalid XML: %s\n\n' % message)
            exit(1)
        # finally:
        #     self._db.close()


if __name__ == '__main__':
    RpBot().run()
