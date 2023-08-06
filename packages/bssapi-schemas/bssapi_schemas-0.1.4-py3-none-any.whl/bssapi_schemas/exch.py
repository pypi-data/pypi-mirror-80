from datetime import date, datetime
from typing import OrderedDict, Literal, Optional, TypeVar, Union, List

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr, BaseConfig, BaseModel, IPvAnyAddress


class Source(BaseModel):
    """
    Адрес службы доступа к файлам. Объект участвует в формировании подписи источника данных (hash/source).
    """
    user: Optional[StrictStr] = Field(
        title="Логин",
        description="Учетная запись пользователя под которой осуществляется доступ к файловой службе",
        example="ivan")
    host: Union[IPvAnyAddress, StrictStr] = Field(
        title="Сервер",
        description="DNS имя или IP адрес сервера",
        example="santens.ru")
    port: Optional[StrictInt] = Field(
        title="ТСР порт",
        example=21)
    path: Optional[StrictStr] = Field(
        title="Путь на сервере",
        example="/path/to/folder")

    class Config(BaseConfig):
        title = 'Источник'


class ColumnDescription(BaseModel):
    """
    Описание формата поля файла DBF
    """
    type: Literal['C', 'N', 'D'] = Field(
        example="N", title="Формат поля DBF",
        description="C(строка), N(число) D(дата)")
    length: StrictInt = Field(
        example=19,
        title="Максимальная длинна значения поля")
    decimal_count: Optional[StrictInt] = Field(
        example=5,
        title="Кол-во десятичных знаков, если формат поля - число")

    class Config:
        title = "Формат колонки DBF"


class Hash(BaseModel):
    """
    Контрольные суммы по алгоритму SHA1
    """
    format: str = Field(
        title="Идентификатор формата файла DBF",
        description="Высчитывается из набора колонок файла DBF (columns). "
                    "Выражает тип DBF в независимости от источника получения файла. "
                    "Может случить идентификатором набора колонок и их типов.",
        example="da58e0c8b7a42981282358c43c15b1d7004deaf4", regex="^[0-9a-f]{40}$")
    source: Optional[str] = Field(
        title="Идентификатор источника данных DBF",
        description="Высчитывается из набора колонок файла DBF (columns) и источника получения файла (url). "
                    "Так как одинаковые форматы DBF могут нести разную прикландую информцию, необходимо точно "
                    "идентифицировать формат файла. Не только по структуре, но и по ее применяемости.",
        example="4e38e02213ec9307ca5cd2bdd3ad9b05f0d24e7a", regex="^[0-9a-f]{40}$")

    class Config(BaseConfig):
        title = "Идентификаторы файла DBF"


class FormatPacket(BaseModel):
    namespace: StrictStr = Field(
        default='Exch', const=True, example='Exch',
        title="Имя адресного пространства схемы данных 1С",
        description="Является константой, служит для идентификации системой 1С данного пакета")
    columns: OrderedDict[StrictStr, ColumnDescription] = Field(title="Набор колонок файла DBF")
    url: Optional[Source]
    hash: Hash

    class Config:
        title = "Формат файла DBF"


RowValueType = TypeVar('RowValueType', StrictStr, StrictInt, StrictFloat, StrictBool, datetime, date)


class Packet(Hash):
    class Config(BaseConfig):
        title = "Формат источника данных DBF"

    rows: List[OrderedDict[StrictStr, RowValueType]] = Field(title="Строки файла DBF")

    class File(BaseModel):
        name: StrictStr = Field(title="Имя загруженного файла")
        hash: str = Field(title="Хеш файла по алгоритму SHA1",
                                example="65188AC21ABF3198780EBAB1CEFD005C12958AFB", regex="^[0-9A-F]{40}$")
        modify: date = Field(title="Дата модификации файла DBF",
                             description="Берется из заголовка самого файла, "
                                         "не имеет значения зафиксированное время изменнения, "
                                         "полученое из файловой системы")
        url: Optional[Source]
        hex: str = Field(title="Содержимое файла в виде HEX строки", regex="^[0-9A-F]{2,}$")

        class Config(BaseConfig):
            title = "Описание загруженного файла DBF"

    file: File
