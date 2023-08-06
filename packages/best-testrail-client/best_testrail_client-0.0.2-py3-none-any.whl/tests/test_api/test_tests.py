def test_get_test(mocked_response, testrail_client, test_data, test):
    mocked_response(data_json=test_data)

    api_test = testrail_client.tests.get_test(test_id=1)

    assert api_test == test


def test_get_tests(mocked_response, testrail_client, test_data, test):
    mocked_response(data_json=[test_data])

    api_tests = testrail_client.tests.get_tests(run_id=1)

    assert len(api_tests) == 1
    assert api_tests[0] == test
