# coding=utf-8
from utils import load_django
load_django()

import unittest
from webtest import TestApp


class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.browser = TestApp('http://localhost:8000/')

    def tearDown(self):
        pass

    def test_base_page(self):
        status_code = self.browser.get('http://localhost:8000/').status_code
        self.assertEquals(status_code, 200)

    def test_united_geo_page(self):
        status_code = self.browser.get('http://localhost:8000/unitedgeo/').status_code
        self.assertEquals(status_code, 200)

    def test_propose_hpn_page(self):
        status_code = self.browser.get('http://localhost:8000/unitedgeo/propose-hpn/').status_code
        self.assertEquals(status_code, 200)

    def test_hpn_database_page(self):
        status_code = self.browser.get('http://localhost:8000/unitedgeo/send-hpn-database/').status_code
        self.assertEquals(status_code, 200)

    def test_seb_servicepage(self):
        status_code = self.browser.get('http://localhost:8000/unitedgeo/web-service/').status_code
        self.assertEquals(status_code, 200)

    def test_documentation_page(self):
        status_code = self.browser.get('http://localhost:8000/unitedgeo/documentation/').status_code
        self.assertEquals(status_code, 200)

    def test_databrowse_page(self):
        status_code = self.browser.get('http://localhost:8000/databrowse/').status_code
        self.assertEquals(status_code, 200)
