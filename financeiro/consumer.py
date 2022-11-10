import os
import django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from core.models import KafkaError
import core.listeners
import json


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
    print(msg.value())
    try:
        getattr(core.listeners, msg.key().decode("utf-8").replace('"','').replace("'",""))(json.loads(msg.value()))
    except Exception as e:
        print("error consumer financeiro: ", e)
        KafkaError.objects.create(
            key=msg.key(),
            value=msg.value(),
            error=e,
        )

consumer.close()
