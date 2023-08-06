import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.models.status import Status


class StatusesAPI(BaseAPI):
    """Statuses API. http://docs.gurock.com/testrail-api2/reference-statuses"""
    def get_statuses(self) -> typing.List[Status]:
        """http://docs.gurock.com/testrail-api2/reference-statuses#get_statuses"""
        statuses_data = self._request('get_statuses')
        return [Status.from_json(status) for status in statuses_data]
