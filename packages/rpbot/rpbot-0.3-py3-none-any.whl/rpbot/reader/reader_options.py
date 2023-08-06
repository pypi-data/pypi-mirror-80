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
from optparse import OptionParser, OptionGroup
from os.path import exists


class ReaderOptions(object):

    def __init__(self):
        self._parser = OptionParser()
        self._add_parser_options()
        self._options, self._files = self._get_validated_options()

    def _add_parser_options(self):
        options = [
            ('-d', '--dry-run', {'action': 'store_true',
                                 'default': False,
                                 'dest': 'dry_run',
                                 'help': 'do everything except store results into reportportal'}),

            ('-v', '--verbose', {
                                 'default': False,
                                 'dest': 'level',
                                 'help': 'be verbose. WARN, INFO, and DEBUG available.'}),
        ]
        for option in options:
            self._parser.add_option(option[0], option[1], **option[2])

        rp_group_options = [
            ('', '--RP_UUID', {'dest': 'rp_uuid', 'default': None, 'help': 'your user uuid'}),
            ('', '--RP_ENDPOINT', {'dest': 'rp_endpoint', 'default': None, 'help': 'your reportportal url'}),
            ('', '--RP_LAUNCH', {'dest': 'rp_launch', 'default': None, 'help': 'launch name'}),
            ('', '--RP_PROJECT', {'dest': 'rp_project', 'default': None, 'help': 'reportportal project name'}),
            ('', '--RP_LAUNCH_UUID', {'dest': 'rp_launch_uuid', 'default': None,
                                      'help': 'ID of existing reportportal launch'}),
            ('', '--RP_LAUNCH_DOC', {'dest': 'rp_launch_doc', 'default': None,
                                     'help': 'Description  for the launch'}),
            ('', '--RP_LAUNCH_ATTRIBUTES', {'dest': 'rp_launch_attributes', 'default': '',
                                            'help': 'Space-separated list of tags/attributes for the launch'}),
            ('', '--RP_TEST_ATTRIBUTES', {'dest': 'rp_test_attributes', 'default': '',
                                          'help': 'Space-separated list of tags/attributes for the tests'}),
            ('', '--RP_LOG_BATCH_SIZE', {'dest': 'rp_log_batch_size', 'default': '20',
                                         'help': 'Default value is "20", affects size of async batch log requests'}),
        ]
        rp_group = OptionGroup(self._parser, 'ReportPortal Options')
        for option in rp_group_options:
            rp_group.add_option(option[0], option[1], **option[2])
        self._parser.add_option_group(rp_group)

    def _get_validated_options(self):
        options, files = self._parser.parse_args()
        self._check_files(files)
        return options, files

    def _check_files(self, files):
        if not files or len(files) < 1:
            self._parser.error('at least one input file is required')
        for file_path in files:
            if not exists(file_path):
                self._parser.error('file "%s" does not exist' % file_path)

    def _exit_with_help(self):
        self._parser.print_help()
        exit(1)

    @property
    def verbose_level(self):
        return self._options.level

    @property
    def file_paths(self):
        return self._files

    @property
    def dry_run(self):
        return self._options.dry_run

    @property
    def rp_uuid(self):
        return self._options.rp_uuid

    @property
    def rp_endpoint(self):
        return self._options.rp_endpoint

    @property
    def rp_launch(self):
        return self._options.rp_launch

    @property
    def rp_project(self):
        return self._options.rp_project

    @property
    def rp_launch_uuid(self):
        return self._options.rp_launch_uuid

    @property
    def rp_launch_doc(self):
        return self._options.rp_launch_doc

    @property
    def rp_launch_attributes(self):
        return self._options.rp_launch_attributes

    @property
    def rp_test_attributes(self):
        return self._options.rp_test_attributes

    @property
    def rp_log_batch_size(self):
        return self._options.rp_log_batch_size
