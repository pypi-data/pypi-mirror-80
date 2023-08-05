import logging
import struct

from .data_stream import DataStream
from .dipole import Dipole
from .header_type import HeaderType
from .tap_object import TapData, TapHeader

log = logging.getLogger(__name__)


class TapFile:
    def __init__(self, file_path):
        self.fileh = open(str(file_path), 'rb')
        header = self.fileh.read(0x14)
        if header[:12] != b'C64-TAPE-RAW':
            raise ValueError("Invalid file format")
        self.version = header[12]
        if self.version > 1:
            raise NotImplementedError("Unsupported version, "+str(self.version))
        self.platform = header[13]
        self.video = header[14]
        self.length, = struct.unpack('<L', header[0x10:0x14])
        self.dipole = Dipole()

    def next_dipole(self):
        data = self.fileh.read(1)
        if not data:
            return None

        if ord(data) == 0:
            if self.version == 0:
                val = None
            else:
                data = self.fileh.read(3)+b'\x00'
                val, = struct.unpack('<L', data)
        else:
            val = ord(data)*8

        d = self.dipole.classify(val)
        return d

    def consume_leader(self, d):
        if d == 'S':
            self.leader += 1
        elif d == 'L' and self.leader >= 16:
            # end of leader
            self.in_leader = False
            self.queued = d
            self.stream = DataStream()
        else:
            self.leader -= 1

    def consume_byte_stream(self, d):
        self.queued += d

        if self.queued.endswith('SSSS'):
            # still in leader
            self.in_leader = True
            return None

        eod = self.queued.endswith('LS')
        if self.queued.endswith('LM') or eod:
            if self.queued == 'LM':
                # initial start of data
                self.queued = ''
            elif len(self.queued) >= 20:
                # may have a complete, good byte
                to_process = []
                for i in range(len(self.queued)-4, len(self.queued)-22, -2):
                    if self.queued[i:i+2] in ('SM', 'MS'):
                        # valid data bit
                        to_process.append(int(self.queued[i:i+2] == 'MS'))
                    else:
                        # invalid, continue queuing
                        break

                if len(to_process) == 9:
                    # good byte

                    self.queued = self.queued[:-20]
                    if self.queued:
                        # one or more bad bytes before this good one
                        errors = (len(self.queued)-1)//20+1
                        for _ in range(0, errors):
                            self.stream.add_byte(None)
                        self.queued = ''

                    self.stream.add_byte(to_process)

        if eod:
            self.in_leader = True
            self.leader = 0
            if len(self.stream) > 10:
                return self.stream
        return None

    def byte_stream(self, is_header=True):
        self.leader = 0
        self.in_leader = True

        while True:
            d = self.next_dipole()
            if d is None:
                return None
            if self.in_leader:
                self.consume_leader(d)
            else:
                ret = self.consume_byte_stream(d)
                if ret:
                    # if a header is expected ignore obviously short streams
                    if not is_header or len(ret) >= 200:
                        return ret

    def contents(self):
        """Return the next data object in the file."""
        while True:
            # consume first header
            header1 = self.byte_stream()
            log.debug("header1: %s", header1)
            if not header1:
                return

            # consume second header
            header2 = self.byte_stream()
            log.debug("header2: %s", header2)
            if not header2:
                return

            # choose best header (yield)
            header = TapHeader(header1, header2)
            log.debug("Header: %s", header)
            yield header

            if header.htype in (HeaderType.PRG_RELOC, HeaderType.PRG):
                # consume first PRG payload
                data1 = self.byte_stream(is_header=False)
                log.debug("data1: %s", data1)
                if not data1:
                    return

                # consume second PRG payload
                data2 = self.byte_stream(is_header=False)
                log.debug("data2: %s", data2)
                if not data2:
                    return

                # choose best PRG payload (yield)
                data = TapData(data1, data2, header.end-header.start)
                log.debug("Data: %s", data)
                yield data
