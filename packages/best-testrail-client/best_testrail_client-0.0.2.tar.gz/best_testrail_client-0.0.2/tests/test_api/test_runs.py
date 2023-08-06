import pytest

from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.run import Run


def test_get_run(testrail_client, mocked_response, run_data, run):
    mocked_response(data_json=run_data)

    api_run = testrail_client.runs.get_run(run_id=1)

    assert api_run == run


def test_get_runs_with_provided_project(testrail_client, mocked_response, run_data, run):
    mocked_response(data_json=[run_data])

    api_runs = testrail_client.runs.get_runs(project_id=1)

    assert api_runs[0] == run


def test_get_runs_with_set_project(testrail_client, mocked_response, run_data, run):
    mocked_response(data_json=[run_data])
    testrail_client.set_project_id(project_id=1)

    api_runs = testrail_client.runs.get_runs()

    assert api_runs[0] == run


def test_get_runs_raises(testrail_client, mocked_response, run_data, run):
    mocked_response(data_json=[run_data])

    with pytest.raises(TestRailException):
        testrail_client.runs.get_runs()


def test_add_run_with_provided_project(testrail_client, mocked_response):
    expected_run = Run(id=1, project_id=1, name='Test Run', include_all=False, case_ids=[1, 2, 3])
    mocked_response(data_json=expected_run.to_json())

    api_run = testrail_client.runs.add_run(run=expected_run, project_id=1)

    assert api_run == expected_run


def test_add_run_with_set_project(testrail_client, mocked_response):
    expected_run = Run(id=1, project_id=1, name='Test Run', include_all=False, case_ids=[1, 2, 3])
    mocked_response(data_json=expected_run.to_json())
    testrail_client.set_project_id(project_id=1)

    api_run = testrail_client.runs.add_run(run=expected_run, project_id=1)

    assert api_run == expected_run


def test_add_run_raises(testrail_client, mocked_response):
    expected_run = Run(id=1, project_id=1, name='Test Run', include_all=False, case_ids=[1, 2, 3])
    mocked_response(data_json=expected_run.to_json())

    with pytest.raises(TestRailException):
        testrail_client.runs.add_run(run=expected_run)


def test_update_run(testrail_client, mocked_response):
    expected_run = Run(id=1, project_id=1, name='Test Run', include_all=False, case_ids=[1, 2, 3])
    mocked_response(data_json=expected_run.to_json())

    api_run = testrail_client.runs.update_run(updated_run=expected_run)

    assert api_run == expected_run


def test_close_run(testrail_client, mocked_response):
    expected_run = Run(id=1, project_id=1, name='Test Run', include_all=False, case_ids=[1, 2, 3])
    mocked_response(data_json=expected_run.to_json())

    api_run = testrail_client.runs.close_run(run_id=1)

    assert api_run == expected_run


def test_delete_run(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.runs.delete_run(run_id=1)

    assert response is True
