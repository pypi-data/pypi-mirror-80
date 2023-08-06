import pydantic


class oDataUrl(pydantic.AnyHttpUrl):
    user_required: bool = True

    @property
    def is_secure(self) -> bool:
        return self.scheme.endswith('s')


class InformationRegister(pydantic.BaseModel):

    @staticmethod
    def _get_url(base_url: pydantic.StrictStr) -> oDataUrl:
        class __get_url(pydantic.BaseModel):
            address: oDataUrl

        return __get_url(address=base_url).address

    @classmethod
    def path(cls, base_url: pydantic.AnyHttpUrl) -> pydantic.AnyHttpUrl:
        base_url += "/odata/standard.odata/InformationRegister_{InformationRegister}?$format=json" \
            .format(InformationRegister=cls.__name__)
        return cls._get_url(base_url=pydantic.StrictStr(base_url))
