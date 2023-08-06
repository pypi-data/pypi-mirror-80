import dataclasses

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Status(BaseModel):
    color_bright: int
    color_dark: int
    color_medium: int
    id: ModelID  # noqa: A003, VNE003
    is_final: bool
    is_system: bool
    is_untested: bool
    label: str
    name: str
