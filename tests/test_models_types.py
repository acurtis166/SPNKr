"""Test the spnkr.models.types module."""

import pytest
from pydantic import BaseModel

from spnkr.models import types


def test_read_only_dict_getitem():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert rod["foo"] == "bar"


def test_read_only_dict_len():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert len(rod) == 1


def test_read_only_dict_iter():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert list(rod) == ["foo"]


def test_read_only_dict_str():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert str(rod) == "{'foo': 'bar'}"


def test_read_only_dict_repr():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert repr(rod) == "{'foo': 'bar'}"


def test_read_only_dict_setitem():
    rod = types._ReadOnlyDict({"foo": "bar"})
    with pytest.raises(TypeError):
        rod["foo"] = "baz"  # type: ignore


def test_read_only_dict_delitem():
    rod = types._ReadOnlyDict({"foo": "bar"})
    with pytest.raises(TypeError):
        del rod["foo"]  # type: ignore


def test_read_only_dict_to_dict():
    rod = types._ReadOnlyDict({"foo": "bar"})
    assert dict(rod) == {"foo": "bar"}


def test_read_only_dict_annotation():
    class Foo(BaseModel):
        bar: types.ReadOnlyDict[str, str]

    foo = Foo(bar={"foo": "bar"})
    assert isinstance(foo.bar, types._ReadOnlyDict)
    assert foo.bar["foo"] == "bar"
    assert foo.model_dump() == {"bar": {"foo": "bar"}}
    assert foo.model_dump_json() == '{"bar":{"foo":"bar"}}'
