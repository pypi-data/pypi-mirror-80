from best_testrail_client.models.priority import Priority


def test_priority_from_json(priority_data):
    priority = Priority.from_json(data_json=priority_data)

    assert priority.id == 1
    assert priority.is_default is False
    assert priority.priority == 1
    assert priority.name == "1 - Don't Test"
    assert priority.short_name == "1 - Don't"
