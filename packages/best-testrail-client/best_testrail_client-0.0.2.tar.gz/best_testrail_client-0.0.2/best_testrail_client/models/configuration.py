from __future__ import annotations

import dataclasses
import typing

from best_testrail_client.custom_types import ModelID, JsonData
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class GroupConfig(BaseModel):
    group_id: ModelID
    id: ModelID  # noqa: A003, VNE003
    name: str


@dataclasses.dataclass
class Configuration(BaseModel):
    configs: typing.List[GroupConfig]
    id: ModelID  # noqa: A003, VNE003
    name: str
    project_id: ModelID

    @classmethod
    def from_json(cls: typing.Type[Configuration], data_json: JsonData) -> Configuration:
        data_json = dict(data_json)
        data_json['configs'] = [
            GroupConfig(
                group_id=config['group_id'],
                id=config['id'],
                name=config['name'],
            ) for config in data_json.get('configs', [])
        ]

        new_instance = Configuration(
            **data_json,
        )

        return new_instance
