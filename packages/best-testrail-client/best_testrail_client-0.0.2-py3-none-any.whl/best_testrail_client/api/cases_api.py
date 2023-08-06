import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID, CaseFilter, JsonData, DeleteResult
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.case import Case
from best_testrail_client.utils import convert_list_to_filter


class CasesAPI(ProjectDependableAPI):
    """Cases API. http://docs.gurock.com/testrail-api2/reference-cases"""
    def get_case(self, case_id: ModelID) -> Case:
        """http://docs.gurock.com/testrail-api2/reference-cases#get_case"""
        case_data = self._request(f'get_case/{case_id}')
        return Case.from_json(case_data)

    def get_cases(
        self,
        project_id: typing.Optional[ModelID] = None,
        suite_id: typing.Optional[ModelID] = None,
        section_id: typing.Optional[ModelID] = None,
        filters: typing.Optional[CaseFilter] = None,
    ) -> typing.List[Case]:
        """http://docs.gurock.com/testrail-api2/reference-cases#get_case"""
        params: JsonData = {}
        if filters is not None:
            params = {key: value for key, value in filters.items()}
            params['created_by'] = convert_list_to_filter(values_list=filters.get('created_by'))
            params['milestone_id'] = convert_list_to_filter(values_list=filters.get('milestone_id'))
            params['priority_id'] = convert_list_to_filter(values_list=filters.get('priority_id'))
            params['template_id'] = convert_list_to_filter(values_list=filters.get('template_id'))
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        params['suite_id'] = suite_id
        params['section_id'] = section_id
        cases_data = self._request(f'get_cases/{project_id}', params=params)
        return [Case.from_json(case_data) for case_data in cases_data]

    def add_case(self, section_id: ModelID, case: Case) -> Case:
        """http://docs.gurock.com/testrail-api2/reference-cases#add_case"""
        new_case_data = case.to_json(include_none=False)
        created_case_data = self._request(
            f'add_case/{section_id}', method='POST', data=new_case_data,
        )
        return Case.from_json(created_case_data)

    def update_case(self, case_id: ModelID, case: Case) -> Case:
        """http://docs.gurock.com/testrail-api2/reference-cases#update_case"""
        new_case_data = case.to_json(include_none=False)
        created_case_data = self._request(
            f'update_case/{case_id}', method='POST', data=new_case_data,
        )
        return Case.from_json(created_case_data)

    def delete_case(self, case_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-cases#delete_case"""
        self._request(f'delete_case/{case_id}', method='POST')
        return True
