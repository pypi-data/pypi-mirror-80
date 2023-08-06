from pydantic import BaseModel, StrictStr
from bssapi_schemas import exch


class PacketsOfTabDataSources(BaseModel):
    """
    Примесь описания источника данных
    """
    Hash: StrictStr
    Format: StrictStr
    Packet: exch.FormatPacket


class PacketsOfTabData(BaseModel):
    """
    Примесь описания пакета данных
    """
    FileName: StrictStr
    Source: StrictStr
    Packet: exch.Packet
