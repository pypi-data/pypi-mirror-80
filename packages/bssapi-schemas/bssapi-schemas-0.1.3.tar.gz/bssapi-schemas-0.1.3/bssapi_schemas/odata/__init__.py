from pydantic import Field, BaseModel, StrictStr, AnyHttpUrl
import bssapi_schemas.exch as exch

class oDataUrl(AnyHttpUrl):
    user_required: bool = True

    @property
    def is_secure(self) -> bool:
        return self.scheme.endswith('s')


class InformationRegister(BaseModel):

    @staticmethod
    def _get_url(base_url: StrictStr) -> oDataUrl:
        class __get_url(BaseModel):
            address: oDataUrl

        return __get_url(address=base_url).address

    @classmethod
    def path(cls, base_url: AnyHttpUrl) -> AnyHttpUrl:
        base_url += "/odata/standard.odata/InformationRegister_{InformationRegister}?$format=json" \
            .format(InformationRegister=cls.__name__)
        return cls._get_url(base_url=StrictStr(base_url))


class PacketsOfTabDataSourcesMixin(BaseModel):
    """
    Примесь описания источника данных
    """
    Hash: StrictStr
    Format: StrictStr
    Packet: exch.FormatPacket


class PacketsOfTabDataMixin(BaseModel):
    """
    Примесь описания пакета данных
    """
    FileName: StrictStr
    Source: StrictStr
    Packet: exch.Packet
