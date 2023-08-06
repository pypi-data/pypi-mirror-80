def test_get_case_types(testrail_client, mocked_response, case_type_data, case_type):
    mocked_response(data_json=[case_type_data])

    api_case_types = testrail_client.case_types.get_case_types()

    assert len(api_case_types) == 1
    assert api_case_types[0] == case_type
