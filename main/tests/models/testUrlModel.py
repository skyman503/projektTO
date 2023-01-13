import unittest
from unittest import TestCase
from ...models import UrlModel
from ...utils import BuiltInSecretStrategy, UrlBasedStrategy


class UrlModelTest(TestCase):
    def setUp(self):
        self.url_model = UrlModel("https://www.google.com/")

    def test_set_strategy(self):
        self.assertEquals(type(self.url_model.get_strategy()), BuiltInSecretStrategy)

        self.url_model.set_strategy(UrlBasedStrategy())
        self.assertEquals(type(self.url_model.get_strategy()), UrlBasedStrategy)
    
    def test_generate_new_url_is_unique(self):
        self.url_model.generate_new_url()
        used_url = self.url_model.new_url

        self.url_model.generate_new_url()
        self.assertNotEquals(used_url, self.url_model.new_url)