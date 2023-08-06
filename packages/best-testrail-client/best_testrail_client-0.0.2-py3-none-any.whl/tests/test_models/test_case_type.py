from best_testrail_client.models.case_type import CaseType


def test_case_types_from_json(case_type_data):
    case_type = CaseType.from_json(data_json=case_type_data)

    assert case_type.id == 1
    assert case_type.is_default is False
    assert case_type.name == 'Automated'
