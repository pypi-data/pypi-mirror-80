import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.models.result_field import ResultField


class ResultFieldsAPI(BaseAPI):
    """Result Fields API. http://docs.gurock.com/testrail-api2/reference-results-fields"""
    def get_result_fields(self) -> typing.List[ResultField]:
        """http://docs.gurock.com/testrail-api2/reference-results-fields#get_result_fields"""
        result_fields_data = self._request('get_result_fields')
        return [ResultField.from_json(result_fields) for result_fields in result_fields_data]
