import asyncio
from time import sleep
from json import dumps
from kafka import KafkaProducer
from asyncio import sleep
import schedule
import time


def job():
    return True


# schedule.every(5).seconds.do(job)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


async def loop_infinito():
    for i in range(1_000_000_000):
        print("PRODUCIENDO!")
        booliano = job()
        producer.send('topic_test', value=booliano)
        await sleep(10)
