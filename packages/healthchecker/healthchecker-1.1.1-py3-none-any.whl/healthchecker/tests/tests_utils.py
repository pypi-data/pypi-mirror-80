# -----------------------------------------------------------------------------
# Copyright (C) 2019 Erus (https://git.rlab.be/erus)
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

from unittest import TestCase
from unittest import mock

import requests

from healthchecker.utils import http_request
from healthchecker.utils import logger
from healthchecker.utils import parse_url


class TestValidInputs(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_url_with_scheme(self):
        result = parse_url('http://test.local')
        self.assertEqual(result, 'http://test.local')

    def test_parse_url_without_scheme(self):
        result = parse_url('test.local')
        self.assertEqual(result, 'http://test.local')

    @mock.patch.object(logger, 'debug')
    @mock.patch('healthchecker.utils.time')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_result_positive(
        self,
        mock_request,
        mock_time,
        mock_logger_debug,
    ):
        resp = mock.MagicMock()
        resp.ok = True
        mock_time.side_effect = 1.0, 2.0
        mock_request.return_value = resp
        response, request_time, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
            test=True,
        )
        mock_request.assert_called_once_with(
            'GET',
            'http://test.local',
            timeout=3,
            test=True,
        )
        mock_logger_debug.assert_called_once_with(
            'Request to %s took %.2f seconds',
            'http://test.local',
            1.0,
        )
        self.assertEqual(response, resp)
        self.assertEqual(request_time, 1.0)
        self.assertFalse(error)

    # noinspection PyUnusedLocal
    @mock.patch.object(logger, 'debug')
    @mock.patch.object(logger, 'warning')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_result_negative(
        self,
        mock_request,
        mock_logger_warning,
        mock_logger_debug,
    ):
        resp = mock.MagicMock()
        resp.ok = False
        resp.status_code = 400
        resp.text = 'test'
        mock_request.return_value = resp
        response, _, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
            test=True,
        )
        mock_request.assert_called_once_with(
            'GET',
            'http://test.local',
            timeout=3,
            test=True,
        )
        mock_logger_warning.assert_called_once_with(
            'Response from %s is NOT OK: %d %s',
            'http://test.local',
            400,
            'test',
        )
        self.assertEqual(response, resp)
        self.assertFalse(error)

    # noinspection PyUnusedLocal
    @mock.patch.object(logger, 'debug')
    @mock.patch.object(logger, 'error')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_exception_connectionerror(
        self,
        mock_request,
        mock_logger_error,
        mock_logger_debug,
    ):
        mock_request.side_effect = requests.exceptions.ConnectionError('test')
        response, _, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
        )
        mock_logger_error.assert_called_once_with(
            'Error %sing data from/to %s: %s',
            'GET',
            'http://test.local',
            "ConnectionError('test')",
        )
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(error)

    # noinspection PyUnusedLocal
    @mock.patch.object(logger, 'debug')
    @mock.patch.object(logger, 'error')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_exception_readtimeout(
        self,
        mock_request,
        mock_logger_error,
        mock_logger_debug,
    ):
        mock_request.side_effect = requests.exceptions.ReadTimeout('test')
        response, _, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
        )
        mock_logger_error.assert_called_once_with(
            'Error %sing data from/to %s: %s',
            'GET',
            'http://test.local',
            "ReadTimeout('test')",
        )
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(error)

    # noinspection PyUnusedLocal
    @mock.patch.object(logger, 'debug')
    @mock.patch.object(logger, 'error')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_exception_invalidurl(
        self,
        mock_request,
        mock_logger_error,
        mock_logger_debug,
    ):
        mock_request.side_effect = requests.exceptions.InvalidURL('test')
        response, _, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
        )
        mock_logger_error.assert_called_once_with(
            'Error %sing data from/to %s: %s',
            'GET',
            'http://test.local',
            "InvalidURL('test')",
        )
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(error)

    # noinspection PyUnusedLocal
    @mock.patch.object(logger, 'debug')
    @mock.patch.object(logger, 'error')
    @mock.patch('healthchecker.utils.requests.request')
    def test_http_request_exception_invalidschema(
        self,
        mock_request,
        mock_logger_error,
        mock_logger_debug,
    ):
        mock_request.side_effect = requests.exceptions.InvalidSchema('test')
        response, _, error = http_request(
            'GET',
            'http://test.local',
            timeout=3,
            log=True,
        )
        mock_logger_error.assert_called_once_with(
            'Error %sing data from/to %s: %s',
            'GET',
            'http://test.local',
            "InvalidSchema('test')",
        )
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(error)
