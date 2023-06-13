from BitIO import *
import math
from CTW import CTW
from os import path
high, low, underflow = 0xffff, 0, 0
shift = 15

def encodeBit(output: bitFile, bit: int, prob):
    global high, low, underflow
    #print(f'low = {bin(low)}\nhigh = {bin(high)}')
    if bit:
        low += int(((high - low) * prob))
    else:
        high = low + int(((high - low) * prob))

    while True:
        #print(f'low = {bin(low)}\nhigh = {bin(high)}')

        if high & 0x8000 == low & 0x8000:
            outputBit(output, high & 0x8000)
            #print("Got here lol")
            while underflow > 0:
                outputBit(output, (~high) & 0x8000)
                underflow -= 1
        elif (not (high & 0x4000)) and (low & 0x4000):
            high |= (1 << 14)
            low &= ~(1 << 14)
            underflow += 1
        else:
            return
        low &= ((1 << shift) - 1)
        low <<= 1
        high &= ((1 << shift) - 1)
        high <<= 1
        high |= 1

def flushEncoder(output: bitFile):
    global high, underflow
    outputBit(output, high & 0x8000)
    underflow += 1
    while underflow > 0:
        outputBit(output, (~high) & 0x8000)
        underflow -= 1


def compressFile(inputName: str, outputName: str, depth: int):
    input: bitFile = openInputBitFile(inputName)
    output: bitFile = openOutputBitFile(outputName)
    sizeArray = [int(x) for x in str(path.getsize(inputName))] + [32]
    output.file.write(bytes(sizeArray))
    global high, low, underflow
    high, low, underflow = 0xffff, 0, 0
    ctxTree = CTW(depth)
    bit = inputBit(input)
    #counter = 0
    while bit != 2:
        p0 = math.exp(ctxTree.getLogPx(0))
        #p1 = math.exp(ctxTree.getLogPx(1))
        # print(counter, ' ', p0, ' ', p1)
        # counter += 1
        #assert (abs(p0 + p1 - 1) < 1e-6)
        # model
        ctxTree.update(bit, reverse=False, temp=False)
        # arithmetic coding
        encodeBit(output, bit, p0)
        bit = inputBit(input)
    else:
        flushEncoder(output)
        outputBits(output, 0, 16)
        closeInputBitFile(input)
        closeOutputBitFile(output)