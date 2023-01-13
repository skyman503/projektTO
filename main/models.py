from collections.abc import Iterable, Iterator
from .utils import SingletonDecorator, BuiltInSecretStrategy


class UrlModel():
    def __init__(self, original_url, collection=None, new_url="", strategy=None) -> None:
        self.original_url = original_url
        self.new_url = new_url
        self._strategy = strategy if strategy else BuiltInSecretStrategy()
        self.collection = collection if collection else UrlCollection()
    
    def set_strategy(self, strategy):
        self._strategy = strategy
    
    def get_strategy(self):
        return self._strategy
    
    def generate_new_url(self):
        while True:
            url = self._strategy.generate_hash(self.original_url)
            if all(x.new_url != url for x in self.collection):
                self.new_url = url
                return


# 5 iterator
class UrlOrderIterator(Iterator):
    def __init__(self, collection) -> None:
        self._collection = collection
        self._position = 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += 1
        except IndexError:
            raise StopIteration()

        return value


class UrlCollection(Iterable):
    def __init__(self, storage="url.storage") -> None:
        self.storage_path = storage
        with open(self.storage_path, mode='r', encoding='utf-8') as f:
            self._collection = [UrlModel(x.rstrip().split(" ")[0], x.rstrip().split(" ")[1]) for x in f.readlines()]

    def __iter__(self):
        return UrlOrderIterator(self._collection)
    
    def add_item(self, url_model):
        self._collection.append(url_model)
        self.save_item(url_model)

    def save_item(self, url_model):
        with open(self.storage_path, mode='a', encoding='utf-8') as f:
            line = str(url_model.original_url) + " " + str(url_model.new_url) + "\n"
            f.write(line)
            return line

    # use for testing purposes only
    def reload_data(self):
        with open(self.storage_path, mode='r', encoding='utf-8') as f:
            self._collection = [UrlModel(x.rstrip().split(" ")[0], x.rstrip().split(" ")[1]) for x in f.readlines()]



UrlCollection = SingletonDecorator(UrlCollection)
