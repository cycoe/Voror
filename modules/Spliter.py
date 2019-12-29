import os
import re


# 自定义异常
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
        """ Atom 文件拆分 """
        # 如果输入文件不存在，抛出异常
        if not os.path.exists(ipath):
            raise FileNotFoundError
        # 如果输入文件是个路径，抛出异常
        if os.path.isdir(ipath):
            raise IsADirectoryError
        # 如果输入文件的后缀不是 dat，抛出自定义异常
        if not ipath.endswith('dat'):
            raise IsNotDataError(ipath)

        data = []
        flag = False

        # 将输入文件按 frame 读取到 data 列表中
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

        # 将 data 列表中的数据格式化后存入 self._data 字典
        self._data = {}
        for i, frame in enumerate(data):
            # 为每一帧生成一个 tag 作为唯一标识符
            tag = '{}-frame-{}'.format(ipath.split('.')[0], i)
            self._data[tag] = {}

            # 读取盒子上下界
            coor = []
            for index in range(3):
                limit = frame[index + 2].strip('\n').split(' ')
                coor.extend([float(item) for item in limit if item != ''])

            self._data[tag]['coor'] = tuple(coor)  # 盒子上下界
            self._data[tag]['head'] = frame[0]  # 每一帧的第一行作为 header
            self._data[tag]['data'] = frame[5:]  # 实际的数据行
            self._data[tag]['opath'] = os.sep.join((opath, tag))  # 每一帧的输出文件路径

        # 如果储存输出帧的文件夹不存在，创建它
        if not os.path.exists(opath):
            os.mkdir(opath)

        # 写入每一帧的数据到对应的输出文件
        for tag in self._data.keys():
            with open(self._data[tag]['opath'], 'w') as fp:
                fp.writelines(self._data[tag]['data'])

        return self._data

    def merge(self, opath):
        """ 合并 vol 输出文件 """
        with open(opath, 'w') as fp:
            for tag in self._data.keys():
                fp.write('{}\n'.format(len(self._data[tag]['data'])))
                fp.write(self._data[tag]['head'])
                with open(self._data[tag]['opath'] + '.vol', 'r') as ip:
                    fp.writelines(ip.readlines())

        return self
