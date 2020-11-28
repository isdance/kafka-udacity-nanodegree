### Python library

use `confluent_kafka`. 

[documetation](https://docs.confluent.io/5.0.0/clients/confluent-kafka-python/index.html)



```py
import asyncio

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic


BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "my-first-python-topic"


async def produce(topic_name):
    """
    produce data into kafka topic
    """
    p = Producer({"bootstrap.servers": BROKER_URL})
    count = 0
    while True:
        p.produce(topic_name, f"message: {count}")
        count += 1
        await asyncio.sleep(1)


async def consume(topic_name):
    """
    pull data from kafka topic
    """
    c = Consumer({"bootstrap.servers": BROKER_URL, "group.id": "first-python-consumer-group"})
    c.subscribe([topic_name])

    while True:
        message = c.poll(1.0)
        if message is None:
            print("NO message received!")
        elif message.error() is not None:
            print(f"Message had an error {message.error()}")
        else:
            print(f"key: {message.key()}, value: {message.value()}")

        await asyncio.sleep(1)


async def produce_and_consume():
    t1 = asyncio.create_task(produce(TOPIC_NAME))
    t2 = asyncio.create_task(consume(TOPIC_NAME))
    await t1
    await t2


def main():
    """
    create topic, then run producer and consumer
    """
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    topic = NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)

    client.create_topics([topic])

    try:
        asyncio.run(produce_and_consume())
    except KeyboardInterrupt as e:
        print("shutting down")
    finally:
        client.delete_topics([topic])


if __name__ == "__main__":
    main()
```
