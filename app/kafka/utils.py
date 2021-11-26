from aiokafka import AIOKafkaProducer


async def create_raw_producer() -> AIOKafkaProducer:
    """
    It creates a new AIOKafkaProducer on 'localhost:9092'
    :return: AIOKafkaProducer
    """
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092')
    return producer
