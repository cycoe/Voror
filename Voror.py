#!/usr/bin/python3

import os
import re
import sys
import multiprocessing

from modules.Spliter import Spliter, IsNotDataError


class Voror(object):
    def __init__(self):
        self._odir = None
        self._data = None
        self._spliter = Spliter()

    def split(self, ipath, odir='data'):
        self._odir = odir

        try:
            self._data = self._spliter.split(ipath, odir)
        except FileNotFoundError as e:
            print('FileNotFoundError: Cannot find input file!')
            exit(0)
        except IsADirectoryError as e:
            print('IsADirectoryError: Input file is a direcotry!')
            exit(0)
        except IsNotDataError as e:
            print(e)
            exit(0)

        return self

    def run(self):
        for i, tag in enumerate(self._data.keys()):
            command = 'voro++ -g {} {} {} {} {} {} {}'.format(
                *self._data[tag]['coor'], self._data[tag]['opath'])
            print('Start to process frame {}...'.format(i))
            # 用shell运行command
            os.system(command)

    def merge(self, opath='total.vol'):
        print('Start to merge files...')
        self._spliter.merge(opath)


def main():
    voror = Voror()
    # sys.argv 代表了命令行参数（运行命令时后面跟的参数）
    # 输出帮助信息
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
    # 输入两个参数 ：代码名 读入的文件名
    if len(sys.argv) == 2:
        voror.split(sys.argv[1])
    # 输入三个参数：代码名 读入的文件名 输出的文件夹名
    else:
        voror.split(sys.argv[1], sys.argv[2])
    voror.run()
    voror.merge()


if __name__ == '__main__':
    main()
