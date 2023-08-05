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

import asyncio
import os
import sys
import tempfile
from contextlib import contextmanager
from io import StringIO
from unittest import TestCase
from unittest import mock

from healthchecker import __main__
from healthchecker.core import ServiceStatus
from healthchecker.core import ServiceStatusList


# https://stackoverflow.com/a/32498408/3626032
class AsyncMock(mock.MagicMock):

    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@contextmanager
def capture_output():
    """Capture stdout and stderr.

    :Source:
        https://stackoverflow.com/a/17981937
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestValidInputs(TestCase):

    def setUp(self):
        self.temp_filename = os.path.join(tempfile.gettempdir(), os.urandom(4).hex())

    def tearDown(self):
        if os.path.exists(self.temp_filename):
            if os.path.isfile(self.temp_filename):
                os.unlink(self.temp_filename)
            else:
                os.rmdir(self.temp_filename)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_ok(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification OK
        mock_notify.return_value = True
        result = __main__._notify('https://test.local', svclist)
        mock_notify.assert_called_with(
            'https://test.local',
            'http://test.local',
            {},
            log=True,
        )
        self.assertTrue(result)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_failed(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification failed
        mock_notify.return_value = False
        result = __main__._notify('https://test.local', svclist)
        mock_notify.assert_called_with(
            'https://test.local',
            'http://test.local',
            {},
            log=True,
        )
        self.assertFalse(result)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_with_headers(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification with headers
        __main__._notify(
            'https://test.local',
            svclist,
            headers={'x-freedom': '#FreeOlaBini'},
        )
        mock_notify.assert_called_with(
            'https://test.local',
            'http://test.local',
            {'x-freedom': '#FreeOlaBini'},
            log=True,
        )

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_with_payload(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification with payload
        __main__._notify('https://test.local', svclist, 'payload: ')
        mock_notify.assert_called_with(
            'https://test.local',
            'payload: http://test.local',
            {},
            log=True,
        )

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_with_payload_composed(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification with composed payload
        __main__._notify(
            'https://test.local',
            svclist,
            'payload: HEALTHCHECKER_FAILED_URLS',
        )
        mock_notify.assert_called_with(
            'https://test.local',
            'payload: http://test.local',
            {},
            log=True,
        )

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_json(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification using JSON
        __main__._notify('https://test.local', svclist, use_json=True)
        mock_notify.assert_called_with(
            'https://test.local',
            '["http://test.local"]',
            {'content-type': 'application/json'},
            log=True,
        )

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.notify')
    def test_notify_all_options(self, mock_notify, mock_logger):
        # mock_logger just to mute output
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        # Notification with composed payload, headers and using JSON
        __main__._notify(
            'https://test.local',
            svclist,
            '{"failed_urls": HEALTHCHECKER_FAILED_URLS}',
            {'x-freedom': '#FreeOlaBini'},
            True,
        )
        mock_notify.assert_called_with(
            'https://test.local',
            '{"failed_urls": ["http://test.local"]}',
            {
                'x-freedom': '#FreeOlaBini',
                'content-type': 'application/json',
            },
            log=True,
        )

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_create_file(self, mock_github, mock_logger):
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        commit = mock.MagicMock()
        commit.sha = 'abc123'
        repo = mock.MagicMock()
        repo.get_contents.side_effect = Exception()
        mock_github.UnknownObjectException = Exception
        repo.create_file.return_value = {
            'commit': commit,
        }
        gh = mock.MagicMock()
        gh.get_repo.return_value = repo
        mock_github.Github.return_value = gh
        mock_github.InputGitAuthor = lambda name, email: name + ' ' + email
        sec = 'abc123'
        result = __main__._to_github('healthchecker/test', sec, 'ftest', svclist)
        mock_github.Github.assert_called_once_with(login_or_token=sec)
        gh.get_repo.assert_called_once_with('healthchecker/test')
        repo.get_contents.assert_called_once_with('ftest')
        repo.create_file.assert_called_once_with(
            path='ftest',
            message='[HealthChecker] Create ftest',
            content=svclist.as_json(pretty=True) + '\n',
            branch='main',
            committer='HealthChecker hackan+healthchecker@rlab.be',
        )
        mock_logger.info.assert_called_with(
            'File %s %s: %s',
            'ftest',
            'created',
            'abc123',
        )
        self.assertTrue(result)

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_update_file_no_changes(self, mock_github, mock_logger):
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        file_content = svclist.as_json(pretty=True) + '\n'
        file = mock.MagicMock()
        file.decoded_content = file_content.encode('utf-8')
        repo = mock.MagicMock()
        repo.get_contents.return_value = file
        gh = mock.MagicMock()
        gh.get_repo.return_value = repo
        mock_github.Github.return_value = gh
        mock_github.InputGitAuthor = lambda name, email: name + ' ' + email
        id_, sec = 'abc', '123'
        result = __main__._to_github(
            'healthchecker/test',
            f'{id_},{sec}',
            'ftest',
            svclist,
        )
        mock_github.Github.assert_called_once_with(client_id=id_, client_secret=sec)
        gh.get_repo.assert_called_once_with('healthchecker/test')
        repo.get_contents.assert_called_once_with('ftest')
        mock_logger.info.assert_called_with(
            'File %s %s: %s',
            'ftest',
            'kept unchanged',
            'no changes detected',
        )
        self.assertTrue(result)

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_update_file(self, mock_github, mock_logger):
        svclist = ServiceStatusList(ServiceStatus(url='http://test.local'))

        commit = mock.MagicMock()
        commit.sha = 'abc123'
        file = mock.MagicMock()
        file.decoded_content = 'test'.encode('utf-8')
        file.sha = 'abc123'
        file.path = 'testpath'
        repo = mock.MagicMock()
        repo.get_contents.return_value = file
        repo.update_file.return_value = {
            'commit': commit,
        }
        gh = mock.MagicMock()
        gh.get_repo.return_value = repo
        mock_github.Github.return_value = gh
        mock_github.InputGitAuthor = lambda name, email: name + ' ' + email
        sec = 'abc123'
        result = __main__._to_github('healthchecker/test', sec, 'ftest', svclist)
        mock_github.Github.assert_called_once_with(login_or_token=sec)
        gh.get_repo.assert_called_once_with('healthchecker/test')
        repo.get_contents.assert_called_once_with('ftest')
        repo.update_file.assert_called_once_with(
            path='testpath',
            message='[HealthChecker] Update ftest',
            content=svclist.as_json(pretty=True) + '\n',
            sha='abc123',
            branch='main',
            committer='HealthChecker hackan+healthchecker@rlab.be',
        )
        mock_logger.info.assert_called_with(
            'File %s %s: %s',
            'ftest',
            'updated',
            'abc123',
        )
        self.assertTrue(result)

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_repo_not_found(self, mock_github, mock_logger):
        gh = mock.MagicMock()
        gh.get_repo.side_effect = Exception()
        mock_github.UnknownObjectException = Exception
        mock_github.Github.return_value = gh
        result = __main__._to_github(
            'healthchecker/test',
            'abc123',
            'ftest',
            ServiceStatusList(),
        )
        gh.get_repo.assert_called_once_with('healthchecker/test')
        mock_logger.error.assert_called_once_with(
            'Repository %s not found',
            'healthchecker/test',
        )
        self.assertFalse(result)

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_bad_creds(self, mock_github, mock_logger):
        gh = mock.MagicMock()
        gh.get_repo.side_effect = Exception()
        mock_github.UnknownObjectException = ValueError
        mock_github.BadCredentialsException = Exception
        mock_github.Github.return_value = gh
        result = __main__._to_github(
            'healthchecker/test',
            'abc123',
            'ftest',
            ServiceStatusList(),
        )
        gh.get_repo.assert_called_once_with('healthchecker/test')
        mock_logger.error.assert_called_once_with(
            'Bad credentials for repository %s',
            'healthchecker/test',
        )
        self.assertFalse(result)

    @mock.patch('healthchecker.__main__.logger')
    def test_to_github_no_filename(self, mock_logger):
        result = __main__._to_github(
            'healthchecker/test',
            'abc123',
            '',
            ServiceStatusList(),
        )
        mock_logger.error.assert_called_once_with(
            'Repository %s indicated to store '
            'results but filename is missing',
            'healthchecker/test',
        )
        self.assertFalse(result)

    @mock.patch('healthchecker.__main__.logger')
    def test_to_github_no_token(self, mock_logger):
        result = __main__._to_github(
            'healthchecker/test',
            '',
            'ftest',
            ServiceStatusList(),
        )
        mock_logger.error.assert_called_once_with(
            'Repository %s indicated to store '
            'results but Github API Token is '
            'missing',
            'healthchecker/test',
        )
        self.assertFalse(result)

    @mock.patch('healthchecker.__main__.logger')
    def test_to_file_new(self, mock_logger):
        statuses = ServiceStatusList()
        result = __main__._to_file(self.temp_filename, statuses)
        mock_logger.info.assert_called_once()
        mock_logger.error.assert_not_called()
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_filename))
        with open(self.temp_filename, 'rt') as file:
            content = file.read()
        self.assertEqual(content, statuses.as_json(pretty=True))

    @mock.patch('healthchecker.__main__.logger')
    def test_to_file_existing(self, mock_logger):
        statuses = ServiceStatusList()
        _, self.temp_filename = tempfile.mkstemp()
        result = __main__._to_file(self.temp_filename, statuses)
        mock_logger.info.assert_called_once()
        mock_logger.error.assert_not_called()
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_filename))
        with open(self.temp_filename, 'rt') as file:
            content = file.read()
        self.assertEqual(content, statuses.as_json(pretty=True))

    @mock.patch('healthchecker.__main__.logger')
    def test_to_file_existing_not_a_file(self, mock_logger):
        statuses = ServiceStatusList()
        self.temp_filename = tempfile.mkdtemp()
        result = __main__._to_file(self.temp_filename, statuses)
        mock_logger.error.assert_called_once()
        mock_logger.info.assert_not_called()
        self.assertFalse(result)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.__main__.logger')
    def test_to_file_stdout(self, mock_logger):
        # mock_logger just to mute output
        statuses = ServiceStatusList()
        with capture_output() as (out, err):
            result = __main__._to_file('-', statuses)
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_not_called()
        self.assertTrue(result)
        self.assertEqual(out.getvalue().strip(), statuses.as_json(pretty=True))

    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_version(self, mock_argparser):
        args = mock.MagicMock()
        args.version = True
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_url(self, mock_argparser, mock_healthcheckurls):
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.notify_url, args.gh_repo, args.output = None, None, None
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once_with(
            ['http://test.local'],
            [],
            timeout=10,
            log=True,
        )
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._to_github')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_github_ok(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_to_github,
    ):
        mock_healthcheckurls.return_value = 'statuses'
        mock_to_github.return_value = True
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.notify_url, args.output = None, None
        args.gh_repo = 'healthchecker/test'
        args.gh_filename = 'ftest'
        args.gh_branch = 'branch'
        args.gh_email = 'healthchecker@hackan.net'
        args.gh_token = 'abc123'
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_to_github.assert_called_once_with(
            'healthchecker/test',
            'abc123',
            'ftest',
            'statuses',
            'branch',
            'healthchecker@hackan.net',
        )
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._to_github')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_github_failed(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_to_github,
    ):
        mock_healthcheckurls.return_value = 'statuses'
        mock_to_github.return_value = False
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.notify_url, args.output = None, None
        args.gh_repo = 'healthchecker/test'
        args.gh_filename = 'ftest'
        args.gh_branch = 'branch'
        args.gh_email = 'healthchecker@hackan.net'
        args.gh_token = 'abc123'
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_to_github.assert_called_once_with(
            'healthchecker/test',
            'abc123',
            'ftest',
            'statuses',
            'branch',
            'healthchecker@hackan.net',
        )
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._notify')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_notify_ok(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_notify,
    ):
        mock_healthcheckurls.return_value = False
        mock_notify.return_value = True
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.gh_repo, args.output = None, None
        args.notify_url = 'https://test.local'
        args.notify_payload = 'payload'
        args.notify_json = True
        args.notify_header = ('header:test',)
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_notify.assert_called_once_with(
            'https://test.local',
            False,
            'payload',
            {'header': 'test'},
            True,
        )
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._notify')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_notify_failed(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_notify,
    ):
        mock_healthcheckurls.return_value = False
        mock_notify.return_value = False
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.gh_repo, args.output = None, None
        args.notify_url = 'https://test.local'
        args.notify_payload = 'payload'
        args.notify_json = True
        args.notify_header = ('header:test',)
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_notify.assert_called_once_with(
            'https://test.local',
            False,
            'payload',
            {'header': 'test'},
            True,
        )
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._to_file')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_output_file_ok(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_to_file,
    ):
        mock_healthcheckurls.return_value = 'statuses'
        mock_to_file.return_value = True
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.notify_url, args.gh_repo, args.output = None, None, 'filename'
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_to_file.assert_called_once_with('filename', 'statuses')
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__._to_file')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_output_file_failed(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_to_file,
    ):
        mock_healthcheckurls.return_value = 'statuses'
        mock_to_file.return_value = False
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.notify_url, args.gh_repo, args.output = None, None, 'filename'
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_to_file.assert_called_once_with('filename', 'statuses')
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__.main', new_callable=AsyncMock)
    def test_run(self, mock_main):
        mock_main.return_value = 0
        result = __main__.run()
        mock_main.assert_called_once()
        self.assertEqual(result, 0)

    @mock.patch('healthchecker.__main__.ArgumentParser')
    def test_arguments_parser(self, mock_argparser):
        result = __main__._get_arguments_parser()
        mock_argparser.assert_called_once()
        self.assertIsInstance(result, mock.MagicMock)


class TestInvalidInputs(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_no_args(self, mock_argparser):
        # should print usage and exit with error
        args = mock.MagicMock()
        args.version = False
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        result = asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        parser.print_usage.assert_called_once()
        self.assertEqual(result, 1)

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__._notify')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_arg_notify_wrong_headers(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_notify,
        mock_logger,
    ):
        mock_healthcheckurls.return_value = False
        mock_notify.return_value = True
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.gh_repo, args.output = None, None
        args.notify_url = 'https://test.local'
        args.notify_payload = 'payload'
        args.notify_json = True
        args.notify_header = ('header-test',)
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_notify.assert_called_once_with(
            'https://test.local',
            False,
            'payload',
            {},
            True,
        )
        mock_logger.error.assert_called_with(
            'At least one header is invalid, '
            'skipping...',
        )

    @mock.patch('healthchecker.settings.REQUESTS_TIMEOUT', 'wrong')
    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.healthcheck_urls', new_callable=AsyncMock)
    @mock.patch('healthchecker.__main__._get_arguments_parser')
    def test_main_wrong_timeout(
        self,
        mock_argparser,
        mock_healthcheckurls,
        mock_logger,
    ):
        args = mock.MagicMock()
        args.version = False
        args.url = ('http://test.local',)
        args.gh_repo, args.notify_url, args.output = None, None, None
        parser = mock.MagicMock()
        parser.parse_args.return_value = args
        mock_argparser.return_value = parser
        asyncio.run(__main__.main())
        parser.parse_args.assert_called_once()
        mock_healthcheckurls.assert_called_once()
        mock_logger.error.assert_called_with(
            'HEALTHCHECKER_REQUESTS_TIMEOUT '
            'must be a valid float, default '
            'to 10 seconds',
        )
        mock_healthcheckurls.assert_called_once_with(
            ['http://test.local'],
            [],
            timeout=10,
            log=True,
        )

    @mock.patch('healthchecker.__main__.logger')
    @mock.patch('healthchecker.__main__.github')
    def test_to_github_retrieves_list(self, mock_github, mock_logger):
        file = [mock.MagicMock()]
        repo = mock.MagicMock()
        repo.get_contents.return_value = file
        gh = mock.MagicMock()
        gh.get_repo.return_value = repo
        mock_github.Github.return_value = gh

        with self.assertRaises(ValueError):
            __main__._to_github(
                'healthchecker/test',
                'abc,123',
                'ftest',
                ServiceStatusList(),
            )
