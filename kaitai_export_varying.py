# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class DataVarying(KaitaiStruct):
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


    class Body(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.field1 = self._io.read_u2le()
            self.field2 = self._io.read_u1()
            self.field3 = self._io.read_u2le()
            self.field4 = self._root.StrWithLen(self._io, self, self._root)
            self.field5 = self._root.StrWithLen(self._io, self, self._root)
            self.field6 = self._io.read_f4le()


    class Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.record_len = self._io.read_u2le()
            self._raw_body = self._io.read_bytes(self.record_len)
            io = KaitaiStream(BytesIO(self._raw_body))
            self.body = self._root.Body(io, self, self._root)



