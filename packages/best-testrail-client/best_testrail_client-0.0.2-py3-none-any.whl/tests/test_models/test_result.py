from best_testrail_client.models.result import Result


def test_result_from_json(result_data):
    result = Result.from_json(data_json=result_data)

    assert result.assignedto_id == 1
    assert result.attachment_ids is None
    assert result.comment == 'This test failed: ..'
    assert result.created_by == 1
    assert result.created_on == 1393851801
    assert result.defects == 'TR-1'
    assert result.elapsed == '5m'
    assert result.id == 1
    assert result.status_id == 5
    assert result.test_id == 1
    assert result.version == '1.0RC1'
    assert result.custom == {
        'custom_step_results': [
            {
                'step1': 'pass',
            },
            {
                'step2': 'fail',
            },
        ],
    }


def test_result_to_json(result_data):
    result = Result.from_json(data_json=result_data)

    assert result.to_json() == result_data
