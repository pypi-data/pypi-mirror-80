import datetime
import pydantic
import typing


class Source(pydantic.BaseModel):
    """
    Адрес службы доступа к файлам. Объект участвует в формировании подписи источника данных (hash/source).
    """
    user: typing.Optional[pydantic.StrictStr] = pydantic.Field(
        title="Логин",
        description="Учетная запись пользователя под которой осуществляется доступ к файловой службе",
        example="ivan")
    host: pydantic.StrictStr = pydantic.Field(
        title="Сервер",
        description="DNS имя или IP адрес сервера",
        example="santens.ru")
    port: typing.Optional[pydantic.StrictInt] = pydantic.Field(
        title="ТСР порт",
        example=21)
    path: typing.Optional[pydantic.StrictStr] = pydantic.Field(
        title="Путь на сервере",
        example="/path/to/folder")

    class Config(pydantic.BaseConfig):
        title = 'Источник'


class ColumnDescription(pydantic.BaseModel):
    """
    Описание формата поля файла DBF
    """
    type: typing.Literal['C', 'N', 'D'] = pydantic.Field(
        example="N", title="Формат поля DBF",
        description="C(строка), N(число) D(дата)")
    length: pydantic.StrictInt = pydantic.Field(
        example=19,
        title="Максимальная длинна значения поля")
    decimal_count: typing.Optional[pydantic.StrictInt] = pydantic.Field(
        example=5,
        title="Кол-во десятичных знаков, если формат поля - число")

    class Config:
        title = "Формат колонки DBF"


class Hash(pydantic.BaseModel):
    """
    Контрольные суммы по алгоритму SHA1
    """
    format: pydantic.StrictStr = pydantic.Field(
        exclusiveRegex="^[0-9a-fA-F]{40}$",
        title="Идентификатор формата файла DBF",
        description="Высчитывается из набора колонок файла DBF (columns). "
                    "Выражает тип DBF в независимости от источника получения файла. "
                    "Может случить идентификатором набора колонок и их типов.",
        example="da58e0c8b7a42981282358c43c15b1d7004deaf4")
    source: typing.Optional[pydantic.StrictStr] = pydantic.Field(
        exclusiveRegex="^[0-9a-fA-F]{40}$",
        title="Идентификатор источника данных DBF",
        description="Высчитывается из набора колонок файла DBF (columns) и источника получения файла (url). "
                    "Так как одинаковые форматы DBF могут нести разную прикландую информцию, необходимо точно "
                    "идентифицировать формат файла. Не только по структуре, но и по ее применяемости.",
        example="4e38e02213ec9307ca5cd2bdd3ad9b05f0d24e7a")

    class Config(pydantic.BaseConfig):
        title = "Идентификаторы файла DBF"


class FormatPacket(pydantic.BaseModel):
    namespace: pydantic.StrictStr = pydantic.Field(
        default='Exch', const=True, example='Exch',
        title="Имя адресного пространства схемы данных 1С",
        description="Является константой, служит для идентификации системой 1С данного пакета")
    columns: typing.OrderedDict[pydantic.StrictStr, ColumnDescription] = pydantic.Field(title="Набор колонок файла DBF")
    url: typing.Optional[Source]
    hash: Hash

    class Config:
        title = "Формат файла DBF"


RowValueType = typing.TypeVar('RowValueType', pydantic.StrictStr, pydantic.StrictInt, pydantic.StrictFloat,
                              pydantic.StrictBool, datetime.datetime, datetime.date)


class Packet(Hash, pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        title = "Формат источника данных DBF"

    rows: typing.List[typing.OrderedDict[pydantic.StrictStr, RowValueType]] = pydantic.Field(title="Строки файла DBF")

    class File(pydantic.BaseModel):
        name: pydantic.StrictStr = pydantic.Field(title="Имя загруженного файла")
        hash: pydantic.StrictStr = pydantic.Field(exclusiveRegex="^[0-9a-fA-F]{40}$",
                                                  title="Хеш файла по алгоритму SHA1",
                                                  example="65188ac21abf3198780ebab1cefb005c12958afb")
        modify: datetime.date = pydantic.Field(title="Дата модификации файла DBF",
                                               description="Берется из заголовка самого файла, "
                                                           "не имеет значения зафиксированное время изменнения, "
                                                           "полученое из файловой системы")
        url: typing.Optional[Source]
        hex: pydantic.StrictStr = pydantic.Field(title="Содержимое файла в виде HEX строки")

        class Config(pydantic.BaseConfig):
            title = "Описание загруженного файла DBF"

    file: File
