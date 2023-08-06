from best_testrail_client.models.result import Result


def test_get_results(testrail_client, mocked_response, result_data, result):
    mocked_response(data_json=[result_data])

    api_results = testrail_client.results.get_results(test_id=1)

    assert len(api_results) == 1
    assert api_results[0] == result


def test_get_results_for_case(testrail_client, mocked_response, result_data, result):
    mocked_response(data_json=[result_data])

    api_results = testrail_client.results.get_results_for_case(run_id=1, case_id=1)

    assert len(api_results) == 1
    assert api_results[0] == result


def test_get_results_for_run(testrail_client, mocked_response, result_data, result):
    mocked_response(data_json=[result_data])

    api_results = testrail_client.results.get_results_for_run(run_id=1)

    assert len(api_results) == 1
    assert api_results[0] == result


def test_add_result(testrail_client, mocked_response):
    expected_result = Result(status_id=1, comment='Success')
    mocked_response(data_json=expected_result.to_json())

    api_result = testrail_client.results.add_result(test_id=1, result=expected_result)

    assert api_result == expected_result


def test_add_result_for_case(testrail_client, mocked_response):
    expected_result = Result(status_id=1, comment='Success')
    mocked_response(data_json=expected_result.to_json())

    api_result = testrail_client.results.add_result_for_case(
        run_id=1, case_id=1, result=expected_result,
    )

    assert api_result == expected_result


def test_add_results(testrail_client, mocked_response):
    expected_result = Result(status_id=1, comment='Success', test_id=1)
    mocked_response(data_json=[expected_result.to_json()])

    api_results = testrail_client.results.add_results(run_id=1, results=[expected_result])

    assert api_results[0] == expected_result


def test_add_results_for_cases(testrail_client, mocked_response):
    expected_result = Result(status_id=1, comment='Success', case_id=1)
    mocked_response(data_json=[expected_result.to_json()])

    api_results = testrail_client.results.add_results_for_cases(run_id=1, results=[expected_result])

    assert api_results[0] == expected_result
