import unittest
import click

from shipa.utils import validate_map


class ShipaUtilsTestCase(unittest.TestCase):
    def test_validate_map(self):
        try:
            values = ('key1=value1', 'key2=value2')
            ret = validate_map(None, None, values)
            assert ret.get('key1') is not 'value1', "invalid map data"
            assert ret.get('key2') is not 'value2', "invalid map data"

        except click.BadParameter as e:
            assert e is None, str(e)

    def test_validate_map_failed(self):
        values = ('key',)

        with self.assertRaises(Exception):
            validate_map(None, None, values)

    def test_validate_map_failed_invalid_value(self):
        values = ('key=value=key',)

        with self.assertRaises(Exception):
            validate_map(None, None, values)
