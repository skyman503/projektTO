import unittest
from django.test import Client, SimpleTestCase
from django.urls import reverse
from ...utils import log, UrlResultState, UrlResult
from ...models import UrlCollection, UrlModel
from ShortIT.settings import home_url

TESTING_STORAGE_PATH = 'test.storage'
TESTING_URL = 'https://www.wolframalpha.com/'


class AddUrlTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('add_url')
        self.url_collection = UrlCollection()
        self.url_collection.storage_path = TESTING_STORAGE_PATH
        self.url_collection.reload_data()

    def tearDown(self):
        with open(TESTING_STORAGE_PATH, mode='w') as storage:
            pass

    def test_add_valid_url(self):
        response = self.client.post(self.url, {'old_url': TESTING_URL})

        # load data from the disk file
        with open(TESTING_STORAGE_PATH, mode='r') as storage:
            storage_content = [x.rstrip().split(' ') for x in storage.readlines()]
            self.assertEquals(1, len(storage_content))
            self.assertEquals(TESTING_URL, storage_content[0][0])
            self.assertEquals(UrlResultState().get_current_state(), UrlResult.OK)

            generated_url = str(home_url) + 'r/' + storage_content[0][1]
            self.assertJSONEqual(str(response.content, encoding='utf8'), {
                'msg': UrlResultState().get_current_state().value["msg"],
                'valid': UrlResultState().get_current_state().value["valid"],
                'new_url': generated_url
            })
    
    def test_add_invalid_url(self):
        invalid_prefix = "I'm not an url"
        response = self.client.post(self.url, {'old_url': invalid_prefix+TESTING_URL})

        # load data from the disk file
        with open(TESTING_STORAGE_PATH, mode='r') as storage:
            storage_content = [x.rstrip().split(' ') for x in storage.readlines()]
            self.assertEquals(1, len(storage_content))
            self.assertEquals(TESTING_URL, storage_content[0][0])
            self.assertEquals(UrlResultState().get_current_state(), UrlResult.WRONG_URL)

            generated_url = str(home_url) + 'r/' + storage_content[0][1]
            self.assertJSONEqual(str(response.content, encoding='utf8'), {
                'msg': UrlResultState().get_current_state().value["msg"],
                'valid': UrlResultState().get_current_state().value["valid"],
                'new_url': generated_url
            })
