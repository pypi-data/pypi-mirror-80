import pytest

from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.milestone import Milestone


def test_get_milestone(testrail_client, mocked_response, milestone_data, milestone):
    mocked_response(data_json=milestone_data)

    api_milestone = testrail_client.milestones.get_milestone(milestone_id=1)

    assert api_milestone == milestone


def test_get_milestones_with_provided_project(
    testrail_client, mocked_response, milestone_data, milestone,
):
    mocked_response(data_json=[milestone_data])

    api_milestones = testrail_client.milestones.get_milestones(project_id=1)

    assert api_milestones[0] == milestone


def test_get_milestones_with_set_project(
    testrail_client, mocked_response, milestone_data, milestone,
):
    mocked_response(data_json=[milestone_data])
    testrail_client.set_project_id(project_id=1)

    api_milestones = testrail_client.milestones.get_milestones()

    assert api_milestones[0] == milestone


def test_get_milestones_raises(
    testrail_client, mocked_response, milestone_data, milestone,
):
    mocked_response(data_json=[milestone_data])

    with pytest.raises(TestRailException):
        testrail_client.milestones.get_milestones()


def test_add_milestone_with_provided_project(testrail_client, mocked_response):
    expected_milestone = Milestone(name='Test milestone', id=1)
    mocked_response(data_json=expected_milestone.to_json())

    api_milestone = testrail_client.milestones.add_milestone(
        milestone=expected_milestone, project_id=1,
    )

    assert api_milestone == expected_milestone


def test_add_milestone_with_set_project(testrail_client, mocked_response):
    expected_milestone = Milestone(name='Test milestone', id=1)
    mocked_response(data_json=expected_milestone.to_json())
    testrail_client.set_project_id(project_id=1)

    api_milestone = testrail_client.milestones.add_milestone(milestone=expected_milestone)

    assert api_milestone == expected_milestone


def test_add_milestone_raises(testrail_client, mocked_response):
    expected_milestone = Milestone(name='Test milestone', id=1)
    mocked_response(data_json=expected_milestone.to_json())

    with pytest.raises(TestRailException):
        testrail_client.milestones.add_milestone(milestone=expected_milestone)


def test_update_milestone(testrail_client, mocked_response):
    expected_milestone = Milestone(name='Test milestone', id=1)
    mocked_response(data_json=expected_milestone.to_json())

    api_milestone = testrail_client.milestones.update_milestone(milestone=expected_milestone)

    assert api_milestone == expected_milestone


def test_delete_milestone(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.milestones.delete_milestone(milestone_id=1)

    assert response is True
