import dataclasses

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Priority(BaseModel):
    id: ModelID  # noqa: A003, VNE003
    is_default: bool
    name: str
    priority: int
    short_name: str
