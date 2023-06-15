from BitIO import *
import math
from CTW import CTW
from os import path
high, low, underflow = 0xffffffff, 0, 0
shift = 31

def encodeBit(output: bitFile, bit: int, prob):
    global high, low, underflow
    if bit:
        low += int(((high - low) * prob))
    else:
        high = low + int(((high - low) * prob))

    while True:
        #print(f'low = {bin(low)}\nhigh = {bin(high)}')
        if high & 0x80000000 == low & 0x80000000:
            outputBit(output, high & 0x80000000)
        if high & 0x80000000 == low & 0x80000000:
            outputBit(output, high & 0x80000000)
            while underflow > 0:
                outputBit(output, (~high) & 0x80000000)
                underflow -= 1
        elif (not (high & 0x40000000)) and (low & 0x40000000):
            high |= (1 << 30)
            low &= ~(1 << 30)
            underflow += 1
        else:
            break
        low &= ((1 << shift) - 1)
        low <<= 1
        high &= ((1 << shift) - 1)
        high <<= 1
        high |= 1

def flushEncoder(output: bitFile):
    global high, underflow
    outputBit(output, high & 0x80000000)
    underflow += 1
    while underflow > 0:
        outputBit(output, (~high) & 0x80000000)
        underflow -= 1

def fillContext(context, input, output, depth):
    for i in range(depth):
        bit = inputBit(input)
        if bit == 2:
            break
        context.append(bit)
    for elem in context:
        outputBit(output, elem)
def compressFile(inputName: str, outputName: str, depth: int):
    input: bitFile = openInputBitFile(inputName)
    output: bitFile = openOutputBitFile(outputName)
    sizeArray = [int(x) for x in str(path.getsize(inputName))] + [32]
    output.file.write(bytes(sizeArray))
    global high, low, underflow
    context = []
    fillContext(context, input, output, depth)
    ctxTree = CTW(depth, context)
    high, low, underflow = 0xffffffff, 0, 0
    bit = inputBit(input)
    #counter = 0
    while bit != 2:
        p0 = math.exp(ctxTree.predict(0))
        ctxTree.update(0, reverse=True, temp=True)
        #p1 = math.exp(ctxTree.getLogPx(1))
        # assert (abs(p0 + p1 - 1) < 1e-6)
        #counter += 1
        ctxTree.update(bit, reverse=False, temp=False)
        # arithmetic coding
        encodeBit(output, bit, p0)
        bit = inputBit(input)
    else:
        flushEncoder(output)
        outputBits(output, 0, 32)
        closeInputBitFile(input)
        closeOutputBitFile(output)