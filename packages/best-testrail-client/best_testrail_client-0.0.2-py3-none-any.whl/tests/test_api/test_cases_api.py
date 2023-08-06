import pytest

from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.case import Case


def test_get_case(testrail_client, mocked_response, case_data, case):
    mocked_response(data_json=case_data)

    api_case = testrail_client.cases.get_case(case_id=1)

    assert api_case == case


def test_get_cases_with_provided_project(
    testrail_client, mocked_response, case_data, case,
):
    mocked_response(data_json=[case_data])

    api_cases = testrail_client.cases.get_cases(project_id=1)

    assert len(api_cases) == 1
    assert api_cases[0] == case


def test_get_cases_with_set_project(
    testrail_client, mocked_response, case_data, case,
):
    mocked_response(data_json=[case_data])
    testrail_client.set_project_id(project_id=1)

    api_cases = testrail_client.cases.get_cases(filters={})

    assert len(api_cases) == 1
    assert api_cases[0] == case


def test_get_cases_raises(
    testrail_client, mocked_response, case_data, case,
):
    mocked_response(data_json=[case_data])

    with pytest.raises(TestRailException):
        testrail_client.cases.get_cases()


def test_add_case(testrail_client, mocked_response):
    expected_case = Case(id=1, title='Test Case')
    mocked_response(data_json=expected_case.to_json())

    api_case = testrail_client.cases.add_case(section_id=1, case=expected_case)

    assert api_case == expected_case


def test_update_case(testrail_client, mocked_response):
    expected_case = Case(id=1, title='Test Case')
    mocked_response(data_json=expected_case.to_json())

    api_case = testrail_client.cases.update_case(case_id=1, case=expected_case)

    assert api_case == expected_case


def test_delete_case(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.cases.delete_case(case_id=1)

    assert response is True
