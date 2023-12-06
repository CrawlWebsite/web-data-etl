from kafka import KafkaConsumer, KafkaProducer
from json import dumps, loads

from config.singleton import SingletonMeta  

class KafkaImpl(metaclass=SingletonMeta):
    def __init__(self, bootstrapServers, groupId):
        self.bootstrapServers = bootstrapServers
        self.groupId = groupId

        self.consumers = dict()
        self.producer = KafkaProducer(  
            bootstrap_servers = bootstrapServers,  
            value_serializer = lambda x:dumps(x).encode('utf-8')  
        )

    def consumerSubcribe(self, topic, callback):
        consumer = self.consumers.get(topic)
        if not consumer:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers = self.bootstrapServers,  
                auto_offset_reset = 'earliest',  
                enable_auto_commit = True,  
                group_id = self.groupId,  
                value_deserializer = lambda x : loads(x.decode('utf-8'))  
            )
            self.consumers[topic] = consumer

        for msg in consumer:
            callback(msg)

    
    def sendMessage(self, topic, message):
        self.producer.send(topic, message)