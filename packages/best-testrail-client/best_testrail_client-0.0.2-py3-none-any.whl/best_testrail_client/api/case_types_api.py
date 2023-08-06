import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.models.case_type import CaseType


class CaseTypesAPI(BaseAPI):
    """Case Types API. http://docs.gurock.com/testrail-api2/reference-cases-types"""
    def get_case_types(self) -> typing.List[CaseType]:
        case_types_data = self._request('get_case_types')
        return [CaseType.from_json(case_type) for case_type in case_types_data]
