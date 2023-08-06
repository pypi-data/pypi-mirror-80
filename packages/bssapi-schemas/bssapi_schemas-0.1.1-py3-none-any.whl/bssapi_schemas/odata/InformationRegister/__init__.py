import typing
import pydantic
from bssapi_schemas.odata import InformationRegister


class PacketsOfTabDataSources(InformationRegister):
    Hash: pydantic.StrictStr = pydantic.Field(exclusiveRegex="^[0-9a-FA-F]{40}$")
    Format: pydantic.StrictStr = pydantic.Field(exclusiveRegex="^[0-9a-FA-F]{40}$")
    Packet: typing.Union[pydantic.StrictStr]


class PacketsOfTabData(PacketsOfTabDataSources):
    Source: pydantic.StrictStr = pydantic.Field(exclusiveRegex="^[0-9a-FA-F]{40}$")
    FileName: pydantic.StrictStr
