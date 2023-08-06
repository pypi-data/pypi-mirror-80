import dataclasses

import typing

from best_testrail_client.custom_types import ModelID, TimeStamp, JsonData, TimeSpan
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Result(BaseModel):
    status_id: typing.Optional[ModelID]
    assignedto_id: typing.Optional[ModelID] = None
    attachment_ids: typing.Optional[typing.List[ModelID]] = None
    comment: typing.Optional[str] = None
    created_by: typing.Optional[ModelID] = None
    created_on: typing.Optional[TimeStamp] = None
    custom: typing.Optional[JsonData] = None
    defects: typing.Optional[str] = None
    elapsed: typing.Optional[TimeSpan] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    test_id: typing.Optional[ModelID] = None
    case_id: typing.Optional[ModelID] = None
    version: typing.Optional[str] = None
