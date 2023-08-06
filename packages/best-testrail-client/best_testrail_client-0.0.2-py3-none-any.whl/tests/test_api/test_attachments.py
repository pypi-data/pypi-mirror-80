def test_add_attachment_to_result(testrail_client, mocked_response):
    mocked_response(data_json={'attachment_id': 123})

    api_attachment = testrail_client.attachments.add_attachment_to_result(
        result_id=1, attachment_file={'name': 'Test File', 'file_content': b'123'},
    )

    assert api_attachment == 123


def test_get_attachments_for_case(testrail_client, mocked_response, attachment_data, attachment):
    mocked_response(data_json=[attachment_data])

    api_attachments = testrail_client.attachments.get_attachments_for_case(case_id=1)

    assert api_attachments[0] == attachment


def test_get_attachments_for_test(testrail_client, mocked_response, attachment_data, attachment):
    mocked_response(data_json=[attachment_data])

    api_attachments = testrail_client.attachments.get_attachments_for_test(test_id=1)

    assert api_attachments[0] == attachment


def test_get_attachment(testrail_client, mocked_response, attachment_data, attachment):
    mocked_response(data_json=attachment_data)

    api_attachment = testrail_client.attachments.get_attachment(attachment_id=1)

    assert api_attachment == attachment


def test_delete_attachment(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.attachments.delete_attachment(attachment_id=1)

    assert response is True
