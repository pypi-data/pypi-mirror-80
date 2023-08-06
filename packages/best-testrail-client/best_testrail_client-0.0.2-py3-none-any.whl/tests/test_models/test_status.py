from best_testrail_client.models.status import Status


def test_status_from_json(status_data):
    status = Status.from_json(data_json=status_data)

    assert status.color_bright == 12709313
    assert status.color_dark == 6667107
    assert status.color_medium == 9820525
    assert status.id == 1
    assert status.is_final is True
    assert status.is_system is True
    assert status.is_untested is False
    assert status.label == 'Passed'
    assert status.name == 'passed'
