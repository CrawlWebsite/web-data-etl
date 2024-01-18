from abc import abstractmethod


class BaseExporter(object):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def export_items(self, items):
        pass

    @abstractmethod
    def export_item(self, item):
        pass

    @abstractmethod
    def convert_items(self, items):
        pass

    @abstractmethod
    def close(self):
        pass

