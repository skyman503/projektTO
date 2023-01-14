import unittest
from unittest import TestCase
from ...utils import LogManager, FileManager, UrlResult
from ShortIT.settings import url_length
from unittest.mock import MagicMock

class LoggerTest(TestCase):

    def setUp(self):
        self.file_manager_mock = FileManager("testLog.txt", 'a')
        self.file_manager_mock.write = MagicMock(return_value=3)

    class FileManagerMock:
        def __init__(self, write) -> None:
            self.write = write

    class UrlResultStateMock:
        def get_current_state():
            return UrlResult.UNKNOWN

    class RequestTemplate:
        def __init__(self,build_absolute_uri,method) -> None:
            self.build_absolute_uri = build_absolute_uri
            self.method = method

    def test_valid_log_data_if_called_once(self):
        self.logManager = LogManager(file_manager=self.file_manager_mock)

        test_request = self.RequestTemplate(lambda : "test_http", "test_method")

        url_result_state_mock = self.UrlResultStateMock()
        url_result_state_mock.get_current_state = MagicMock(return_value = UrlResult.OK)


        self.logManager.log(test_request,"f name")
        
        self.file_manager_mock.write.assert_called_once()



    def test_valid_log_data_output_format(self):
        url_result_state_mock = self.UrlResultStateMock()
        url_result_state_mock.get_current_state = MagicMock(return_value = UrlResult.OK)


        test_request = self.RequestTemplate(lambda : "test_http", "test_method")
        self.logManager = LogManager(file_manager=self.file_manager_mock,state_manager=url_result_state_mock, currentTimeFunc=lambda:"current_time")


        self.logManager.log(test_request,"f name")
        
        self.file_manager_mock.write.assert_called_with("current_time;test_method;test_http;f name;UrlResult.OK\n")

    def test_valid_log_Wrong_Url(self):
        url_result_state_mock = self.UrlResultStateMock()

        test_request = self.RequestTemplate(lambda : "test_http", "test_method")
        self.logManager = LogManager(file_manager=self.file_manager_mock,state_manager=url_result_state_mock, currentTimeFunc=lambda:"current_time")

        url_result_state_mock.get_current_state = MagicMock(return_value = UrlResult.WRONG_URL)


        self.logManager.log(test_request,"f name")
        
        self.file_manager_mock.write.assert_called_with("current_time;test_method;test_http;f name;UrlResult.WRONG_URL\n")


    def test_invalid_request_throws_exception(self):
        url_result_state_mock = self.UrlResultStateMock()

        test_request = {}
        self.logManager = LogManager(file_manager=self.file_manager_mock,state_manager=url_result_state_mock, currentTimeFunc=lambda:"current_time")

        self.assertRaises(ValueError, self.logManager.log, test_request,"f name")
        


