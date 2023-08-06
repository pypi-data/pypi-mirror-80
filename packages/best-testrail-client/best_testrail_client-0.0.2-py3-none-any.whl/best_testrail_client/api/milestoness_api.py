import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID, DeleteResult
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.milestone import Milestone


class MilestonesAPI(ProjectDependableAPI):
    """Milestones API. http://docs.gurock.com/testrail-api2/reference-milestones"""
    def get_milestone(self, milestone_id: ModelID) -> Milestone:
        """http://docs.gurock.com/testrail-api2/reference-milestones#get_milestone"""
        milestone_data = self._request(f'get_milestone/{milestone_id}')
        return Milestone.from_json(data_json=milestone_data)

    def get_milestones(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Milestone]:
        """http://docs.gurock.com/testrail-api2/reference-milestones#get_milestones"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        milestones_data = self._request(f'get_milestones/{project_id}')
        return [
            Milestone.from_json(data_json=milestone_data) for milestone_data in milestones_data
        ]

    def add_milestone(
        self, milestone: Milestone, project_id: typing.Optional[ModelID] = None,
    ) -> Milestone:
        """http://docs.gurock.com/testrail-api2/reference-milestones#add_milestone"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_milestone_data = milestone.to_json(include_none=False)
        milestone_data = self._request(
            f'add_milestone/{project_id}', method='POST', data=new_milestone_data,
        )
        return Milestone.from_json(data_json=milestone_data)

    def update_milestone(self, milestone: Milestone) -> Milestone:
        """http://docs.gurock.com/testrail-api2/reference-milestones#update_milestone"""
        updated_milestone_data = milestone.to_json(include_none=False)
        milestone_data = self._request(
            f'update_milestone/{milestone.id}', method='POST', data=updated_milestone_data,
        )
        return Milestone.from_json(data_json=milestone_data)

    def delete_milestone(self, milestone_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-milestones#delete_milestone"""
        self._request(f'delete_milestone/{milestone_id}', method='POST')
        return True
