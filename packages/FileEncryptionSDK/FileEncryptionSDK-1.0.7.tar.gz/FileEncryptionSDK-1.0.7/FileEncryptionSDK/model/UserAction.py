from enum import Enum


class UserAction(Enum):

    # 文件上传日志动作
    FILEUP = 1
    # 文件下载日志动作
    FILEDOWN = 2
    # 文件解密日志动作
    DECODE = 3
    # 数据上链日志动作
    DATACOC = 4
    # 链上获取数据日志动作
    DATAQYC = 5