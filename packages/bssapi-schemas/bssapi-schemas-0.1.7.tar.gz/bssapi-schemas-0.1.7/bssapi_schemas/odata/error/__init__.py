from typing import Literal

from pydantic import BaseModel, Field, StrictStr


class Message(BaseModel):
    lang: Literal['en', 'ru']
    value: StrictStr


class Descriplion(BaseModel):
    code: StrictStr
    message: Message


class Model(BaseModel):
    error: Descriplion = Field(alias='odata.error')
