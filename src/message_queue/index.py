from config.envVar import KAFKA_BROKERS
from message_queue.kafka.kafkaImpl import KafkaImpl


class MessageQueueConsumerImpl():
    def __init__(self):
        self.groupId = 'crawl-collector'

        self.queue = KafkaImpl(bootstrapServers=[KAFKA_BROKERS], groupId=self.groupId)
        
    def consumerSubcribe(self, topic, callback):
        self.queue.consumerSubcribe(topic, callback)

class MessageQueueProducerImpl():
    def __init__(self):
        self.groupId = 'crawl-collector'

        self.queue = KafkaImpl(bootstrapServers=[KAFKA_BROKERS], groupId=self.groupId)
        
    def sendMessage(self, topic, message):
        self.queue.sendMessage(topic, message)