import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.custom_types import ModelID, CreatedFilters, StatusFilters, JsonData
from best_testrail_client.models.result import Result
from best_testrail_client.utils import convert_list_to_filter


class ResultsAPI(BaseAPI):
    """Results API. http://docs.gurock.com/testrail-api2/reference-results"""
    def get_results(
        self,
        test_id: ModelID,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        status_ids: typing.Optional[typing.List[int]] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results"""
        status = ','.join(str(status) for status in status_ids) if status_ids is not None else ''
        filters = {
            'limit': limit,
            'offset': offset,
            'status_id': status,
        }
        results_data = self._request(f'get_results/{test_id}', params=filters)
        return [Result.from_json(result_data) for result_data in results_data]

    def get_results_for_case(
        self,
        run_id: ModelID,
        case_id: ModelID,
        filters: typing.Optional[StatusFilters] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results_for_case"""
        params: JsonData = {}
        if filters is not None:
            params = {
                'limit': filters.get('limit'),
                'offset': filters.get('offset'),
                'status_id': convert_list_to_filter(values_list=filters.get('status_ids')),
            }
        results_data = self._request(f'get_results_for_case/{run_id}/{case_id}', params=params)
        return [Result.from_json(result_data) for result_data in results_data]

    def get_results_for_run(
        self,
        run_id: ModelID,
        filters: typing.Optional[CreatedFilters] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results_for_run"""
        params: JsonData = {}
        if filters is not None:
            params = {
                'created_after': filters.get('created_after'),
                'created_before': filters.get('created_before'),
                'created_by': convert_list_to_filter(values_list=filters.get('created_by')),
                'limit': filters.get('limit'),
                'offset': filters.get('offset'),
                'status_id': convert_list_to_filter(values_list=filters.get('status_ids')),
            }
        results_data = self._request(f'get_results_for_run/{run_id}', params=params)
        return [Result.from_json(result_data) for result_data in results_data]

    def add_result(self, test_id: ModelID, result: Result) -> Result:
        """http://docs.gurock.com/testrail-api2/reference-results#add_result"""
        new_result_data = result.to_json(include_none=False)
        result_data = self._request(f'add_result/{test_id}', method='POST', data=new_result_data)
        return Result.from_json(data_json=result_data)

    def add_result_for_case(self, run_id: ModelID, case_id: ModelID, result: Result) -> Result:
        """http://docs.gurock.com/testrail-api2/reference-results#add_result_for_case"""
        new_result_data = result.to_json(include_none=False)
        result_data = self._request(
            f'add_result_for_case/{run_id}/{case_id}', method='POST', data=new_result_data,
        )
        return Result.from_json(data_json=result_data)

    def add_results(self, run_id: ModelID, results: typing.List[Result]) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#add_results"""
        new_results_data = {
            'results': [result.to_json(include_none=False) for result in results],
        }
        results_data = self._request(
            f'add_results/{run_id}', method='POST', data=new_results_data,
        )
        return [Result.from_json(data_json=result_data) for result_data in results_data]

    def add_results_for_cases(
        self, run_id: ModelID, results: typing.List[Result],
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#add_results_for_cases"""
        new_results_data = {
            'results': [result.to_json(include_none=False) for result in results],
        }
        results_data = self._request(
            f'add_results_for_cases/{run_id}', method='POST', data=new_results_data,
        )
        return [Result.from_json(data_json=result_data) for result_data in results_data]
