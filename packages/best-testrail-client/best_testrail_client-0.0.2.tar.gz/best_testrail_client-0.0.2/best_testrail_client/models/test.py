import dataclasses

import typing

from best_testrail_client.custom_types import ModelID, TimeSpan, JsonData
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Test(BaseModel):
    assignedto_id: typing.Optional[ModelID] = None
    case_id: typing.Optional[ModelID] = None
    estimate: typing.Optional[TimeSpan] = None
    estimate_forecast: typing.Optional[TimeSpan] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    milestone_id: typing.Optional[ModelID] = None
    priority_id: typing.Optional[ModelID] = None
    refs: typing.Optional[str] = None
    run_id: typing.Optional[ModelID] = None
    status_id: typing.Optional[ModelID] = None
    template_id: typing.Optional[ModelID] = None
    title: typing.Optional[str] = None
    type_id: typing.Optional[ModelID] = None
    custom: typing.Optional[JsonData] = None
