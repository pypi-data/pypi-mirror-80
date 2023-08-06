from best_testrail_client.models.attachment import Attachment


def test_attachment_from_json(attachment_data):
    attachment = Attachment.from_json(data_json=attachment_data)

    assert attachment.id == 444
    assert attachment.name == 'What-Testers-Should-Be-Automating.jpg'
    assert attachment.filename == '444.what_testers_should_be_automating.jpg'
    assert attachment.size == 166994
    assert attachment.created_on == 1554737184
    assert attachment.project_id == 14
    assert attachment.case_id == 3414
    assert attachment.test_change_id == 17899
    assert attachment.user_id == 10
