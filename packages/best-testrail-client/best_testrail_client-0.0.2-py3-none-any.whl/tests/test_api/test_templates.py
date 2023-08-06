import pytest

from best_testrail_client.exceptions import TestRailException


def test_get_templates_with_provided_project(
    testrail_client, mocked_response, template_data, template,
):
    mocked_response(data_json=[template_data])

    api_templates = testrail_client.templates.get_templates(project_id=1)

    assert len(api_templates) == 1
    assert api_templates[0] == template


def test_get_templates_with_set_project(testrail_client, mocked_response, template_data, template):
    mocked_response(data_json=[template_data])
    testrail_client.set_project_id(project_id=1)

    api_templates = testrail_client.templates.get_templates()

    assert len(api_templates) == 1
    assert api_templates[0] == template


def test_get_templates_raises(testrail_client, mocked_response, template_data, template):
    mocked_response(data_json=[template_data])

    with pytest.raises(TestRailException):
        testrail_client.templates.get_templates()
