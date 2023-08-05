

class FileInfo:
    """
    文件信息
    """
    def __init__(self ,key=None, localPath=None):
        # 文件上链唯一识别key
        self.key = key
        # 文件本地绝对路径
        self.localPath = localPath