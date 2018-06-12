from kafka import KafkaProducer

config = {'bootstrap_servers': 'sandbox-hdp.hortonworks.com:6667'}
producer = KafkaProducer(**config)


def write_to_topic(storage):
    for poi in storage:
        producer.send('kafka-connect', {poi: storage[poi]})
