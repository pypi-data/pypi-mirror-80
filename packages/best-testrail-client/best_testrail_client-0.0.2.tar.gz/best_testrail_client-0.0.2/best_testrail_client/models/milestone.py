import dataclasses

import typing

from best_testrail_client.custom_types import ModelID, TimeStamp
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Milestone(BaseModel):
    name: str
    completed_on: typing.Optional[TimeStamp] = None
    description: typing.Optional[str] = None
    due_on: typing.Optional[TimeStamp] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    is_completed: typing.Optional[bool] = None
    is_started: typing.Optional[bool] = None
    milestones: typing.Optional[typing.List[ModelID]] = None
    parent_id: typing.Optional[ModelID] = None
    project_id: typing.Optional[ModelID] = None
    start_on: typing.Optional[TimeStamp] = None
    started_on: typing.Optional[TimeStamp] = None
    url: typing.Optional[str] = None
