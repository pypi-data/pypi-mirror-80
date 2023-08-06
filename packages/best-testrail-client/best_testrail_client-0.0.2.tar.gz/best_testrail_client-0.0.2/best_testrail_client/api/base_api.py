from __future__ import annotations

import json
import typing

import requests

from best_testrail_client.custom_types import ModelID, JsonData, Method, AttachmentFile


class BaseAPI:
    def __init__(self, testrail_url: str, login: str, token: str):
        self._token = token
        self._login = login
        self._project_id: typing.Optional[ModelID] = None

        if not testrail_url.endswith('/'):
            testrail_url += '/'
        self._base_url = f'{testrail_url}index.php?/api/v2/'

    def _request(
        self,
        url: str, data: typing.Optional[JsonData] = None, method: Method = 'GET',
        params: typing.Optional[JsonData] = None,
        attachment: typing.Optional[AttachmentFile] = None,
    ) -> typing.Any:
        if data is None:
            data = {}
        attach_files = None
        if attachment is not None:
            attach_files = {'attachment': (attachment['name'], attachment['file_content'])}

        response = requests.request(
            method, f'{self._base_url}{url}', json=data,
            auth=(self._login, self._token), params=params, files=attach_files,
        )

        try:
            return response.json()
        except json.JSONDecodeError:
            return response


class ProjectDependableAPI(BaseAPI):
    def set_project_id(self, project_id: ModelID) -> ProjectDependableAPI:
        self._project_id = project_id
        return self
