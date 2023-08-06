import unittest

from shipa.client.client import ShipaClient, CONST_TEST_SERVER, CONST_TEST_TOKEN
from shipa.client.http import MockResponse, MockClient


class ShipaPoolTestCase(unittest.TestCase):

    def test_pool_create(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.pool_add(pool="test")

        except Exception as e:
            assert e is None, str(e)

    def test_pool_create_failed(self):
        response = MockResponse(code=400, text='failed to create a pool')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.pool_add(pool="test")

    def test_pool_remove(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.pool_remove(pool="test")

        except Exception as e:
            assert e is None, str(e)

    def test_pool_remove_failed(self):
        response = MockResponse(code=400, text='failed to remove a pool')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.pool_remove(pool="test")

    def test_pool_update(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.pool_update(pool="test")

        except Exception as e:
            assert e is None, str(e)

    def test_pool_update_failed(self):
        response = MockResponse(code=400, text='failed to update a pool')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.pool_update(pool="test")
