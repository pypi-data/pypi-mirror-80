# -----------------------------------------------------------------------------
# Copyright (C) 2019 HacKan (https://hackan.net)
#
# This file is part of HealthChecker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
import subprocess  # nosec: B404  # noqa: S404
import tempfile
from unittest import TestCase


class TestValidInputs(TestCase):

    def setUp(self):
        self.temp_filename = os.path.join(tempfile.gettempdir(), os.urandom(4).hex())

    def tearDown(self):
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)

    def _test_base(self, cmds, expected_results):
        for index, cmd in enumerate(cmds):
            expected = expected_results[index]
            result = subprocess.run(  # nosec: B603  # noqa: S603
                cmd,
                env={
                    **os.environ,
                    'HEALTHCHECKER_REQUESTS_TIMEOUT': '0.1',
                    'HEALTHCHECKER_LOG_LEVEL': 'debug',
                },
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            text = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
            self.assertEqual(text[-1:], '\n')  # ends with newline
            self.assertIn(expected, text)

    def test_cli_defaults(self):
        cmds = (('python3', '-m', 'healthchecker'),)
        expected = ('usage: healthchecker',)
        self._test_base(cmds, expected)

    def test_cli_option_version(self):
        cmds = (('python3', '-m', 'healthchecker', '--version'),)
        expected = ('HealthChecker v',)
        self._test_base(cmds, expected)

    def test_cli_option_help(self):
        cmds = (
            ('python3', '-m', 'healthchecker', '--help'),
            ('python3', '-m', 'healthchecker', '-h'),
        )
        expected = (
            'by HacKan (https://hackan.net) FOSS under GNU GPL v3.0 or\nnewer. '
            'Checks URLs through HTTP GET requests to verify their availability.'
        )
        self._test_base(cmds, expected)

    def test_cli_urls(self):
        cmds = (
            ('python3', '-m', 'healthchecker', '127.0.0.1:1'),
            ('python3', '-m', 'healthchecker', 'http://127.0.0.1:1'),
            ('python3', '-m', 'healthchecker', 'https://127.0.0.1:1'),
        )
        expected = (
            'Begin checking URL http://127.0.0.1:1',
            'Begin checking URL http://127.0.0.1:1',
            'Begin checking URL https://127.0.0.1:1',
        )
        self._test_base(cmds, expected)

    def test_cli_options_github(self):
        cmds = (
            (
                'python3',
                '-m',
                'healthchecker',
                '--gh-repo',
                'healthchecker/test',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--gh-repo',
                'healthchecker/test',
                '--gh-token',
                'test',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--gh-repo',
                'healthchecker/test',
                '--gh-token',
                'test',
                '--gh-filename',
                'test',
                'http://127.0.0.1:1',
            ),
        )
        expected = (
            'API Token is missing',
            'filename is missing',
            'Bad credentials for repository',
        )
        self._test_base(cmds, expected)

    def test_cli_options_notify(self):
        cmds = (
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                '--notify-header',
                'x-auth:abc123',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                '--notify-payload',
                'Failed URLs: ',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                '--notify-payload',
                'This URLs HEALTHCHECKER_FAILED_URLS failed.',
                'http://127.0.0.1:1',
            ),
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                '--notify-json',
                'http://127.0.0.1:1',
            ),
        )
        expected = (
            "Error POSTing data from/to https://127.0.0.1:1",  # noqa: Q000
            "Notifying https://127.0.0.1:1 with headers: {'x-auth': 'abc123'} "
            "and payload: http://127.0.0.1:1",  # noqa: Q000
            "Notifying https://127.0.0.1:1 with headers: {} and "  # noqa: P103,Q000
            "payload: Failed URLs: http://127.0.0.1:1",  # noqa: Q000
            "Notifying https://127.0.0.1:1 with headers: {} and "  # noqa: P103,Q000
            "payload: This URLs http://127.0.0.1:1 failed.",  # noqa: Q000
            "Notifying https://127.0.0.1:1 with headers: {'content-type': "
            "'application/json'} and payload: [\"http://127.0.0.1:1\"]",
        )  # noqa: Q000,P103
        self._test_base(cmds, expected)

    def test_cli_options_output(self):
        cmds = (
            (
                'python3',
                '-m',
                'healthchecker',
                '--output',
                self.temp_filename,
                '127.0.0.1:1',
            ),
            ('python3', '-m', 'healthchecker', '-o', self.temp_filename, '127.0.0.1:1'),
            ('python3', '-m', 'healthchecker', '--output', '-', '127.0.0.1:1'),
            ('python3', '-m', 'healthchecker', '-o', '-', '127.0.0.1:1'),
        )
        expected = (
            'Result stored as',
            'Result stored as',
            '"url": "http://127.0.0.1:1",',
            '"url": "http://127.0.0.1:1",',
        )
        self._test_base(cmds, expected)


class TestInvalidInputs(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_base(self, cmds, expected_results):
        for index, cmd in enumerate(cmds):
            expected = expected_results[index]
            result = subprocess.run(  # nosec: B603  # noqa: S603
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            ).stderr.decode('utf-8')
            self.assertIn(expected, result)

    def test_cli_inexistent_option(self):
        cmds = (('python3', '-m', 'healthchecker', '--inexistent'),)
        expected = ('error: unrecognized arguments',)
        self._test_base(cmds, expected)

    def test_cli_invalid_param_notify_header(self):
        cmds = (
            (
                'python3',
                '-m',
                'healthchecker',
                '--notify-url',
                'https://127.0.0.1:1',
                '--notify-header',
                'invalid',
                'https://127.0.0.1:1',
            ),
        )
        expected = ('At least one header is invalid, skipping...',)
        self._test_base(cmds, expected)
