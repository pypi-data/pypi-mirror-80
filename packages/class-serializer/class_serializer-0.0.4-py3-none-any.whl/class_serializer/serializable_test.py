import json
from unittest import TestCase

from src.class_serializer import Serializable


class FlatClass(Serializable):
    def __init__(
            self,
            a_str: str,
            an_int: int,
            a_float: float,
            a_bool: bool
    ):
        self.__a_str = a_str
        self.__an_int = an_int
        self.__a_float = a_float
        self.__a_bool = a_bool

    @property
    def a_str(self) -> str:
        return self.__a_str

    @property
    def an_int(self) -> int:
        return self.__an_int

    @property
    def a_float(self) -> float:
        return self.__a_float

    @property
    def a_bool(self) -> bool:
        return self.__a_bool


class SerializableTest(TestCase):

    def test_flat_class(self):
        flat_thing = FlatClass('foo', 1, 2.0, False)
        serialized = flat_thing.serialize()
        as_dict = json.loads(serialized)
        self.assertEqual('foo', as_dict['a_str'])
        self.assertEqual(1, as_dict['an_int'])
        self.assertEqual(2.0, as_dict['a_float'])
        self.assertEqual(False, as_dict['a_bool'])
