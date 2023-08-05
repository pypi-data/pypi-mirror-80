import logging
import sys

from tap_file import TapFile, HeaderType


logging.basicConfig(level="DEBUG")

t = TapFile(sys.argv[1])

expect_header = True

for obj in t.contents():
    if expect_header:
        if obj.htype == HeaderType.SEQ_DATA:
            print("SEQ data", obj.data, obj.uncorrected_errors)
            if obj.seq_eof:
                # last block
                print("End of file")
        else:
            print("header", obj.htype, obj.start, obj.end, obj.name, obj.uncorrected_errors)
            if obj.htype in (HeaderType.PRG_RELOC, HeaderType.PRG):
                expect_header = False
    else:
        print("PRG data", obj.data)
        expect_header = True
