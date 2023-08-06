from bssapi_schemas import exch
from bssapi_schemas import odata


class PacketsOfTabDataSources(odata.InformationRegister, odata.PacketsOfTabDataSourcesMixin):
    """
    Запись регистра "Пакеты источников импортируемых табличных данных"
    """

    def __init__(self, format: exch.FormatPacket):
        super(PacketsOfTabDataSources, self).__init__(
            Hash=format.hash.source, Format=format.hash.format, Packet=format)


class PacketsOfTabData(odata.InformationRegister, odata.PacketsOfTabDataMixin, odata.PacketsOfTabDataSourcesMixin):
    """
    Запись регистра "Пакеты импортируемых табличных данных"
    """

    def __init__(self, packet: exch.Packet):
        super(PacketsOfTabData, self).__init__(Hash=packet.file.hash, Format=packet.format, Packet=packet,
                                               FileName=packet.file.name, Source=packet.source)
