import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.custom_types import ModelID, JsonData
from best_testrail_client.models.user import User


class UsersAPI(BaseAPI):
    """Users API. http://docs.gurock.com/testrail-api2/reference-users"""
    def get_user(self, user_id: ModelID) -> User:
        """http://docs.gurock.com/testrail-api2/reference-users#get_user"""
        user_data = self._request(f'get_user/{user_id}')
        return User.from_json(user_data)

    def get_user_by_email(self, email: str) -> User:
        """http://docs.gurock.com/testrail-api2/reference-users#get_user_by_email"""
        user_data = self._request(f'get_user_by_email/{email}')
        return User.from_json(user_data)

    def get_users(self) -> typing.List[User]:
        """http://docs.gurock.com/testrail-api2/reference-users#get_users"""
        users_data: typing.List[JsonData] = self._request('get_users')
        return [User.from_json(user_data) for user_data in users_data]
