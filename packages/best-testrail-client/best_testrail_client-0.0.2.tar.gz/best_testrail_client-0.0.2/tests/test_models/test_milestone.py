from best_testrail_client.models.milestone import Milestone


def test_milestone_from_json(milestone_data):
    milestone = Milestone.from_json(data_json=milestone_data)

    assert milestone.completed_on == 1389968184
    assert milestone.description == 'Milestone description'
    assert milestone.due_on == 1391968184
    assert milestone.id == 1
    assert milestone.is_completed is False
    assert milestone.name == 'Release 1.5'
    assert milestone.project_id == 1
    assert milestone.is_started is True
    assert milestone.milestones == [2, 3, 4]
    assert milestone.parent_id is None
    assert milestone.start_on == 1389968184
    assert milestone.started_on == 1389968184
    assert milestone.url == 'http://<server>/testrail/index.php?/milestones/view/1'
