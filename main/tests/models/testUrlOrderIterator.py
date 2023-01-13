import unittest
from unittest import TestCase
from ...models import UrlOrderIterator


class UrlOrderIteratorTest(TestCase):
    def setUp(self):
        self.mock_collection = [0, 1, 2]
        self.url_order_iterator = UrlOrderIterator(self.mock_collection)

    def test_valid_iteration(self):
        parameters = [-1, 1000]
        for test_case in parameters:

            self.url_order_iterator._position = test_case
            for item in self.url_order_iterator:
                self.assertIsNotNone(item)

    def test_index_out_of_bounds(self):
        invalid_index = -1
        self.url_order_iterator._position = invalid_index
        for _ in self.url_order_iterator:
            self.assertRaises(StopIteration)

    def test_valid_values_during_iteration(self):
        # Mocked collection ad index i stores i.
        for item, index in enumerate(self.url_order_iterator):
            self.assertEquals(item, index)
