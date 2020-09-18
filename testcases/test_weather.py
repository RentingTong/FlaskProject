# -*- coding: utf-8 -*-
"""
@date: 2020/09/17

@author: Tara

@description:
Unit test for weather application.
"""
import unittest
import application.weather as w


class TestWeather(unittest.TestCase):

    def setUp(self):
        w.app.testing = True
        self.app = w.app.test_client()

    def test_001_default_route_returns_success(self):
        request = self.app.get('/')
        self.assertEqual(request.status_code, 200)

    def test_002_invaild_route_returns_404_page(self):
        request = self.app.get('/doesnotexist')
        self.assertEqual(request.status_code, 404)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
