#!/usr/bin/python3

import os
import re
import sys
import multiprocessing

from modules.Spliter import Spliter, IsNotDataError


class Voror(object):
    def __init__(self):
        self._odir = None
        self._opaths = None
        self._coors = None

    def split(self, ipath, odir='data'):
        self._odir = odir
        spliter = Spliter()

        try:
            self._coors = spliter.parse(ipath)
        except FileNotFoundError as e:
            print('FileNotFoundError: Cannot find input file!')
            exit(0)
        except IsADirectoryError as e:
            print('IsADirectoryError: Input file is a direcotry!')
            exit(0)
        except IsNotDataError as e:
            print(e)
            exit(0)

        self._opaths = spliter.write(odir)
        return self

    def run(self):
        for i, coor in enumerate(self._coors):
            command = 'voro++ -g {} {} {} {} {} {} {}'.format(
                *coor, self._opaths[i])
            print('Start to process frame {}...'.format(i))
            os.system(command)


def main():
    voror = Voror()
    if len(sys.argv) == 1:
        print("+--------------------------------------+")
        print("| __     __                            |")
        print("| \ \   / /__  _ __ ___  _ __          |")
        print("|  \ \ / / _ \| '__/ _ \| '__|         |")
        print("|   \ V / (_) | | | (_) | |            |")
        print("|    \_/ \___/|_|  \___/|_|   by Cycoe |")
        print("+--------------------------------------+")
        print('\nUsage:\t./Voror.py [name of data file] [path to output]')
        exit(0)
    if len(sys.argv) == 2:
        voror.split(sys.argv[1])
    else:
        voror.split(sys.argv[1], sys.argv[2])
    voror.run()


if __name__ == '__main__':
    main()
