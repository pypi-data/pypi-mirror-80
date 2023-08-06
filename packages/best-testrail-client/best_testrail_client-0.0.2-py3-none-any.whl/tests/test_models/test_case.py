from best_testrail_client.models.case import Case


def test_case_from_json(case_data):
    case = Case.from_json(data_json=case_data)

    assert case.created_by == 5
    assert case.created_on == 1392300984
    assert case.display_order is None
    assert case.estimate == '1m 5s'
    assert case.estimate_forecast is None
    assert case.id == 1
    assert case.milestone_id == 7
    assert case.priority_id == 2
    assert case.template_id is None
    assert case.refs == 'RF-1, RF-2'
    assert case.section_id == 1
    assert case.suite_id == 1
    assert case.title == 'Change document attributes (author, title, organization)'
    assert case.type_id == 4
    assert case.updated_by == 1
    assert case.updated_on == 1393586511
    assert case.custom == {
        'custom_expected': 'Custom Expected',
        'custom_preconds': 'Custom Preconditions',
        'custom_steps': 'Custom Steps',
        'custom_steps_separated': [
            {
                'content': 'Step 1',
                'expected': 'Expected Result',
            },
            {
                'content': 'Step 2',
                'expected': 'Expected Result 2',
            },
        ],
    }


def test_case_to_json(case_data):
    case = Case.from_json(data_json=case_data)

    assert case.to_json() == case_data
