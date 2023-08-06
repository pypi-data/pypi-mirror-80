from best_testrail_client.models.user import User


def test_user_from_json(user_data):
    user = User.from_json(data_json=user_data)

    assert user.email == 'alexis@example.com'
    assert user.id == 1
    assert user.is_active is True
    assert user.name == 'Alexis Gonzalez'
