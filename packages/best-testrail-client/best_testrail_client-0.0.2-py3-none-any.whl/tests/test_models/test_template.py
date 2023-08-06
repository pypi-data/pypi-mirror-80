from best_testrail_client.models.template import Template


def test_template_from_json(template_data):
    template = Template.from_json(data_json=template_data)

    assert template.id == 1
    assert template.is_default is True
    assert template.name == 'Test Case (Text)'
