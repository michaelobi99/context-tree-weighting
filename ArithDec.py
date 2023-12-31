from BitIO import *
import math
from CTW import CTW

high, low, underflow, code = 0xffffffff, 0, 0, 0
shift = 31

def decodeBit(prob: float, input: bitFile):
    global high, low, underflow, code
    split = low + int(((high - low) * prob))
    bit = (code >= split)
    if bit:
        low = split
    else:
        high = split
    while True:
        if high & 0x80000000 == low & 0x80000000:
            pass
        elif (not (high & 0x40000000)) and (low & 0x40000000):
            code ^= (1 << 30)
            high ^= (1 << 30)
            low ^= (1 << 30)
        else:
            break
        low &= ((1 << shift) - 1)
        low <<= 1
        high &= ((1 << shift) - 1)
        high <<= 1
        high |= 1
        code &= ((1 << shift) - 1)
        code <<= 1
        code |= inputBit(input)

    return 1 if bit else 0

def initializeDecoder(input: bitFile):
    global code
    for i in range(32):
        code <<= 1
        code |= inputBit(input)

def fillContext(context, input, output, depth, fileSize):
    for i in range(depth):
        bit = inputBit(input)
        if i < fileSize:
            outputBit(output, bit)
            context.append(bit)
        if bit == 2:
            break


def expandFile(inputName: str, outputName: str, depth: int):
    input: bitFile = openInputBitFile(inputName)
    output: bitFile = openOutputBitFile(outputName)
    bytestream = []
    fileSize = 0
    # read original file size from compressed stream
    c = input.file.read(1)
    while c != b' ':
        bytestream.append(int.from_bytes(c))
        c = input.file.read(1)
    counter = len(bytestream) - 1
    for i in bytestream:
        fileSize += i * (10 ** counter)
        counter -= 1
    fileSize *= 8
    # ..............................................
    global high, low, underflow
    context = []
    fillContext(context, input, output, depth, fileSize)
    initializeDecoder(input)
    ctxTree = CTW(depth, context)
    #ctxTree = CTW(depth)
    counter = len(context)
    while counter < fileSize:
        p0 = math.exp(ctxTree.predict(0))
        ctxTree.update(0, reverse=True, temp=True)
        #p1 = math.exp(ctxTree.predict(1))
        #assert (abs(p0 + p1 - 1) < 1e-6)

        bit = decodeBit(p0, input)
        outputBit(output, bit)
        # model
        ctxTree.update(bit, reverse=False, temp=False)
        # arithmetic coding
        counter += 1
    else:
        closeInputBitFile(input)
        closeOutputBitFile(output)
