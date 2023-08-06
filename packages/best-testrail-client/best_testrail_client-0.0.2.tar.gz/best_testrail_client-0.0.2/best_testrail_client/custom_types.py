import typing

import typing_extensions

ModelID = int
FieldName = str
FieldValue = typing.Any
TimeStamp = int
DeleteResult = bool
TimeSpan = str

JsonData = typing.Dict[FieldName, FieldValue]

Method = typing_extensions.Literal['GET', 'POST']


class PaginatorFilters(typing_extensions.TypedDict, total=False):
    limit: typing.Optional[int]
    offset: typing.Optional[int]


class StatusFilters(PaginatorFilters, total=False):
    status_ids: typing.Optional[typing.List[ModelID]]


class CreatedFilters(StatusFilters, total=False):
    created_after: typing.Optional[TimeStamp]
    created_before: typing.Optional[TimeStamp]
    created_by: typing.Optional[typing.List[ModelID]]


class CaseFilter(CreatedFilters, total=False):
    milestone_id: typing.Optional[typing.List[ModelID]]
    priority_id: typing.Optional[typing.List[ModelID]]
    template_id: typing.Optional[typing.List[ModelID]]
    type_id: typing.Optional[typing.List[ModelID]]
    updated_after: typing.Optional[TimeStamp]
    updated_before: typing.Optional[TimeStamp]
    updated_by: typing.Optional[typing.List[ModelID]]


class AttachmentFile(typing_extensions.TypedDict):
    name: str
    file_content: bytes
