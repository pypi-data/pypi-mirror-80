def test_get_priorities(testrail_client, mocked_response, priority_data, priority):
    mocked_response(data_json=[priority_data])

    api_priorities = testrail_client.priorities.get_priorities()

    assert len(api_priorities) == 1
    assert api_priorities[0] == priority
