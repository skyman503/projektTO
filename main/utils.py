from functools import wraps
from enum import Enum
from abc import ABC, abstractmethod
from secrets import token_urlsafe
from ShortIT.settings import url_length
import random
import string
from datetime import datetime


# 1 dekorator + 2 singleton
class SingletonDecorator:
    def __init__(self, class_):
        self.class_ = class_
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.class_(*args,**kwds)
        return self.instance


class LogManager:
    def __init__(self, state_manager=None, file_manager = None, currentTimeFunc = None) -> None:
        self.state_manager = state_manager if state_manager else UrlResultState()
        self.file_manager = file_manager if file_manager else FileManager('logs.txt','a')
        self.currentTimeFunc = currentTimeFunc if currentTimeFunc else datetime.now

    def log(self, request, func_name):
        if self._validate_request(request):
            line = str(self.currentTimeFunc()) + ";" + request.method + ";" + request.build_absolute_uri() + ";" + func_name + ";" + str(self.state_manager.get_current_state()) + "\n"
            self.file_manager.write(line)
    
    def _validate_request(self,request):
        try:
            return request.method!=None and request.build_absolute_uri()!=None
        except:
            raise ValueError("request is not valid")


class FileManager:

    def __init__(self, path, mode, encoding='utf-8') -> None:
        self.file_path = path
        self.mode = mode
        self.encoding = encoding

    def write(self,line):
        with open(self.file_path, mode=self.mode, encoding=self.encoding) as f:
            f.write(line)



# dekorator
def log(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        f = function(request, *args, **kwargs)
        LogManager().log(request, function.__name__)
        return f

    return wrap


class UrlResult(Enum):
    OK = {'msg': 'Your form has been submited',
            'valid': 1}
    WRONG_URL = {'msg': 'Enter a valid url !',
            'valid': 0}
    UNKNOWN = {'msg': 'Error occured! Please try again later.',
            'valid': 0}

# 3 Stan
class UrlResultState:
    def __init__(self) -> None:
        self.current_state = UrlResult.UNKNOWN

    def set_state(self, state):
        self.current_state = state
    
    def get_current_state(self):
        return self.current_state

UrlResultState = SingletonDecorator(UrlResultState)

# 4 strategia
class Strategy(ABC):
    @abstractmethod
    def generate_hash(self, data):
        pass


class BuiltInSecretStrategy(Strategy):
    def generate_hash(self, data):
        return token_urlsafe(url_length)


class UrlBasedStrategy(Strategy):
    def generate_hash(self, data):
        hash = ""
        offset = len(data) // (url_length-2)

        for i in range(0, len(data), offset):
            hash += data[i]
        
        for i in range(len(hash), url_length):
            hash += random.choice(string.ascii_letters + string.digits)
        
        return hash
