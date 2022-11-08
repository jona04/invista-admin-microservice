from confluent_kafka import Producer

conf = {
        'bootstrap.servers': 'pkc-ldjyd.southamerica-east1.gcp.confluent.cloud:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.username': 'MABSYUGWW23PZAFB',
        'sasl.password': 'ZgFhk8CANir6A17SoxYlv2Pz4ReQAROtrr1yIYVBHIcFGWG+xyP5+xDWxFFqz2lA',
        'sasl.mechanism': 'PLAIN',
        'group.id': 'myGroup',
        'auto.offset.reset': 'earliest'
    }
producer = Producer(conf)