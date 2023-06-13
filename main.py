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
    filename = "textFile1.txt"
    filename2 = "textFile2.txt"
    filename3 = "textFile3.txt"
    print('compression started')
    timer.start()
    compressFile(filename, filename2, depth)
    timer.stop()
    print(f'compression time = {timer.time()} seconds')
    timer.start()
    expandFile(filename2, filename3, depth)
    timer.stop()
    print(f'original filesize = {os.path.getsize(filename)}')
    print(f'compressed filesize = {os.path.getsize(filename2)}')
    print(f'expanded filesize = {os.path.getsize(filename3)}')
    print(f'expansion time = {timer.time()} seconds')

main()