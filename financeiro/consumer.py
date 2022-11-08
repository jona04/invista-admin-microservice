import os
import django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from core.models import KafkaError
import core.listeners
import json


conf = {
        'bootstrap.servers': 'pkc-ldjyd.southamerica-east1.gcp.confluent.cloud:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.username': 'MABSYUGWW23PZAFB',
        'sasl.password': 'ZgFhk8CANir6A17SoxYlv2Pz4ReQAROtrr1yIYVBHIcFGWG+xyP5+xDWxFFqz2lA',
        'sasl.mechanism': 'PLAIN',
        'group.id': 'myGroup',
        'auto.offset.reset': 'earliest'
    }
consumer = Consumer(conf)

consumer.subscribe(['financeiro_topic'])

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
