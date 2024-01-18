from abc import abstractmethod
from typing import List

class ImportQuery:
    where: object

class BaseImporter(object):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def import_items(self, queries: List[ImportQuery]):
        pass

    @abstractmethod
    def import_item(self, query: ImportQuery):
        pass

    @abstractmethod
    def convert_items(self, items):
        pass

    @abstractmethod
    def close(self):
        pass

