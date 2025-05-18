#!/usr/bin/env python3
'''test utils.access_nested_map'''
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    '''Class to test utils.access_nested_map'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        '''Test the function access_nested_map'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map,
                                         path,
                                         expected_exception):
        '''Test the function access_nested_map'''
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''class to  test utils.get_json'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, expected_payload):
        '''test the get_json function'''
        with patch('utils.requests.get') as mock_method:
            mock_method.return_value.json.return_value = expected_payload
            result = get_json(url)
        mock_method.assert_called_once_with(url)
        self.assertEqual(result, expected_payload)
