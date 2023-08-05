import enum


class HeaderType(enum.IntEnum):
    PRG_RELOC = 1
    SEQ_DATA = 2
    PRG = 3
    SEQ_HDR = 4
    EOT = 5
