import typing

from best_testrail_client.api.base_api import BaseAPI
from best_testrail_client.custom_types import ModelID, AttachmentFile, DeleteResult
from best_testrail_client.models.attachment import Attachment


class AttachmentsAPI(BaseAPI):
    """Attachments API. http://docs.gurock.com/testrail-api2/reference-attachments"""
    def add_attachment_to_result(
        self, result_id: ModelID, attachment_file: AttachmentFile,
    ) -> typing.Optional[ModelID]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#add_attachment_to_result"""
        attachment_data = self._request(
            f'add_attachment_to_result/{result_id}', method='POST', attachment=attachment_file,
        )
        return attachment_data.get('attachment_id')

    def get_attachments_for_case(self, case_id: ModelID) -> typing.List[Attachment]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_case"""
        attachments_data = self._request(f'get_attachments_for_case/{case_id}')
        return [
            Attachment.from_json(data_json=attachment_data) for attachment_data in attachments_data
        ]

    def get_attachments_for_test(self, test_id: ModelID) -> typing.List[Attachment]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_test"""
        attachments_data = self._request(f'get_attachments_for_test/{test_id}')
        return [
            Attachment.from_json(data_json=attachment_data) for attachment_data in attachments_data
        ]

    def get_attachment(self, attachment_id: ModelID) -> Attachment:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachment"""
        attachment_data = self._request(f'get_attachment/{attachment_id}')
        return Attachment.from_json(data_json=attachment_data)

    def delete_attachment(self, attachment_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-attachments#delete_attachment"""
        self._request(f'delete_attachment/{attachment_id}', method='POST')
        return True
