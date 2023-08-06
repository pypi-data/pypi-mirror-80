def test_get_user(testrail_client, mocked_response, user_data, user):
    mocked_response(data_json=user_data)

    api_user = testrail_client.users.get_user(user_id=1)

    assert api_user == user


def test_get_user_by_email(testrail_client, mocked_response, user_data, user):
    mocked_response(data_json=user_data)

    api_user = testrail_client.users.get_user_by_email(email='alexis@example.com')

    assert api_user == user


def test_get_users(testrail_client, mocked_response, user_data, user):
    mocked_response(data_json=[user_data])

    api_users = testrail_client.users.get_users()

    assert len(api_users) == 1
    assert api_users[0] == user
