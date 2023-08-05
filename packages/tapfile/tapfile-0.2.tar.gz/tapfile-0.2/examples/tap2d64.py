import struct
import sys

from d64 import DiskImage
from tap_file import TapFile, HeaderType


tape_image = TapFile(sys.argv[1])
with DiskImage(sys.argv[2], 'w') as disk_image:

    expect_header = True

    for obj in tape_image.contents():
        if expect_header:
            if obj.htype == HeaderType.SEQ_DATA:
                out_file.write(obj.data)
                if obj.seq_eof:
                    out_file.close()
            else:
                if obj.htype in (HeaderType.PRG_RELOC, HeaderType.PRG):
                    print("Copying PRG file", obj.name)
                    out_file = disk_image.path(obj.name).open('w', ftype='PRG')
                    out_file.write(struct.pack('<H', obj.start))
                    expect_header = False
                elif obj.htype == HeaderType.SEQ_HDR:
                    print("Copying SEQ file", obj.name)
                    out_file = disk_image.path(obj.name).open('w', ftype='SEQ')
        else:
            out_file.write(obj.data)
            out_file.close()
            expect_header = True
