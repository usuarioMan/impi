import asyncio
import pytest
from app.kafka.producers.producer import ProducerOne


@pytest.mark.asyncio
def test_start_producer():
    async def foo():
        producer = ProducerOne()
        await producer.start_producer()
        return producer

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    producer = loop.run_until_complete(foo())
    loop.close()

    assert producer.status == 1


@pytest.mark.asyncio
def test_send_message():
    async def foo():
        producer = ProducerOne()
        await producer.start_producer()
        await producer.send_message("my_topic", "otro mensaje")
        return producer

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    producer = loop.run_until_complete(foo())
    loop.close()

    assert producer.status == 1
