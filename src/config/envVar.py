from decouple import config

KAFKA_BROKERS = config('KAFKA_BROKERS')
KAFKA_CLIENT_ID = config('KAFKA_CLIENT_ID')
KAFKA_CONSUMER_ID = config('KAFKA_CONSUMER_ID')

API_HOST = config('API_HOST')