#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
  
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
                ({"a": 1}, ("a",), 1),
                ({"a": {"b": 2}}, ("a",), {"b":2}),
                ({"a": {"b": 2}}, ("a", "b"), 2)
                ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    @parameterized.expand([
                ({}, ("a",)),
                ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exemption(self,nested_map, path):
        self.assertRaises(KeyError, access_nested_map(nested_map, path))

class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        mock=Mock()
        mock.json.return_value = test_payload

        mock_get.return_value = mock

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)

        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            test_class = TestClass()
            test_class.a_property
            test_class.a_property
            mock_a_method.assert_called_once()



if __name__ == '__main__':
    unittest.main()
