import json

from .context import src

import unittest
from flask_testing import TestCase
from requests.auth import _basic_auth_str


class TestInstagramApi(TestCase):
    def create_app(self):
        app = src.application
        app.config['TESTING'] = True
        self.run_gc_after_test = True
        return app

    def login(self):
        headers = {
            'Authorization': _basic_auth_str('user', 'password')
        }
        response = self.client.post("/api/login", headers=headers)
        return json.loads(response.data)['token']

    def test_find_profile(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.login())
        }
        response = self.client.post("/api/instagram/find", data=data, headers=headers)
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
