import dataclasses

import typing

from best_testrail_client.custom_types import ModelID, TimeStamp, JsonData
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Run(BaseModel):
    name: str
    include_all: bool
    assignedto_id: typing.Optional[ModelID] = None
    blocked_count: typing.Optional[int] = None
    completed_on: typing.Optional[TimeStamp] = None
    config: typing.Optional[str] = None
    config_ids: typing.Optional[typing.List[ModelID]] = None
    created_by: typing.Optional[ModelID] = None
    case_ids: typing.Optional[typing.List[ModelID]] = None
    created_on: typing.Optional[TimeStamp] = None
    description: typing.Optional[str] = None
    failed_count: typing.Optional[int] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    is_completed: typing.Optional[bool] = None
    milestone_id: typing.Optional[ModelID] = None
    plan_id: typing.Optional[ModelID] = None
    passed_count: typing.Optional[int] = None
    project_id: typing.Optional[ModelID] = None
    retest_count: typing.Optional[int] = None
    suite_id: typing.Optional[ModelID] = None
    untested_count: typing.Optional[int] = None
    url: typing.Optional[str] = None
    updated_on: typing.Optional[TimeStamp] = None
    refs: typing.Optional[str] = None
    custom: typing.Optional[JsonData] = None
