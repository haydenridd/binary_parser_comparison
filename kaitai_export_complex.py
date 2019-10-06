# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class DataComplex(KaitaiStruct):

    class SubTables(Enum):
        sub_table1 = 1
        sub_table2 = 2
        sub_table3 = 3
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.record = []
        i = 0
        while not self._io.is_eof():
            self.record.append(self._root.Record(self._io, self, self._root))
            i += 1


    class StrWithLen(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u1()
            self.value = (self._io.read_bytes(self.len)).decode(u"UTF-8")


    class SubTable1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.table1_field1 = self._io.read_u2le()
            self.table1_field2 = self._io.read_u1()
            self.table1_field3 = self._root.StrWithLen(self._io, self, self._root)
            self.table1_field4 = self._io.read_f4le()


    class SubTable2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.table2_field1 = self._root.StrWithLen(self._io, self, self._root)
            self.table2_field2 = self._root.StrWithLen(self._io, self, self._root)
            self.table2_field3 = self._root.StrWithLen(self._io, self, self._root)


    class SubTable3(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.table3_field1 = self._io.read_u2le()
            self.table3_field2 = self._io.read_u4le()
            self.table3_field3 = self._io.read_u4le()
            self.table3_field4 = self._io.read_u4le()
            self.table3_field5 = self._io.read_u4le()
            self.table3_field6 = self._io.read_u4le()
            self.table3_field7 = self._io.read_u4le()
            self.table3_field8 = self._io.read_u4le()
            self.table3_field9 = self._root.StrWithLen(self._io, self, self._root)
            self.table3_field10 = self._io.read_f4le()
            self.table3_field11 = self._io.read_f4le()


    class Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.record_len = self._io.read_u2le()
            self.record_typ = self._root.SubTables(self._io.read_u1())
            _on = self.record_typ
            if _on == self._root.SubTables.sub_table1:
                self._raw_body = self._io.read_bytes(self.record_len)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.SubTable1(io, self, self._root)
            elif _on == self._root.SubTables.sub_table2:
                self._raw_body = self._io.read_bytes(self.record_len)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.SubTable2(io, self, self._root)
            elif _on == self._root.SubTables.sub_table3:
                self._raw_body = self._io.read_bytes(self.record_len)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.SubTable3(io, self, self._root)
            else:
                self.body = self._io.read_bytes(self.record_len)



