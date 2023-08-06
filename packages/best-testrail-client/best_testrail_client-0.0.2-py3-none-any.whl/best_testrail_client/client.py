from __future__ import annotations

from best_testrail_client.api.attachments_api import AttachmentsAPI
from best_testrail_client.api.case_types_api import CaseTypesAPI
from best_testrail_client.api.cases_api import CasesAPI
from best_testrail_client.api.configurations_api import ConfigurationsAPI
from best_testrail_client.api.milestoness_api import MilestonesAPI
from best_testrail_client.api.priorities_api import PrioritiesAPI
from best_testrail_client.api.result_fields_api import ResultFieldsAPI
from best_testrail_client.api.results_api import ResultsAPI
from best_testrail_client.api.runs_api import RunsAPI
from best_testrail_client.api.sections_api import SectionsAPI
from best_testrail_client.api.statuses_api import StatusesAPI
from best_testrail_client.api.templates_api import TemplatesAPI
from best_testrail_client.api.tests_api import TestsAPI
from best_testrail_client.api.users_api import UsersAPI
from best_testrail_client.custom_types import ModelID


class TestRailClient:
    """http://docs.gurock.com/testrail-api2/start"""
    def __init__(self, testrail_url: str, login: str, token: str):

        self.attachments = AttachmentsAPI(testrail_url, login, token)
        self.cases = CasesAPI(testrail_url, login, token)
        self.case_types = CaseTypesAPI(testrail_url, login, token)
        self.configurations = ConfigurationsAPI(testrail_url, login, token)
        self.milestones = MilestonesAPI(testrail_url, login, token)
        self.priorities = PrioritiesAPI(testrail_url, login, token)
        self.results = ResultsAPI(testrail_url, login, token)
        self.result_fields = ResultFieldsAPI(testrail_url, login, token)
        self.runs = RunsAPI(testrail_url, login, token)
        self.sections = SectionsAPI(testrail_url, login, token)
        self.statuses = StatusesAPI(testrail_url, login, token)
        self.templates = TemplatesAPI(testrail_url, login, token)
        self.tests = TestsAPI(testrail_url, login, token)
        self.users = UsersAPI(testrail_url, login, token)

    # Custom methods
    def set_project_id(self, project_id: ModelID) -> TestRailClient:
        self.cases.set_project_id(project_id=project_id)
        self.configurations.set_project_id(project_id=project_id)
        self.milestones.set_project_id(project_id=project_id)
        self.runs.set_project_id(project_id=project_id)
        self.sections.set_project_id(project_id=project_id)
        self.templates.set_project_id(project_id=project_id)
        return self
