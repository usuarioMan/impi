from abc import ABC, abstractmethod
from types import new_class

from odmantic import AIOEngine

from db.utils import get_motor_client, check_if_database_exists


class ODMEngineInterface(ABC):
    @staticmethod
    @abstractmethod
    def create_engine():
        pass


class AIOEngineCreator:
    def __init__(self, engine_name, database_name):
        self.engine_name = engine_name
        self.database_name = database_name

    async def create(self):
        await check_if_database_exists(self.database_name)
        cls_dictionary = {
            '__init__': self.initializer,
            'create_engine': self.create_engine,
        }
        engine = new_class(self.engine_name, (ODMEngineInterface,), {}, lambda ns: ns.update(cls_dictionary))
        engine.__module__ = __name__
        return engine

    def initializer(self, database_name: str):
        self.database_name = database_name

    async def create_engine(self):
        motor_client = get_motor_client()
        engine = AIOEngine(
            motor_client=motor_client,
            database=self.database_name)
        return engine
