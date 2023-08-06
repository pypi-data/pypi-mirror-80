def test_get_statuses(testrail_client, mocked_response, status_data, status):
    mocked_response(data_json=[status_data])

    api_statuses = testrail_client.statuses.get_statuses()

    assert len(api_statuses) == 1
    assert api_statuses[0] == status
