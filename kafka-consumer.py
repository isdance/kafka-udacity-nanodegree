import asyncio

from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic


BROKER_URL = "PLAINTEXT://localhost:9092"


async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    # Sleep for a few seconds to give the producer time to create some data
    await asyncio.sleep(2.5)

    # Action to take when there is no initial offset in offset store or the desired offset is out of range: 
    # 'smallest','earliest' - automatically reset the offset to the smallest offset, 
    # 'largest','latest' - automatically reset the offset to the largest offset, 
    # 'error' - trigger an error which is retrieved by consuming messages and checking 'message->err'.
    #  Type: enum value
    #        See: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    c = Consumer(
        {
            "bootstrap.servers": BROKER_URL,
            "group.id": "0",
            "auto.offset.reset": "earliest" # or latest
        }
    )

    # "on_assign" event happens when the Kafka broker assigns our client a partiontion to consumer from.
    # Configure the on_assign callback
    #        See: https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#confluent_kafka.Consumer.subscribe
    c.subscribe([topic_name], on_assign=on_assign)

    while True:
        message = c.poll(1.0)
        if message is None:
            print("no message received by consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            print(f"consumed message {message.key()}: {message.value()}")
        await asyncio.sleep(0.1)


def on_assign(consumer, partitions):
    """Callback for when topic assignment takes place"""
    #   Set the partition offset to the beginning on every boot.
    #        See: https://docs.confluent.io/5.0.0/clients/confluent-kafka-python/index.html?highlight=on_assign#confluent_kafka.Consumer.on_assign
    #        See: https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#confluent_kafka.TopicPartition
    for partition in partitions:
        partition.offset = OFFSET_BEGINNING # "OFFSET_BEGINNING" is a special value imported from confluent_kafka library

    # Assign the consumer the partitions
    #        See: https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#confluent_kafka.Consumer.assign
    consumer.assign(partitions)


def main():
    """Runs the exercise"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    try:
        asyncio.run(produce_consume("com.udacity.lesson2.exercise5.iterations"))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    curr_iteration = 0
    while True:
        p.produce(topic_name, f"iteration {curr_iteration}".encode("utf-8"))
        curr_iteration += 1
        await asyncio.sleep(0.1)


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


if __name__ == "__main__":
    main()
