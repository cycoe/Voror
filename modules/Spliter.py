import os
import re


class IsNotDataError(Exception):
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return 'IsNotDataError: {} is not a data file!'.format(self._path)


class Spliter(object):
    def __init__(self):
        self._data = None

    def parse(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isdir(path):
            raise IsADirectoryError
        if not path.endswith('dat'):
            raise IsNotDataError(path)

        data = []
        flag = False

        with open(path, 'r') as fp:
            frame = []
            for line in fp.readlines():
                if re.match('.*Atoms.*', line):
                    if flag:
                        data.append(frame)
                    frame = []
                    frame.append(line)
                    flag = True
                else:
                    frame.append(line)

            data.append(frame)

        self._data = data
        return data

    def write(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

        for i, frame in enumerate(self._data):
            with open(os.sep.join((path, 'frame-{}.dat'.format(i))),
                      'w') as fp:
                fp.writelines(frame[5:])

        return self
