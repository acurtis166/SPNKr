"""Base Models."""

from dataclasses import dataclass
import datetime as dt
from typing import Type

from dataclass_wizard import JSONSerializable, LoadMixin, json_field
from dataclass_wizard.enums import LetterCase
import dateutil.parser
import orjson

from haloinfinite import util


def load_to_datetime(o: str, base_type: dt.datetime) -> dt.datetime:
    return dateutil.parser.isoparse(o)

def load_to_timedelta(o: str, base_type: dt.timedelta):
    return util.parse_iso_duration(o)
    
def parse_json(cls: Type[JSONSerializable], string: str):
    return cls.from_json(string, decoder=orjson.loads)  # type: ignore


class SnakeModel(JSONSerializable, LoadMixin):
    load_to_datetime = load_to_datetime
    load_to_timedelta = load_to_timedelta

    @classmethod
    def parse_json(cls, string: str):
        return parse_json(cls, string)


class PascalModel(JSONSerializable, LoadMixin):
    load_to_datetime = load_to_datetime
    load_to_timedelta = load_to_timedelta

    @classmethod
    def parse_json(cls, string: str):
        return parse_json(cls, string)

    class Meta(JSONSerializable.Meta):
        key_transform_with_dump = LetterCase.PASCAL


class CamelModel(JSONSerializable, LoadMixin):
    load_to_datetime = load_to_datetime
    load_to_timedelta = load_to_timedelta

    @classmethod
    def parse_json(cls, string: str):
        return parse_json(cls, string)

    class Meta(JSONSerializable.Meta):
        key_transform_with_dump = LetterCase.CAMEL


@dataclass
class Date(JSONSerializable, LoadMixin):
    iso_8601_date: dt.datetime = json_field(('ISO8601Date',), all=True)

    load_to_datetime = load_to_datetime

