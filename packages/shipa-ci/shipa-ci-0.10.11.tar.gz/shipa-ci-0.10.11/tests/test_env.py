import unittest

from shipa.client.client import ShipaClient, CONST_TEST_SERVER, CONST_TEST_TOKEN
from shipa.client.http import MockResponse, MockClient


class ShipaEnvTestCase(unittest.TestCase):

    def test_env_set(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.env_set(app_name="test")

        except Exception as e:
            assert e is None, str(e)

    def test_env_set_failed(self):
        response = MockResponse(code=400, text='failed to set env')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.env_set(app_name="test")

    def test_env_unset(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.env_unset(app_name="test")

        except Exception as e:
            assert e is None, str(e)

    def test_env_unset_failed(self):
        response = MockResponse(code=400, text='failed to remove env')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.env_unset(app_name="test")
