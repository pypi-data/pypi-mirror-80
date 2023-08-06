import json
from abc import ABC
from typing import Iterable, Tuple


class Serializable(ABC):
    def __iter__(self) -> Iterable[Tuple[str, any]]:
        for item_name, item_value in self.__class__.__dict__.items():
            if isinstance(item_value, property):
                yield item_name, getattr(self, item_name)

    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: dict(o), separators=(',', ':'))
