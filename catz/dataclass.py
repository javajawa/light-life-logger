#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

import dataclasses
import datetime
import enum

from typing import Any, Dict, _GenericAlias, List, Optional, Tuple, Type, Union


JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


@dataclasses.dataclass
class CatZ:
    day: datetime.date = dataclasses.field(default_factory=datetime.date.today)


    @classmethod
    def new(cls: Type[CatZ]) -> CatZ:
        return cls()

    @classmethod
    def from_json(cls: Type[CatZ], json: Dict[str, JSON]) -> CatZ:
        data: Dict[str, Any] = {}

        for _field in dataclasses.fields(cls):
            if _field.name not in json:
                continue

            data[_field.name] = cls.internalise_value(_field.type, json[_field.name])

        return cls(**data)

    @classmethod
    def internalise_value(cls: Type[CatZ], field_type: Type[Any], value: JSON):
        ret: Any = ...
        msg: str = "Unexpected type %d for field of type %s"

        if field_type == str:
            assert isinstance(value, str), msg % (str(type(value)), field_type)
            ret = str(value)

        elif field_type == int:
            assert isinstance(value, (int, str)), msg % (str(type(value)), field_type)
            ret = int(value)

        elif field_type == float:
            assert isinstance(value, (int, float, str)), msg % (str(type(value)), field_type)
            ret = float(value)

        elif field_type == 'datetime.date':
            assert isinstance(value, str), msg % (str(type(value)), field_type)
            ret = datetime.date.fromisoformat(value)

        elif isinstance(field_type, _GenericAlias):
            ret = cls.internalise_generic(field_type, value, msg)

        elif callable(field_type) and issubclass(field_type, enum.Enum):
            assert isinstance(value, str), msg % (str(type(value)), field_type)

            return cls.enum_value(field_type, value)

        else:
            raise ValueError("Unable to cast to " + field_type)

        return ret

    @classmethod
    def internalise_generic(cls: Type[CatZ], field_type: Type[Any], value: JSON, msg: str):
        ret = ...
        subs = field_type.__args__

        if field_type.__origin__ == list:
            assert isinstance(value, list), msg % (str(type(value)), field_type)

            ret = list(value)
            ret = [v for v in [cls.internalise_value(subs[0], v) for v in ret] if v]

        elif field_type.__origin__ == set:
            assert isinstance(value, list), msg % (str(type(value)), field_type)

            ret = list(value)
            ret = {v for v in {cls.internalise_value(subs[0], v) for v in ret} if v}

        elif field_type.__origin__ == dict:
            assert isinstance(value, (dict, list)), msg % (str(type(value)), field_type)

            if isinstance(value, list):
                ret = {v: 1 for v in {cls.internalise_value(subs[0], v) for v in value} if v}
            else:
                ret = {
                    cls.internalise_value(subs[0], k): cls.internalise_value(subs[1], value[k])
                    for k in value
                }

        else:
            raise ValueError("Unknown Generic %s" % field_type.__origin__)

        return ret

    @classmethod
    def enum_value(cls: Type[CatZ], enum_type: Type[enum.Enum], value: str) -> Optional[enum.Enum]:
        if value in enum_type.__members__:
            return enum_type.__members__[value]

        try:
            return enum_type(value)
        except ValueError:
            return None

    def to_json(self: CatZ) -> JSON:
        return {
            field.name: self.clean_value(getattr(self, field.name))
            for field in dataclasses.fields(self)
        }

    def clean_value(self: CatZ, value) -> JSON:
        if isinstance(value, (str, int, float)):
            return value

        if isinstance(value, enum.Enum):
            return value.name

        if isinstance(value, datetime.date):
            return value.isoformat()

        if isinstance(value, (set, list)):
            return [self.clean_value(v) for v in value]

        if isinstance(value, dict):
            return {
                k: v for (k, v) in {
                    self.clean_value(k): self.clean_value(v)
                    for (k, v) in value.items()
                }.items() if v
            }

        raise ValueError("Unhandled type " + str(type(value)))


_FIELDS: List[Tuple[str, Type[Any], dataclasses.field]] = []


def registerfield(name: str, _type: Type[Any], _default):
    if callable(_default):
        _field = dataclasses.field(default_factory=_default)
    else:
        _field = dataclasses.field(default=_default)

    _FIELDS.append((name, _type, _field))

    return lambda x: x


def get_data_object() -> Type[CatZ]:
    return dataclasses.make_dataclass('CatZImpl', _FIELDS, bases=(CatZ,))
