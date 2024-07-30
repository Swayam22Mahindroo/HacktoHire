import os
from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv

load_dotenv()

def create_kafka_consumer():
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'group.id': 'flights_notification_consumer_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    return consumer

def consume_messages():
    consumer = create_kafka_consumer()
    consumer.subscribe(['flight_notifications'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f"Received message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
print('hello world')
if __name__ == '__main__':
    consume_messages()

