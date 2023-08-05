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
from unittest import TestCase
from unittest import mock

from healthchecker.core import ServiceStatus
from healthchecker.core import ServiceStatusList
from healthchecker.core import healthcheck_url
from healthchecker.core import healthcheck_urls
from healthchecker.core import logger
from healthchecker.core import notify


class TestValidInputs(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('healthchecker.core.http_request')
    def test_notify(self, mock_http_request):
        resp_ok = mock.MagicMock()
        resp_ok.ok = True
        mock_http_request.return_value = resp_ok, 0, False
        result = notify('https://test.local', 'payload', {})
        mock_http_request.assert_called_with(
            'POST',
            'https://test.local',
            log=False,
            timeout=5,
            headers={},
            data=b'payload',
        )
        self.assertTrue(result)
        mock_http_request.return_value = resp_ok, 0, True
        result = notify('https://test.local')
        mock_http_request.assert_called_with(
            'POST',
            'https://test.local',
            log=False,
            timeout=5,
            headers=None,
            data=None,
        )
        self.assertFalse(result)

    @mock.patch('healthchecker.core.http_request')
    def test_notify_additional_params_to_requests(self, mock_http_request):
        mock_http_request.return_value = mock.MagicMock(), 0, False
        notify('https://test.local', some='kword', more=True)
        mock_http_request.assert_called_once_with(
            'POST',
            'https://test.local',
            timeout=5,
            log=False,
            data=None,
            headers=None,
            some='kword',
            more=True,
        )

    @mock.patch('healthchecker.core.http_request')
    def test_notify_log(self, mock_http_request):
        resp_ok = mock.MagicMock()
        resp_ok.ok = True
        mock_http_request.return_value = resp_ok, 0, False
        notify('https://test.local', log=False)
        mock_http_request.assert_called_with(
            'POST',
            'https://test.local',
            log=False,
            timeout=5,
            headers=None,
            data=None,
        )
        notify('https://test.local', log=True)
        mock_http_request.assert_called_with(
            'POST',
            'https://test.local',
            log=True,
            timeout=5,
            headers=None,
            data=None,
        )

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.core.logger')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_with_data_correct(self, mock_http_request, mock_logger):
        # mock_logger just to mute output
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = 'body'
        mock_http_request.return_value = resp, 0, False
        result = healthcheck_url('https://test.local', 'body', timeout=5)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
        )
        self.assertEqual(result.url, 'https://test.local')
        self.assertTrue(result.alive)
        self.assertTrue(result.ok)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.core.logger')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_with_data_wrong(self, mock_http_request, mock_logger):
        # mock_logger just to mute output
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = ''
        mock_http_request.return_value = resp, 0, False
        result = healthcheck_url('https://test.local', 'body', timeout=5)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
        )
        self.assertEqual(result.url, 'https://test.local')
        self.assertTrue(result.alive)
        self.assertFalse(result.ok)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.core.logger')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_without_data_correct(self, mock_http_request, mock_logger):
        # mock_logger just to mute output
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = ''
        mock_http_request.return_value = resp, 0, False
        result = healthcheck_url('https://test.local', timeout=5)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
        )
        self.assertEqual(result.url, 'https://test.local')
        self.assertTrue(result.alive)
        self.assertTrue(result.ok)

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.core.logger')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_without_data_wrong(self, mock_http_request, mock_logger):
        # mock_logger just to mute output
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = ''
        mock_http_request.return_value = resp, 0, True
        result = healthcheck_url('https://test.local', timeout=5)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
        )
        self.assertEqual(result.url, 'https://test.local')
        self.assertFalse(result.alive)
        self.assertFalse(result.ok)

        resp.status_code = 400
        resp.ok = False
        mock_http_request.return_value = resp, 0, False
        result = healthcheck_url('https://test.local', timeout=5)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
        )
        self.assertEqual(result.url, 'https://test.local')
        self.assertTrue(result.alive)
        self.assertFalse(result.ok)

    @mock.patch.object(logger, 'info')
    @mock.patch.object(logger, 'warning')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_log(
        self,
        mock_http_request,
        mock_logger_warning,
        mock_logger_info,
    ):
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = ''
        mock_http_request.return_value = resp, 4, False
        healthcheck_url('https://test.local', timeout=5, log=False)
        mock_logger_info.assert_not_called()
        mock_logger_warning.assert_not_called()

        mock_http_request.return_value = resp, 5.555, True
        healthcheck_url('https://test.local', timeout=5, log=True)
        mock_logger_warning.assert_called_with(
            'Request to %s timed out taking %.2f seconds',
            'https://test.local',
            5.555,
        )
        mock_http_request.return_value = resp, 4, False
        healthcheck_url('https://test.local', timeout=5, log=True)
        mock_logger_warning.assert_called_with(
            'Request to %s took too long: %.2f seconds',
            'https://test.local',
            4,
        )
        mock_logger_info.assert_has_calls((
            mock.call('Begin checking URL %s...', 'https://test.local'),
            mock.call('Finish checking URL: %s', 'https://test.local is DEAD'),
            mock.call('Begin checking URL %s...', 'https://test.local'),
            mock.call('Finish checking URL: %s', 'https://test.local is ALIVE and OK'),
        ))

    # noinspection PyUnusedLocal
    @mock.patch('healthchecker.core.logger')
    @mock.patch('healthchecker.core.http_request')
    def test_healthcheck_url_additional_params_to_requests(
        self,
        mock_http_request,
        mock_logger,
    ):
        # mock_logger just to mute output
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.ok = True
        resp.text = ''
        mock_http_request.return_value = resp, 0, False
        healthcheck_url('https://test.local', timeout=5, some='kword', more=True)
        mock_http_request.assert_called_with(
            'GET',
            'https://test.local',
            timeout=5,
            log=False,
            some='kword',
            more=True,
        )

    @mock.patch('healthchecker.core.healthcheck_url')
    def test_healthcheck_urls_without_validations(self, mock_healthcheck):
        urls = ['https://test.local', 'https://test2.local']
        results = ServiceStatus(urls[0]), ServiceStatus(urls[1])
        mock_healthcheck.side_effect = results
        statuses = asyncio.run(healthcheck_urls(urls, timeout=5))
        mock_healthcheck.assert_has_calls((
            mock.call('https://test.local', None, timeout=5, log=False),
            mock.call('https://test2.local', None, timeout=5, log=False),
        ))
        self.assertIsInstance(statuses, ServiceStatusList)
        self.assertEqual(statuses[0], results[0])
        self.assertEqual(statuses[1], results[1])

    @mock.patch('healthchecker.core.healthcheck_url')
    def test_healthcheck_urls_with_validations(self, mock_healthcheck):
        urls = ['https://test.local', 'https://test2.local']
        validations = ['']
        mock_healthcheck.return_value = ServiceStatus()
        statuses = asyncio.run(healthcheck_urls(urls, validations, timeout=5))
        mock_healthcheck.assert_has_calls((
            mock.call('https://test.local', '', timeout=5, log=False),
            mock.call('https://test2.local', '', timeout=5, log=False),
        ))
        self.assertIsInstance(statuses, ServiceStatusList)

    @mock.patch('healthchecker.core.healthcheck_url')
    def test_healthcheck_urls_additional_params_to_requests(self, mock_healthcheck):
        urls = ['https://test.local']
        validations = ['']
        mock_healthcheck.return_value = ServiceStatus()
        asyncio.run(
            healthcheck_urls(
                urls,
                validations,
                timeout=5,
                some='kword',
                more=True,
            ),
        )
        mock_healthcheck.assert_has_calls((
            mock.call(
                'https://test.local',
                '',
                timeout=5,
                log=False,
                some='kword',
                more=True,
            ),
        ))
