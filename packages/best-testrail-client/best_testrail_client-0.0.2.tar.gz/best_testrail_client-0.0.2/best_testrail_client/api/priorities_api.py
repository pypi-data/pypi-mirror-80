import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.models.priority import Priority


class PrioritiesAPI(BaseAPI):
    """Priorities API. http://docs.gurock.com/testrail-api2/reference-priorities"""
    def get_priorities(self) -> typing.List[Priority]:
        """http://docs.gurock.com/testrail-api2/reference-priorities#get_priorities"""
        priorities_data = self._request('get_priorities')
        return [Priority.from_json(priority) for priority in priorities_data]
