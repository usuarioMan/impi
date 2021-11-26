from json import dumps
from aiokafka import AIOKafkaProducer

from app.logger import logger


class ProducerOne:
    """
    Producer singleton.
    """
    __client: "ProducerOne" = None
    DOWN = 0
    UP = 1

    def __new__(cls, connection_string=None, io_loop=None) -> "ProducerOne":
        if cls.__client is None:
            cls.__client = object.__new__(cls)
            # noinspection PyTypeHints
            cls.__client.producer: AIOKafkaProducer = AIOKafkaProducer(
                bootstrap_servers='localhost:9092',
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )
            cls.__client.status = cls.DOWN

        return cls.__client

    async def start_producer(self):
        if self.status == self.DOWN:
            logger.info("Starting ProducerOne ...")
            await self.producer.start()
            logger.info("ProducerOne started.")
            self.status = self.UP

        else:
            logger.warning("ProducerOne is already running.")
            return

    async def send_message(self, topic: str, value: str) -> None:
        await self.producer.send_and_wait(topic, value)
        return

    async def stop_producer(self):
        await self.producer.stop()
