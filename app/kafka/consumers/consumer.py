from kafka import KafkaConsumer
from json import loads
from asyncio import sleep

from aiokafka import AIOKafkaConsumer
import asyncio


async def consume():
    consumer = AIOKafkaConsumer(
        'my_topic', 'my_other_topic',
        bootstrap_servers='localhost:9092',
        group_id="my-group")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


asyncio.run(consume())

#
# async def consumerme():
#     consumer = KafkaConsumer(
#         'topic_test',
#         bootstrap_servers=['localhost:9092'],
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         group_id='my-group-id',
#         value_deserializer=lambda x: loads(x.decode('utf-8'))
#     )
#     for event in consumer:
#         event_data = event.value
#         print(event_data)
#         await sleep(2)
