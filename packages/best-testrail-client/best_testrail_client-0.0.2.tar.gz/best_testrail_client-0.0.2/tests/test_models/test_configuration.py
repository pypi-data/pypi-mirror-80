from best_testrail_client.models.configuration import Configuration, GroupConfig


def test_group_config_from_json(group_config_data):
    group_config = GroupConfig.from_json(data_json=group_config_data)

    assert group_config.id == 1
    assert group_config.group_id == 1
    assert group_config.name == 'Chrome'


def test_configuration_from_json(configuration_data):
    configuration = Configuration.from_json(data_json=configuration_data)

    assert configuration.id == 1
    assert configuration.name == 'Browsers'
    assert configuration.project_id == 1
    assert len(configuration.configs) == 3
    assert configuration.configs[0].id == 1
    assert configuration.configs[0].group_id == 1
    assert configuration.configs[0].name == 'Chrome'


def test_configuration_to_json(configuration_data):
    configuration = Configuration.from_json(data_json=configuration_data)

    assert configuration.to_json() == configuration_data
