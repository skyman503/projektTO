import unittest
from unittest import TestCase
from ...utils import BuiltInSecretStrategy, UrlBasedStrategy
from ShortIT.settings import url_length


TESTING_URL = 'https://www.google.com'

class StrategyTest(TestCase):

    def test_built_in_secret_strategy(self):
        generated_hash = BuiltInSecretStrategy().generate_hash(TESTING_URL)

        self.assertIsNotNone(generated_hash)
        self.assertEquals(url_length+2, len(generated_hash))
    
    def test_url_based_strategy(self):
        generated_hash = BuiltInSecretStrategy().generate_hash(TESTING_URL)

        self.assertIsNotNone(generated_hash)
        self.assertEquals(url_length+2, len(generated_hash))
