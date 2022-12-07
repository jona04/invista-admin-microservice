from confluent_kafka import Producer
import os

conf = {
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
        'security.protocol': os.getenv('SECURITY_PROTOCOL'),
        'sasl.username': os.getenv('SASL_USERNAME'),
        'sasl.password': os.getenv('SASL_PASSWORD'),
        'sasl.mechanism': os.getenv('SASL_MECHANISM'),
        'group.id': os.getenv('GROUP_ID'),
        'auto.offset.reset': 'earliest'
    }
producer = Producer(conf)