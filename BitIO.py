class bitFile():
    def __init__(self, file, mask, rack):
        self.file = file
        self.mask = mask
        self.rack = rack

def openOutputBitFile(name: str):
    file = open(name, 'wb')
    bitfile = bitFile(file, 0x80, 0)
    return bitfile

def openInputBitFile(name: str):
    file = open(name, 'rb')
    bitfile = bitFile(file, 0x80, 0)
    return bitfile

def closeOutputBitFile(bitfile: bitFile):
    if bitfile.mask != 0x80:
        bitfile.file.write(int.to_bytes(bitfile.rack))
    bitfile.file.close()

def closeInputBitFile(bitfile: bitFile):
    bitfile.file.close()

def outputBit(bitfile: bitFile, bit: int):
    if bit:
        bitfile.rack |= bitfile.mask
    bitfile.mask >>= 1
    if bitfile.mask == 0x00:
        bitfile.file.write(int.to_bytes(bitfile.rack))
        bitfile.rack = 0
        bitfile.mask = 0x80

def outputBits(bitFile: bitFile, code: int, count: int):
    mask: int = 1 << (count - 1)
    while mask != 0:
        outputBit(bitFile, code & mask)
        mask >>= 1

def inputBit(bitfile: bitFile):
    if bitfile.mask == 0x80:
        bitfile.rack = bitfile.file.read(1)
    if len(bitfile.rack) == 0:
        return 2
    value = ord(bitfile.rack) & bitfile.mask
    bitfile.mask >>= 1
    if bitfile.mask == 0:
        bitfile.mask = 0x80
    return 1 if value != 0 else 0

def inputBits(bitfile: bitFile, count: int):
    mask: int = 1 << (count - 1)
    value: int = 0
    while mask != 0:
        if bitfile.mask == 0x80:
            bitfile.rack = bitfile.file.read(1)
            if bitfile.rack == '':
                return 2
        if ord(bitfile.rack) & bitfile.mask:
            value |= mask
        mask >>= 1
        bitfile.mask >>= 1
        if bitfile.mask == 0:
            bitfile.mask = 0
    return value