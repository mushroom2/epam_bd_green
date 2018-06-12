from kafka import KafkaProducer

config = {'bootstrap_servers': 'PLAINTEXT://sandbox-hdp.hortonworks.com:6667', 'api_version': (0, 10)}
producer = KafkaProducer(**config)


def write_to_topic(storage):
    for poi in storage:
        producer.send('kafka-connect', {poi: storage[poi]})
        producer.flush()
    producer.close()
