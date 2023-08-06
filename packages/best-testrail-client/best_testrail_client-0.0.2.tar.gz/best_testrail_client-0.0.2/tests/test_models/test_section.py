from best_testrail_client.models.section import Section


def test_section_from_json(section_data):
    section = Section.from_json(data_json=section_data)

    assert section.depth == 0
    assert section.description is None
    assert section.display_order == 1
    assert section.id == 1
    assert section.name == 'Prerequisites'
    assert section.parent_id is None
    assert section.suite_id == 1
