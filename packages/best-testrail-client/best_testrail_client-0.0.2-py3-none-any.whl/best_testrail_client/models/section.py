import dataclasses
import typing

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Section(BaseModel):
    name: str
    depth: typing.Optional[int] = None
    description: typing.Optional[str] = None
    display_order: typing.Optional[int] = None
    id: typing.Optional[ModelID] = None  # noqa: A003, VNE003
    parent_id: typing.Optional[ModelID] = None
    suite_id: typing.Optional[ModelID] = None
