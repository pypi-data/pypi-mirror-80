import typing

from best_testrail_client.api.base_api import ProjectDependableAPI
from best_testrail_client.custom_types import ModelID, DeleteResult
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.run import Run


class RunsAPI(ProjectDependableAPI):
    """Runs API. http://docs.gurock.com/testrail-api2/reference-runs"""
    def get_run(self, run_id: ModelID) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#get_run"""
        run_data = self._request(f'get_run/{run_id}')
        return Run.from_json(data_json=run_data)

    def get_runs(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Run]:
        """http://docs.gurock.com/testrail-api2/reference-runs#get_runs"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        runs_data = self._request(f'get_runs/{project_id}')
        return [Run.from_json(data_json=run_data) for run_data in runs_data]

    def add_run(self, run: Run, project_id: typing.Optional[ModelID] = None) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#add_run"""
        project_id = project_id or self._project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_run_data = run.to_json(include_none=False)
        run_data = self._request(f'add_run/{project_id}', method='POST', data=new_run_data)
        return Run.from_json(data_json=run_data)

    def update_run(self, updated_run: Run) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#update_run"""
        update_run_data = updated_run.to_json(include_none=False)
        run_data = self._request(
            f'update_run/{updated_run.id}', method='POST', data=update_run_data,
        )
        return Run.from_json(data_json=run_data)

    def close_run(self, run_id: ModelID) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#close_run"""
        run_data = self._request(f'close_run/{run_id}', method='POST')
        return Run.from_json(data_json=run_data)

    def delete_run(self, run_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-runs#delete_run"""
        self._request(f'delete_run/{run_id}', method='POST')
        return True
