import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID, DeleteResult
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.configuration import Configuration, GroupConfig


class ConfigurationsAPI(ProjectDependableAPI):
    """Configurations API. http://docs.gurock.com/testrail-api2/reference-configs"""
    def get_configs(
        self, project_id: typing.Optional[ModelID] = None,
    ) -> typing.List[Configuration]:
        """http://docs.gurock.com/testrail-api2/reference-configs#get_configs"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        configurations_data = self._request(f'get_configs/{project_id}')
        return [
            Configuration.from_json(configuration_data)
            for configuration_data in configurations_data
        ]

    def add_config_group(
        self, name: str, project_id: typing.Optional[ModelID] = None,
    ) -> Configuration:
        """http://docs.gurock.com/testrail-api2/reference-configs#add_config_group"""
        new_config_group_data = {'name': name}
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        config_group_data = self._request(
            f'add_config_group/{project_id}', method='POST', data=new_config_group_data,
        )
        return Configuration.from_json(config_group_data)

    def add_config(self, name: str, config_group_id: ModelID) -> GroupConfig:
        """http://docs.gurock.com/testrail-api2/reference-configs#add_config"""
        new_config_data = {'name': name}
        config_group_data = self._request(
            f'add_config/{config_group_id}', method='POST', data=new_config_data,
        )
        return GroupConfig.from_json(config_group_data)

    def update_config_group(self, name: str, config_group_id: ModelID) -> Configuration:
        """http://docs.gurock.com/testrail-api2/reference-configs#update_config_group"""
        new_config_group_data = {'name': name}
        config_group_data = self._request(
            f'update_config_group/{config_group_id}', method='POST', data=new_config_group_data,
        )
        return Configuration.from_json(config_group_data)

    def update_config(self, name: str, config_id: ModelID) -> GroupConfig:
        """http://docs.gurock.com/testrail-api2/reference-configs#update_config"""
        new_config_data = {'name': name}
        config_data = self._request(
            f'update_config/{config_id}', method='POST', data=new_config_data,
        )
        return GroupConfig.from_json(config_data)

    def delete_config_group(self, config_group_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-configs#delete_config_group"""
        self._request(f'delete_config_group/{config_group_id}', method='POST')
        return True

    def delete_config(self, config_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-configs#delete_config"""
        self._request(f'delete_config/{config_id}', method='POST')
        return True
