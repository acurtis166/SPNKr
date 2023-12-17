"""Custom types for pydantic models."""

from collections.abc import Mapping
from typing import Annotated, TypeVar

from pydantic import AfterValidator, PlainSerializer

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
