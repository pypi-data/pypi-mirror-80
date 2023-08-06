import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.test import Test


class TestsAPI(BaseAPI):
    """http://docs.gurock.com/testrail-api2/reference-tests"""
    def get_test(self, test_id: ModelID) -> Test:
        """http://docs.gurock.com/testrail-api2/reference-tests#get_test"""
        test_data = self._request(f'get_test/{test_id}')
        return Test.from_json(test_data)

    def get_tests(self, run_id: ModelID) -> typing.List[Test]:
        """http://docs.gurock.com/testrail-api2/reference-tests#get_tests"""
        tests_data = self._request(f'get_tests/{run_id}')
        return [Test.from_json(test_data) for test_data in tests_data]
