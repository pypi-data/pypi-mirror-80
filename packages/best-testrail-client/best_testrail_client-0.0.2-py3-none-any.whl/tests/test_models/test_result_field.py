from best_testrail_client.enums import FieldType
from best_testrail_client.models.result_field import ResultField


def test_result_fields_from_json(result_field_data):
    result_fields = ResultField.from_json(data_json=result_field_data)

    assert len(result_fields.configs) == 1
    assert result_fields.configs[0].id == 1
    assert result_fields.configs[0].context.is_global is True
    assert result_fields.configs[0].context.project_ids is None
    assert result_fields.configs[0].options.format == 'markdown'
    assert result_fields.configs[0].options.has_actual is False
    assert result_fields.configs[0].options.has_expected is True
    assert result_fields.configs[0].options.is_required is False
    assert result_fields.display_order == 1
    assert result_fields.id == 5
    assert result_fields.label == 'Steps'
    assert result_fields.name == 'step_results'
    assert result_fields.system_name == 'custom_step_results'
    assert result_fields.type_id == FieldType.STEP_RESULTS
    assert result_fields.description is None


def test_result_fields_to_json(result_field_data):
    result_fields = ResultField.from_json(data_json=result_field_data)

    assert result_fields.to_json() == result_field_data
