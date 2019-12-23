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
        self._ipath = None
        self._data = None

    def parse(self, ipath):
        # Error if input file does not exist
        if not os.path.exists(ipath):
            raise FileNotFoundError
        # Error if input file is a direcotry
        if os.path.isdir(ipath):
            raise IsADirectoryError
        # Error if input file is not a data file
        if not ipath.endswith('dat'):
            raise IsNotDataError(ipath)

        self._ipath = ipath

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
        coors = []
        for frame in data:
            coor = []
            for index in range(3):
                limit = frame[index + 2].strip('\n').split(' ')
                limit = [item for item in limit if item != '']
                coor.extend([float(item) for item in limit])
            coors.append(coor)

        self._data = data
        return coors

    def write(self, path):
        # make the output direcotry if it didn't exist
        if not os.path.exists(path):
            os.mkdir(path)

        opaths = []
        # Write the frame into the dat file
        for i, frame in enumerate(self._data):
            opath = os.sep.join(
                (path, '{}-frame-{}.dat'.format(self._ipath.split('.')[0], i)))
            opaths.append(opath)
            with open(opath, 'w') as fp:
                # Skip the topmost 5 rows
                fp.writelines(frame[5:])

        self._clean()
        return opaths

    def _clean(self):
        del self._data
        self._data = None
