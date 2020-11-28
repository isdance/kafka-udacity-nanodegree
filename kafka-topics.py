import asyncio

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic


BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "my-second-python-topic"


def topic_exists(client: Consumer, topic_name: str) -> bool:
    topic_metadata = client.list_topics(timeout=5)
    return topic_metadata.topics.get(topic_name) is not None


def create_topic(client: AdminClient, topic_name: str) -> NewTopic:
    newTopic: NewTopic = NewTopic(
        topic_name,
        num_partitions=1,
        replication_factor=1,
        config={
            "cleanup.policy": "compact",
            "compression.type": "gzip",
            "delete.retention.ms": 864000000,
            "file.delete.delay.ms": 60000,
        },
    )

    # a dict of futures for each topic, keyed by the topic name. 
    # :rtype: dict(<topic_name, future>)
    # https://docs.confluent.io/5.0.0/clients/confluent-kafka-python/
    futures: dict = client.create_topics([newTopic])

    for topic, future in futures.items():
        try:
            future.result()
            print(f"topic {topic} created")
        except Exception as e:
            print(f"topic {topic} failed to create: {e}")
            raise


async def produce(topic_name):
    """
    produce data into kafka topic
    """
    p = Producer({"bootstrap.servers": BROKER_URL})
    count = 0
    while True:
       p.produce(topic_name, f"message: {count}".encode("utf-8"))
       count += 1
       await asyncio.sleep(0.5)


async def consume(topic_name):
    """
    pull data from kafka topic
    """
    c = Consumer({"bootstrap.servers": BROKER_URL, "group.id": "0"})
    c.subscribe([topic_name])

    while True:
        message = c.poll(1.0)
        if message is None:
            print("NO message received!")
        elif message.error() is not None:
            print(f"Message had an error {message.error()}")
        else:
            print(f"key: {message.key()}, value: {message.value()}")

        await asyncio.sleep(2.5)


async def produce_and_consume(topic_name):
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


def main():
    """
    create topic, then run producer and consumer
    """
    client = AdminClient({"bootstrap.servers": BROKER_URL})

    if not topic_exists(client, TOPIC_NAME):
        create_topic(client, TOPIC_NAME)

    try:
        asyncio.run(produce_and_consume(TOPIC_NAME))
    except KeyboardInterrupt as e:
        print("shutting down")


if __name__ == "__main__":
    main()
