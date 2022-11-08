from confluent_kafka import Consumer
import core.listeners
import os, json

conf = {
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
        'security.protocol': os.getenv('SECURITY_PROTOCOL'),
        'sasl.username': os.getenv('SASL_USERNAME'),
        'sasl.password': os.getenv('SASL_PASSWORD'),
        'sasl.mechanism': os.getenv('SASL_MECHANISM'),
        'group.id': os.getenv('GROUP_ID'),
        'auto.offset.reset': 'earliest'
    }
consumer = Consumer(conf)

consumer.subscribe([os.getenv('KAFKA_TOPIC')])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    
    print(msg.key())
    
    getattr(core.listeners, msg.key().decode("utf-8").replace('"',''))(json.loads(msg.value()))

    print("Consumer received message: {}".format(msg.value()))

consumer.close()
