import asyncio
import pytest
from aiokafka import AIOKafkaProducer

from app.kafka.utils import create_raw_producer


@pytest.mark.asyncio
def test_create_raw_producer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    producer = loop.run_until_complete(create_raw_producer())
    loop.close()
    assert type(producer) is AIOKafkaProducer
