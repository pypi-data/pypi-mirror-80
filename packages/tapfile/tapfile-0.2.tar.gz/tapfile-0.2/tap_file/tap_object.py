import logging
import struct

from .data_stream import DataStream
from .header_type import HeaderType


log = logging.getLogger(__name__)


class TapObject:
    def __init__(self):
        """Create an object from two data streams."""
        self._data, errors1 = self.primary.payload()
        if errors1:
            # can only perform error correction if stream lengths match
            if len(self.primary) == len(self.secondary):
                data2, errors2 = self.secondary.payload()
                for n in errors1-errors2:
                    self._data[n] = data2[n]
                self.uncorrected_errors = bool(errors1 & errors2)
                if self.uncorrected_errors:
                    log.debug("Uncorrected errors remain")
                else:
                    log.debug("All errors corrected")
            else:
                log.debug("Stream lengths differ, no error correction")
                self.uncorrected_errors = True
        else:
            self.uncorrected_errors = False

    def __str__(self):
        return "<{}: data_len - {}, errors? - {}>".format(type(self).__name__, len(self._data), self.uncorrected_errors)


class TapHeader(TapObject):
    """All objects except program data."""
    def __init__(self, stream1, stream2):
        self.primary, self.secondary = DataStream.grade_streams(stream1, stream2, 202)
        super().__init__()

    @property
    def htype(self):
        """Header type."""
        return HeaderType(self._data[0])

    @property
    def start(self):
        """Start address, only valid for program headers."""
        return struct.unpack('<H', self._data[1:3])[0]

    @property
    def end(self):
        """End address, only valid for program headers."""
        return struct.unpack('<H', self._data[3:5])[0]

    @property
    def name(self):
        """File name."""
        return self._data[5:21].rstrip(b' ')

    @property
    def data(self):
        """For SEQ objects the payload, rest of header after file name for others."""
        if self.htype == HeaderType.SEQ_DATA:
            nul = self._data.find(b'\x00')
            if nul == -1:
                return self._data[1:]
            return self._data[1:nul]
        return self._data[21:]

    @property
    def seq_eof(self):
        """True if payload contains NUL."""
        return self._data.find(b'\x00') != -1


class TapData(TapObject):
    """Program data object."""
    def __init__(self, stream1, stream2, length):
        self.primary, self.secondary = DataStream.grade_streams(stream1, stream2, length+10)
        super().__init__()

    @property
    def data(self):
        """Program payload."""
        return self._data
