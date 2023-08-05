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

from unittest import TestCase

from healthchecker.objects import ServiceStatus
from healthchecker.objects import ServiceStatusList


class TestValidInputs(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_servicestatus_init(self):
        url = 'http://test.local'
        alive = True
        ok = True
        servicestatus = ServiceStatus(url, alive, ok)
        self.assertEqual(servicestatus.url, url)
        self.assertEqual(servicestatus.alive, alive)
        self.assertEqual(servicestatus.ok, ok)

    def test_servicestatus_bool(self):
        servicestatus = ServiceStatus()
        self.assertFalse(bool(servicestatus))
        servicestatus.ok = True
        self.assertTrue(bool(servicestatus))

    def test_servicestatus_repr(self):
        servicestatus = ServiceStatus()
        string = 'ServiceStatus(uid=d41d8cd9, url=, alive=False, ok=False)'
        self.assertEqual(repr(servicestatus), string)

    def test_servicestatus_str(self):
        servicestatus = ServiceStatus()
        self.assertEqual(str(servicestatus), '')
        servicestatus.url = 'http://test.local'
        servicestatus.alive = False
        status = 'http://test.local is DEAD'
        self.assertEqual(str(servicestatus), status)
        servicestatus.alive = True
        servicestatus.ok = False
        status = 'http://test.local is ALIVE but NOT OK'
        self.assertEqual(str(servicestatus), status)
        servicestatus.ok = True
        status = 'http://test.local is ALIVE and OK'
        self.assertEqual(str(servicestatus), status)

    def test_servicestatus_uid(self):
        servicestatus = ServiceStatus()
        self.assertEqual(servicestatus.uid, 'd41d8cd9')
        servicestatus.url = 'http://test.local'
        self.assertEqual(servicestatus.uid, 'ea1f911a')

    def test_servicestatus_dict(self):
        url = 'http://test.local'
        alive = True
        ok = True
        servicestatus = ServiceStatus(url, alive, ok)
        dct = {
            'uid': 'ea1f911a',
            'url': url,
            'alive': alive,
            'ok': ok,
        }
        self.assertEqual(servicestatus.as_dict(), dct)

    def test_servicestatus_json(self):
        url, alive, ok = 'http://test.local', True, True
        servicestatus = ServiceStatus(url, alive, ok)
        json = (
            '{"uid": "ea1f911a", "url": "http://test.local", "alive": true, "ok": true}'
        )
        self.assertEqual(servicestatus.as_json(), json)
        json = (
            '{\n  "uid": "ea1f911a",\n  "url": "http://test.local",\n  '
            '"alive": true,\n  "ok": true\n}'
        )
        self.assertEqual(servicestatus.as_json(pretty=True), json)

    def test_servicestatuslist_len(self):
        svclst = ServiceStatusList()
        self.assertEqual(len(svclst), 0)
        servicestatus = ServiceStatus()
        svclst.append(servicestatus)
        self.assertEqual(len(svclst), 1)

    def test_servicestatuslist_bool(self):
        svclst = ServiceStatusList()
        self.assertFalse(bool(svclst))
        servicestatus = ServiceStatus()
        svclst.append(servicestatus)
        self.assertFalse(bool(svclst))
        servicestatus.ok = True
        self.assertTrue(bool(svclst))

    def test_servicestatuslist_repr(self):
        svclst = ServiceStatusList()
        string = 'ServiceStatusList([])'
        self.assertEqual(repr(svclst), string)
        svclst.append(ServiceStatus())
        string = (
            'ServiceStatusList([ServiceStatus(uid=d41d8cd9, url=, '
            'alive=False, ok=False)])'
        )
        self.assertEqual(repr(svclst), string)

    def test_servicestatuslist_str(self):
        svclst = ServiceStatusList()
        string = ''
        self.assertEqual(str(svclst), string)
        svclst.append(ServiceStatus())
        self.assertEqual(str(svclst), string)
        svclst = ServiceStatusList(
            ServiceStatus(url='http://test.local'),
            ServiceStatus(url='https://test.local'),
        )
        string = 'http://test.local is DEAD, https://test.local is DEAD'
        self.assertEqual(str(svclst), string)

    def test_servicestatuslist_actions(self):
        svclst = ServiceStatusList()
        servicestatus = ServiceStatus()
        svclst.append(servicestatus)
        self.assertEqual(servicestatus, svclst[0])
        servicestatus2 = ServiceStatus(alive=True)
        svclst.append(servicestatus2)
        self.assertEqual(len(svclst), 2)
        self.assertEqual(servicestatus2, svclst.pop())
        self.assertEqual(len(svclst), 1)
        svclst.insert(0, servicestatus2)
        self.assertEqual(len(svclst), 2)
        self.assertEqual(servicestatus2, svclst[0])
        for svc in svclst:
            self.assertIn(svc, [servicestatus, servicestatus2])
        del svclst[0]
        self.assertEqual(len(svclst), 1)
        self.assertEqual(svclst[0], servicestatus)
        svclst2 = ServiceStatusList()
        svclst2.append(servicestatus2)
        svclst.extend(svclst2)
        self.assertEqual(len(svclst), 2)
        self.assertEqual(svclst[1], servicestatus2)
        svclst[0] = servicestatus2
        self.assertEqual(len(svclst), 2)
        self.assertEqual(svclst[0], servicestatus2)
        svclst = ServiceStatusList(servicestatus, servicestatus2)
        self.assertEqual(len(svclst), 2)
        self.assertEqual(svclst[0], servicestatus)
        self.assertEqual(svclst[1], servicestatus2)

    def test_servicestatuslist_json(self):
        svclst = ServiceStatusList()
        url, alive, ok = 'http://test.local', True, True
        servicestatus = ServiceStatus(url, alive, ok)
        svclst.append(servicestatus)
        json = (
            '[{"uid": "ea1f911a", "url": "http://test.local", "alive": true, '
            '"ok": true}]'
        )
        self.assertEqual(svclst.as_json(), json)
        json = (
            '[\n  {\n    "uid": "ea1f911a",\n    "url": "http://test.local",'
            '\n    "alive": true,\n    "ok": true\n  }\n]'
        )
        self.assertEqual(svclst.as_json(pretty=True), json)
