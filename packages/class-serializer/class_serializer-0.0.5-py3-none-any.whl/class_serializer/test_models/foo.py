from typing import List

from src.class_serializer.serializable import serialize, Serializable
from src.class_serializer.test_models.bar import Bar


class Foo(Serializable):
    def __init__(
            self,
            a_str: str,
            a_str_with_custom_key: str,
            bar: Bar,
            bars: List[Bar]
    ):
        self.__a_str = a_str
        self.__a_str_with_custom_key = a_str_with_custom_key
        self.__bar = bar
        self.__bars = bars

    @serialize()
    def a_str_without_custom_key(self) -> str:
        return self.__a_str

    @serialize(json_key='custom_key')
    def a_str_with_custom_key(self) -> str:
        return self.__a_str

    @serialize()
    def bar(self) -> Bar:
        return self.__bar

    @serialize()
    def bars(self) -> List[Bar]:
        return self.__bars
