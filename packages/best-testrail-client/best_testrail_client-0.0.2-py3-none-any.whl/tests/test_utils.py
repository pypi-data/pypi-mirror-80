import pytest

from best_testrail_client.utils import convert_list_to_filter


@pytest.mark.parametrize(
    'values_list, expected_result',
    [
        ([1, 2, 3], '1,2,3'),
        ([], None),
        (None, None),
    ],
)
def test_convert_list_to_filter(values_list, expected_result):
    filter_string = convert_list_to_filter(values_list=values_list)

    assert filter_string == expected_result
