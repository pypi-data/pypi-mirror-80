def test_get_result_fields(testrail_client, mocked_response, result_field_data, result_field):
    mocked_response(data_json=[result_field_data])

    api_result_fields = testrail_client.result_fields.get_result_fields()

    assert len(api_result_fields) == 1
    assert api_result_fields[0] == result_field
