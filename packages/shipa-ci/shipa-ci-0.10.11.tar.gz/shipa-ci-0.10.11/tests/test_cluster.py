import unittest

from shipa.client.client import CONST_TEST_TOKEN, CONST_TEST_SERVER, ShipaClient
from shipa.client.http import MockResponse, MockClient


class ShipaClusterTestCase(unittest.TestCase):

    def test_pool_create(self):
        try:
            response = MockResponse(code=201)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.cluster_add('test', pools=tuple("test"))

        except Exception as e:
            assert e is None, str(e)

    def test_pool_create_failed(self):
        response = MockResponse(code=400, text='failed to create a cluster')
        http = MockClient(response=response)
        client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)

        with self.assertRaises(Exception):
            client.cluster_add('test', pools=tuple("test"))
