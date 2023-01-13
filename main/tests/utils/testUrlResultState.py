import unittest
from unittest import TestCase
from ...utils import UrlResultState, UrlResult


class UrlResultStateTest(TestCase):
    def setUp(self):
        self.url_result_state = UrlResultState()
    
    def test_set_state(self):
        self.url_result_state.set_state(UrlResult.OK)
        self.assertEquals(UrlResult.OK, self.url_result_state.current_state)
    
    def test_get_state(self):
        self.url_result_state.current_state = UrlResult.WRONG_URL
        self.assertEquals(UrlResult.WRONG_URL, self.url_result_state.get_current_state())
