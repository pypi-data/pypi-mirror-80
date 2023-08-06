import json
from abc import ABC
from typing import Iterable, Tuple, Dict, List


class _SerializationSettings:
    def __init__(self, member_name: str, json_key: str):
        self.__member_name = member_name
        self.__json_key = json_key

    @property
    def member_name(self) -> str:
        return self.__member_name

    @property
    def json_key(self) -> str:
        return self.__json_key


_serializable_fields_by_module: Dict[str, List[_SerializationSettings]] = {}


class Serializable(ABC):
    def __iter__(self) -> Iterable[Tuple[str, any]]:
        mangle_prefix = '_%s' % type(self).__name__
        serializable_members = _serializable_fields_by_module.get(self.__module__, [])
        for serialization_settings in serializable_members:
            name = serialization_settings.member_name
            if not hasattr(self, name):
                continue
            json_key = serialization_settings.json_key
            if not json_key:
                unmangled_name = name if not name.startswith(mangle_prefix) \
                    else name.replace(mangle_prefix, '', 1)
                json_key = unmangled_name
            yield json_key, getattr(self, name)

    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: dict(o), separators=(',', ':'))


def serialize(json_key: str = None):
    def inner_serialize(f):
        _serializable_fields_by_module[f.__module__] = _serializable_fields_by_module.get(f.__module__, []) + \
                                                       [_SerializationSettings(f.__name__, json_key)]
        return property(f)

    return inner_serialize
