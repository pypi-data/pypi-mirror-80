from typing import List, Dict

from src.class_serializer.serializable import serialize, Serializable
from src.class_serializer.test_models.bar import Bar


class Foo(Serializable):
    def __init__(
            self,
            a_str: str,
            a_str_with_custom_key: str,
            bar: Bar,
            bars: List[Bar],
            dict_of_bars: Dict[str, Bar]
    ):
        self.__a_str = a_str
        self.__a_str_with_custom_key = a_str_with_custom_key
        self.__bar = bar
        self.__bars = bars
        self.__dict_of_bars = dict_of_bars

    @serialize()
    def a_str(self) -> str:
        return self.__a_str

    @serialize(json_key='custom_key')
    def a_str_with_custom_key(self) -> str:
        return self.__a_str_with_custom_key

    @serialize()
    def bar(self) -> Bar:
        return self.__bar

    @serialize()
    def bars(self) -> List[Bar]:
        return self.__bars

    @serialize()
    def dict_of_bars(self) -> Dict[str, Bar]:
        return self.__dict_of_bars
