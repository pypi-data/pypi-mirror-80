import pytest

from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.section import Section


def test_get_section(testrail_client, mocked_response, section_data, section):
    mocked_response(data_json=section_data)

    api_section = testrail_client.sections.get_section(section_id=1)

    assert api_section == section


def test_get_sections_with_provided_project(
    testrail_client, mocked_response, section_data, section,
):
    mocked_response(data_json=[section_data])

    api_sections = testrail_client.sections.get_sections(project_id=1)

    assert api_sections[0] == section


def test_get_sections_with_set_project(testrail_client, mocked_response, section_data, section):
    mocked_response(data_json=[section_data])
    testrail_client.set_project_id(project_id=1)

    api_sections = testrail_client.sections.get_sections()

    assert api_sections[0] == section


def test_get_sections_raises(testrail_client, mocked_response, section_data, section):
    mocked_response(data_json=[section_data])

    with pytest.raises(TestRailException):
        testrail_client.sections.get_sections()


def test_add_section_with_provided_project(testrail_client, mocked_response):
    expected_section = Section(id=1, name='test')
    mocked_response(data_json=expected_section.to_json())

    section = testrail_client.sections.add_section(Section(name='test'), project_id=1)

    assert section == expected_section


def test_add_section_with_set_project(testrail_client, mocked_response):
    expected_section = Section(id=1, name='test')
    mocked_response(data_json=expected_section.to_json())
    testrail_client.set_project_id(project_id=1)

    section = testrail_client.sections.add_section(Section(name='test'))

    assert section == expected_section


def test_add_section_raises(testrail_client, mocked_response):
    expected_section = Section(id=1, name='test')
    mocked_response(data_json=expected_section.to_json())

    with pytest.raises(TestRailException):
        testrail_client.sections.add_section(Section(name='test'))


@pytest.mark.parametrize(
    'description',
    [
        None,
        'test_description',
    ],
)
def test_update_section(description, testrail_client, mocked_response):
    expected_section = Section(id=1, name='test', description=description)
    mocked_response(data_json=expected_section.to_json())

    section = testrail_client.sections.update_section(
        section_id=1, name='test', description=description,
    )

    assert section == expected_section


def test_delete_section(testrail_client, mocked_response):
    mocked_response()

    response = testrail_client.sections.delete_section(section_id=1)

    assert response is True
