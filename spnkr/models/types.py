"""Custom types for pydantic models."""

import datetime as dt
from collections.abc import Mapping
from typing import Annotated, TypeVar

from pydantic import (
    AfterValidator,
    BeforeValidator,
    PlainSerializer,
    WrapSerializer,
)

K = TypeVar("K")
V = TypeVar("V")


class _ReadOnlyDict(Mapping[K, V]):
    """A read-only dict."""

    def __init__(self, data: Mapping[K, V]) -> None:
        self._data = data

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __len__(self) -> int:
        return self._data.__len__()

    def __iter__(self):
        return self._data.__iter__()

    def __str__(self) -> str:
        return self._data.__str__()

    def __repr__(self) -> str:
        return self._data.__repr__()


_ReadOnlyDictValidator = AfterValidator(lambda v: _ReadOnlyDict(v))
_ReadOnlyDictSerializer = PlainSerializer(lambda v: dict(v), return_type=dict)

ReadOnlyDict = Annotated[
    Mapping[K, V], _ReadOnlyDictValidator, _ReadOnlyDictSerializer
]


def _date_object_validator(value):
    if isinstance(value, dict):
        try:
            return value["ISO8601Date"]
        except KeyError:
            raise ValueError(f"Expected ISO8601Date key: {value}")
    return value


def _date_object_serializer(value: dt.datetime, nxt):
    return {"ISO8601Date": nxt(value)}


_ISO8601DateObjectValidator = BeforeValidator(_date_object_validator)
_ISO8601DateObjectSerializer = WrapSerializer(_date_object_serializer, dict)

ISO8601DateObject = Annotated[
    dt.datetime, _ISO8601DateObjectValidator, _ISO8601DateObjectSerializer
]
