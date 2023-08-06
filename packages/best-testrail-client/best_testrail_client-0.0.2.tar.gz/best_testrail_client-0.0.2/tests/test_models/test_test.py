from best_testrail_client.models.test import Test


def test_test_from_json(test_data):
    test = Test.from_json(data_json=test_data)

    assert test.assignedto_id == 1
    assert test.case_id == 1
    assert test.estimate == '1m 5s'
    assert test.estimate_forecast is None
    assert test.id == 100
    assert test.priority_id == 2
    assert test.milestone_id is None
    assert test.run_id == 1
    assert test.refs is None
    assert test.status_id == 5
    assert test.template_id is None
    assert test.title == 'Verify line spacing on multi-page document'
    assert test.type_id == 4
    assert test.custom == {
        'custom_expected': 'Custom Expected',
        'custom_preconds': 'Custom Preconditions',
        'custom_steps_separated': [
            {
                'content': 'Step 1',
                'expected': 'Expected Result 1',
            },
            {
                'content': 'Step 2',
                'expected': 'Expected Result 2',
            },
        ],
    }


def test_test_to_json(test_data):
    test = Test.from_json(data_json=test_data)

    assert test.to_json(include_none=True) == test_data
