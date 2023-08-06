from best_testrail_client.models.run import Run


def test_run_from_json(run_data):
    run = Run.from_json(data_json=run_data)

    assert run.assignedto_id == 6
    assert run.blocked_count == 0
    assert run.completed_on is None
    assert run.config == 'Firefox, Ubuntu 12'
    assert run.config_ids == [2, 6]
    assert run.case_ids is None
    assert run.created_by == 1
    assert run.created_on == 1393845644
    assert run.refs == 'SAN-1'
    assert run.custom['custom_status1_count'] == 0
    assert run.custom['custom_status2_count'] == 0
    assert run.custom['custom_status3_count'] == 0
    assert run.custom['custom_status4_count'] == 0
    assert run.custom['custom_status5_count'] == 0
    assert run.custom['custom_status6_count'] == 0
    assert run.custom['custom_status7_count'] == 0
    assert run.description is None
    assert run.failed_count == 2
    assert run.id == 81
    assert run.include_all is False
    assert run.is_completed is False
    assert run.milestone_id == 7
    assert run.name == 'File Formats'
    assert run.passed_count == 2
    assert run.plan_id == 80
    assert run.project_id == 1
    assert run.retest_count == 1
    assert run.suite_id == 4
    assert run.untested_count == 3
    assert run.url == 'http://<server>/testrail/index.php?/runs/view/81'


def test_run_to_json(run_data):
    run = Run.from_json(data_json=run_data)

    assert run.to_json() == run_data


def test_run_from_json_with_unexpected_key(run_data):
    data_with_extra_key = dict(run_data)
    data_with_extra_key['some_random_key'] = 'Some random value'

    run = Run.from_json(data_json=data_with_extra_key)

    assert run.to_json() == run_data
