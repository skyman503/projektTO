import unittest
from django.test import Client, SimpleTestCase
from ...models import UrlCollection, UrlModel

TESTING_STORAGE_PATH = 'test.storage'
TESTING_URL = 'https://www.wolframalpha.com/'
TESTING_NEW_URL = "11111"

class ConnectTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.test_item = UrlModel(original_url=TESTING_URL, new_url=TESTING_NEW_URL)
        self.url_collection = UrlCollection()
        self.url_collection.storage_path = TESTING_STORAGE_PATH
        self.url_collection.reload_data()

    def test_worng_url(self) :
        response = self.client.get('/r/1', follow=True)
        self.assertRedirects(response=response, expected_url='/', status_code=302, target_status_code=200)
    
    def test_valid_url(self) :
        with open(TESTING_STORAGE_PATH, mode='w') as storage:
            pass

        self.url_collection.add_item(self.test_item)

        response = self.client.get('/r/11111', follow=True)

        # Check number of redirects
        self.assertEquals(1, len(response.redirect_chain))
        # Check status code
        self.assertEquals(response.redirect_chain[0][1], 302)
        # Check final url
        self.assertAlmostEquals(response.redirect_chain[0][0], TESTING_URL)
