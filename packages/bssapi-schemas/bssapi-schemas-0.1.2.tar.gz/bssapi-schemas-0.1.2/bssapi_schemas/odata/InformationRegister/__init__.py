from bssapi_schemas.odata import InformationRegister, PacketsOfTabDataMixin, PacketsOfTabDataSourcesMixin
from exch import FormatPacket, Packet


class PacketsOfTabDataSources(InformationRegister, PacketsOfTabDataSourcesMixin):
    def __init__(self, format: FormatPacket):
        pass


class PacketsOfTabData(InformationRegister, PacketsOfTabDataSourcesMixin, PacketsOfTabDataMixin):
    def __init__(self, packet: Packet):
        super(PacketsOfTabData, self).__init__(Hash=packet.File.hash, Format=packet.format, Packet=packet,
                                               FileName=packet.file.name, Source=packet.source)
