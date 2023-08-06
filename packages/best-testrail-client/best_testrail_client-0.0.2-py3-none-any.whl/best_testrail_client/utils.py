import typing

from best_testrail_client.custom_types import ModelID


def convert_list_to_filter(
    values_list: typing.Optional[typing.List[ModelID]],
) -> typing.Optional[str]:
    return ','.join(str(value) for value in values_list) if values_list else None
