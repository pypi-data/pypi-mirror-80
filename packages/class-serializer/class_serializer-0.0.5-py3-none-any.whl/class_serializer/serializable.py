import json
from abc import ABC
from typing import Iterable, Tuple, cast

_serializable_field_properties = '_serializable_field_properties'


class _SerializableFieldProperties:
    def __init__(self, json_key: str):
        self.__json_key = json_key

    @property
    def json_key(self) -> str:
        return self.__json_key


class Serializable(ABC):
    def __iter__(self) -> Iterable[Tuple[str, any]]:
        mangle_prefix = '_%s' % type(self).__name__
        for name in dir(self):
            member = getattr(self, name)
            if not hasattr(member, _serializable_field_properties):
                continue
            serializable_field_properties = cast(
                _SerializableFieldProperties,
                getattr(member, _serializable_field_properties)
            )
            json_key = serializable_field_properties.json_key
            if not json_key:
                unmangled_name = name if not name.startswith(mangle_prefix) \
                    else name.replace(mangle_prefix, '', 1)
                json_key = unmangled_name
            yield json_key, member()

    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: dict(o), separators=(',', ':'))


def serialize(json_key: str = None):
    def inner_serialize(fn):
        serializable_field_properties = _SerializableFieldProperties(
            json_key
        )
        setattr(fn, _serializable_field_properties, serializable_field_properties)
        return fn

    return inner_serialize
