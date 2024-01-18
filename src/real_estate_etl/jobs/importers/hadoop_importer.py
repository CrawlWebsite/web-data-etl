import collections
import json
import logging

from real_estate_etl.jobs.converters.composite_item_converter import CompositeItemConverter


class HadoopImporter:

    def __init__(self, input, item_type_to_topic_mapping, converters=()):
        self.item_type_to_topic_mapping = item_type_to_topic_mapping
        self.converter = CompositeItemConverter(converters)
        self.connection_url = self.get_connection_url(input)
        print(self.connection_url)

    def get_connection_url(self, input):
        try:
            return input.split('/')[1]
        except KeyError:
            raise Exception('Invalid kafka input param, It should be in format of "kafka/127.0.0.1:9092"')

    def open(self):
        pass

    def import_items(self, items):
        for item in items:
            self.import_item(item)

    def import_item(self, item):
        item_type = item.get('type')
        if item_type is not None and item_type in self.item_type_to_topic_mapping:
            data = json.dumps(item).encode('utf-8')
            logging.debug(data)
            # return self.producer.send(self.item_type_to_topic_mapping[item_type], value=data)
        else:
            logging.warning('Topic for item type "{}" is not configured.'.format(item_type))

    def convert_items(self, items):
        for item in items:
            yield self.converter.convert_item(item)

    def close(self):
        pass
