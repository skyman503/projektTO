from unittest import TestCase
from ...models import UrlCollection, UrlModel

TESTING_STORAGE_PATH = 'test.storage'
TESTING_URL = 'https://www.google.com'
TESTING_NEW_URL = "11111"

class UrlCollectionTest(TestCase):
    def setUp(self):
        self.test_item = UrlModel(original_url=TESTING_URL, new_url=TESTING_NEW_URL)
        self.url_collection = UrlCollection()
        self.url_collection.storage_path = TESTING_STORAGE_PATH
        self.url_collection.reload_data()

    def test_add_item(self):
        self.url_collection.add_item(self.test_item)
        self.assertIn(self.test_item, self.url_collection)
    
    def test_save_item(self):
        with open(TESTING_STORAGE_PATH, mode='w') as storage:
            pass

        # act
        self.url_collection.add_item(self.test_item)

        # assert
        with open(TESTING_STORAGE_PATH, mode='r') as storage:
            storage_content = [x.rstrip() for x in storage.readlines()]
            self.assertEquals(1, len(storage_content))
            self.assertEquals(TESTING_URL + " " + TESTING_NEW_URL, storage_content[0])
