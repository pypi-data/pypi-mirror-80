import json

import pytest
import requests

from best_testrail_client.client import TestRailClient


@pytest.fixture
def testrail_client():
    return TestRailClient('https://test.test.test/', 'login', 'token')


@pytest.fixture
def mocked_response(mocker):
    def _with_response(raw_data=None, data_json=None, status_code=200):

        mocked_requests = mocker.patch('best_testrail_client.api.base_api.requests.request')
        response = requests.Response()
        response._content = json.dumps(data_json).encode('utf8') if data_json else raw_data
        response.status_code = status_code

        mocked_requests.return_value = response

        return mocked_requests

    return _with_response
