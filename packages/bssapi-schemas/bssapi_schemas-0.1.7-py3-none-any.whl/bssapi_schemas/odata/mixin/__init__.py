from pydantic import BaseModel, StrictStr, Field

from bssapi_schemas import exch


class PacketsOfTabDataSources(BaseModel):
    """
    Примесь описания источника данных
    """
    Hash: str = Field(regex="^[0-9a-f]{40}$")
    Format: str = Field(regex="^[0-9a-f]{40}$")
    Packet: exch.FormatPacket


class PacketsOfTabData(BaseModel):
    """
    Примесь описания пакета данных
    """
    Hash: str = Field(regex="^[0-9A-F]{40}$")
    FileName: StrictStr
    Source: str = Field(regex="^[0-9a-f]{40}$")
    Packet: exch.Packet
