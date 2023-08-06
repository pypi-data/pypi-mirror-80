import dataclasses

from best_testrail_client.custom_types import ModelID, TimeStamp
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Attachment(BaseModel):
    id: ModelID  # noqa: A003, VNE003
    name: str
    filename: str
    size: int
    created_on: TimeStamp
    project_id: ModelID
    case_id: ModelID
    test_change_id: ModelID
    user_id: ModelID
