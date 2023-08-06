from __future__ import annotations

import enum

from best_testrail_client.custom_types import JsonData

if False:  # TYPE_CHECKING
    import typing

    BaseModelType = typing.TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    def __init__(self, **kwargs: typing.Any):
        pass

    @classmethod
    def from_json(cls: typing.Type[BaseModelType], data_json: JsonData) -> BaseModelType:
        data = dict(data_json)
        for key, value in data_json.items():
            if 'custom_' in key:
                data.setdefault('custom', {})[key] = value
                data.pop(key)
            elif key not in cls.__annotations__:
                data.pop(key)
        return cls(**data)

    @classmethod
    def cast_value(cls, value: typing.Any, include_none: bool = False) -> typing.Any:
        if isinstance(value, enum.Enum):
            return value.value
        elif isinstance(value, BaseModel):
            return value.to_json()
        elif isinstance(value, list):
            return [
                cls.cast_value(list_value, include_none) for list_value in value
            ]
        else:
            return value

    def to_json(self, include_none: bool = True) -> JsonData:
        data_json = {}
        for key, value in self.__dict__.items():
            if value is None and not include_none:
                continue
            if key == 'custom':
                data_json.update(self._get_custom_values(value=value, include_none=include_none))
            else:
                data_json[key] = self.cast_value(value, include_none)
        return data_json

    def _get_custom_values(self, value: typing.Optional[JsonData], include_none: bool) -> JsonData:
        custom_dict: JsonData = {}
        if value is None:
            return custom_dict
        for custom_key, custom_value in value.items():
            custom_dict[custom_key] = self.cast_value(custom_value, include_none)
        return custom_dict
