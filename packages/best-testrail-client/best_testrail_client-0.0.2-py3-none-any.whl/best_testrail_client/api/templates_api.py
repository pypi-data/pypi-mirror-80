import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.template import Template


class TemplatesAPI(ProjectDependableAPI):
    # Templates API  http://docs.gurock.com/testrail-api2/reference-templates
    def get_templates(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Template]:
        """http://docs.gurock.com/testrail-api2/reference-templates#get_templates"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        templates_data = self._request(f'get_templates/{project_id}')
        return [Template.from_json(template) for template in templates_data]
