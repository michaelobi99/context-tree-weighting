from ArithEnc import compressFile
from time import perf_counter
from ArithDec import expandFile
import os


class Timer():
    def __init__(self):
        self.__start: float = 0
        self.__stop: float = 0

    def start(self):
        self.__start = perf_counter()

    def stop(self):
        self.__stop = perf_counter()

    def time(self):
        return self.__stop - self.__start


def main():
    timer = Timer()
    depth = 48
    total = 0.0
    filename = ["textFile1.txt"] #r'calgarycorpus\bib', r'calgarycorpus\book1', r'calgarycorpus\book2', r'calgarycorpus\geo',
    #             r'calgarycorpus\news', r'calgarycorpus\obj1', r'calgarycorpus\obj2', r'calgarycorpus\paper1',
    #             r'calgarycorpus\paper2', r'calgarycorpus\pic', r'calgarycorpus\progc', r'calgarycorpus\progl',
    #             r'calgarycorpus\progp', r'calgarycorpus\trans']
    filename2 = "textFile2.txt"
    filename3 = "textFile3.txt"
    for file in filename:
        print('--------------------------------------------------------------------')
        print('compression started')
        timer.start()
        compressFile(file, filename2, depth)
        timer.stop()
        print(f'compression time = {timer.time()} seconds')
        timer.start()
        expandFile(filename2, filename3, depth)
        timer.stop()
        print(f'original filesize = {os.path.getsize(file)}')
        print(f'compressed filesize = {os.path.getsize(filename2)}')
        print(f'expanded filesize = {os.path.getsize(filename3)}')
        print(f'expansion time = {timer.time()} seconds')
        eff = (os.path.getsize(filename2) * 8) / os.path.getsize(file)
        print(f'compression efficiency = {eff}')
        total += eff
        print('--------------------------------------------------------------------')
    print(f'average compression efficiency = {total}')

main()