import pytest

from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.configuration import Configuration, GroupConfig


def test_get_configs_with_provided_project(
    testrail_client, mocked_response, configuration_data, configuration,
):
    mocked_response(data_json=[configuration_data])

    api_configurations = testrail_client.configurations.get_configs(project_id=1)

    assert len(api_configurations) == 1
    assert api_configurations[0] == configuration


def test_get_configs_with_set_project(
    testrail_client, mocked_response, configuration_data, configuration,
):
    mocked_response(data_json=[configuration_data])
    testrail_client.set_project_id(project_id=1)

    api_configurations = testrail_client.configurations.get_configs()

    assert len(api_configurations) == 1
    assert api_configurations[0] == configuration


def test_get_configs_raises(
    testrail_client, mocked_response, configuration_data, configuration,
):
    mocked_response(data_json=[configuration_data])

    with pytest.raises(TestRailException):
        testrail_client.configurations.get_configs()


def test_add_config_group_with_provided_project(testrail_client, mocked_response):
    expected_config = Configuration(id=1, project_id=1, name='Test Group', configs=[])
    mocked_response(data_json=expected_config.to_json())

    api_config_group = testrail_client.configurations.add_config_group(
        name='Test Group', project_id=1,
    )

    assert api_config_group == expected_config


def test_add_config_group_with_set_project(testrail_client, mocked_response):
    expected_config = Configuration(id=1, project_id=1, name='Test Group', configs=[])
    mocked_response(data_json=expected_config.to_json())
    testrail_client.set_project_id(project_id=1)

    api_config_group = testrail_client.configurations.add_config_group(
        name='Test Group', project_id=1,
    )

    assert api_config_group == expected_config


def test_add_config_group_raises(testrail_client, mocked_response):
    mocked_response(data_json=1)

    with pytest.raises(TestRailException):
        testrail_client.configurations.add_config_group(name='Test Group')


def test_add_config(testrail_client, mocked_response):
    expected_config = GroupConfig(id=1, group_id=1, name='Test Config')
    mocked_response(data_json=expected_config.to_json())

    api_config = testrail_client.configurations.add_config(name='Test Config', config_group_id=1)

    assert api_config == expected_config


def test_update_config_group(testrail_client, mocked_response):
    expected_config = Configuration(id=1, project_id=1, name='New Test Group', configs=[])
    mocked_response(data_json=expected_config.to_json())

    api_config_group = testrail_client.configurations.update_config_group(
        name='New Test Group', config_group_id=1,
    )

    assert api_config_group == expected_config


def test_update_config(testrail_client, mocked_response):
    expected_config = GroupConfig(id=1, group_id=1, name='New Test Config')
    mocked_response(data_json=expected_config.to_json())

    api_config = testrail_client.configurations.update_config(name='New Test Config', config_id=1)

    assert api_config == expected_config


def test_delete_config_group(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.configurations.delete_config_group(config_group_id=1)

    assert response is True


def test_delete_config(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.configurations.delete_config(config_id=1)

    assert response is True
