#!/usr/bin/python3

import os
import re
import sys
import multiprocessing

from modules.Spliter import Spliter, IsNotDataError


class Voror(object):
    def __init__(self):
        self._path = None
        self._data = None

    def split(self, path, direcotry='data'):
        self._path = direcotry
        spliter = Spliter()

        try:
            self._data = spliter.parse(path)
        except FileNotFoundError as e:
            print('FileNotFoundError: Cannot find input file!')
            exit(0)
        except IsADirectoryError as e:
            print('IsADirectoryError: Input file is a direcotry!')
            exit(0)
        except IsNotDataError as e:
            print(e)
            exit(0)

        spliter.write(direcotry)
        return self

    def run(self):
        for i, frame in enumerate(self._data):
            coor = []
            for index in range(3):
                pair = frame[index + 2].strip('\n').split(' ')
                pair = [item for item in pair if item != '']
                coor.extend([float(item) for item in pair])
            command = 'voro++ -g {} {} {} {} {} {} {}'.format(
                *coor, os.sep.join((self._path, 'frame-{}.dat'.format(i))))
            print('Start to process frame {}...'.format(i))
            os.system(command)


def main():
    voror = Voror()
    if len(sys.argv) == 1:
        print('Usage:')
        print('./Voror.py [name of data file] [path to output]')
        exit(0)
    if len(sys.argv) == 2:
        voror.split(sys.argv[1])
    else:
        voror.split(sys.argv[1], sys.argv[2])
    voror.run()


if __name__ == '__main__':
    main()
