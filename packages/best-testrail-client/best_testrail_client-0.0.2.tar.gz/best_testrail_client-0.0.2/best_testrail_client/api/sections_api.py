import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID, DeleteResult
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.section import Section


class SectionsAPI(ProjectDependableAPI):
    """Sections API. http://docs.gurock.com/testrail-api2/reference-sections"""
    def get_section(self, section_id: ModelID) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#get_section"""
        section_data = self._request(f'get_section/{section_id}')
        return Section.from_json(section_data)

    def get_sections(
        self,
        project_id: typing.Optional[ModelID] = None, suite_id: typing.Optional[ModelID] = None,
    ) -> typing.List[Section]:
        """http://docs.gurock.com/testrail-api2/reference-sections#get_sections"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        sections_data = self._request(f'get_sections/{project_id}', params={'suite_id': suite_id})
        return [Section.from_json(section) for section in sections_data]

    def add_section(self, section: Section, project_id: typing.Optional[ModelID] = None) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#add_section"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_section_data = section.to_json(include_none=False)
        section_data = self._request(
            f'add_section/{project_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def update_section(
        self, section_id: ModelID, name: str, description: typing.Optional[str] = None,
    ) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#update_section"""
        new_section_data = {'name': name}
        if description is not None:
            new_section_data['description'] = description
        section_data = self._request(
            f'update_section/{section_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def delete_section(self, section_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-sections#delete_section"""
        self._request(f'delete_section/{section_id}', method='POST')
        return True
