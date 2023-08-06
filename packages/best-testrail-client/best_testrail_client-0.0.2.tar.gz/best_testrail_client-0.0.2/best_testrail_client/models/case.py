import dataclasses

import typing

from best_testrail_client.custom_types import ModelID, TimeStamp, TimeSpan, JsonData
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Case(BaseModel):
    created_by: typing.Optional[ModelID] = None
    created_on: typing.Optional[TimeStamp] = None
    display_order: typing.Optional[int] = None
    estimate: typing.Optional[TimeSpan] = None
    estimate_forecast: typing.Optional[TimeSpan] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    milestone_id: typing.Optional[ModelID] = None
    priority_id: typing.Optional[ModelID] = None
    refs: typing.Optional[str] = None
    section_id: typing.Optional[ModelID] = None
    suite_id: typing.Optional[ModelID] = None
    title: typing.Optional[str] = None
    template_id: typing.Optional[ModelID] = None
    type_id: typing.Optional[ModelID] = None
    updated_by: typing.Optional[ModelID] = None
    updated_on: typing.Optional[TimeStamp] = None
    custom: typing.Optional[JsonData] = None
