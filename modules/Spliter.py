import os
import re


class IsNotDataError(Exception):
    """ Error if input file is not a data file """
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return 'IsNotDataError: {} is not a data file!'.format(self._path)


class Spliter(object):
    def __init__(self):
        self._data = None

    def split(self, ipath, opath):
        # Error if input file does not exist
        if not os.path.exists(ipath):
            raise FileNotFoundError
        # Error if input file is a direcotry
        if os.path.isdir(ipath):
            raise IsADirectoryError
        # Error if input file is not a data file
        if not ipath.endswith('dat'):
            raise IsNotDataError(ipath)

        data = []
        flag = False

        # Read input file into the data list
        with open(ipath, 'r') as fp:
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

        # Calculate the box limits for all the frames
        self._data = {}
        for i, frame in enumerate(data):
            tag = '{}-frame-{}'.format(ipath.split('.')[0], i)
            self._data[tag] = {}

            coor = []
            for index in range(3):
                limit = frame[index + 2].strip('\n').split(' ')
                limit = [item for item in limit if item != '']
                coor.extend([float(item) for item in limit])
            self._data[tag]['coor'] = tuple(coor)
            self._data[tag]['head'] = frame[0]
            self._data[tag]['data'] = frame[5:]
            self._data[tag]['opath'] = os.sep.join((opath, tag))

        # make the output direcotry if it didn't exist
        if not os.path.exists(opath):
            os.mkdir(opath)

        for tag in self._data.keys():
            with open(self._data[tag]['opath'], 'w') as fp:
                # Skip the topmost 5 rows
                fp.writelines(self._data[tag]['data'])

        return self._data

    def merge(self, opath):
        with open(opath, 'w') as fp:
            for tag in self._data.keys():
                fp.write(self._data[tag]['head'])
                with open(self._data[tag]['opath'] + '.vol', 'r') as ip:
                    fp.writelines(ip.readlines())

        return self
