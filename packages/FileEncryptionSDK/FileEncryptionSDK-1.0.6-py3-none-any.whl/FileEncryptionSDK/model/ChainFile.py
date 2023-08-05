



class ChainFile:
    """
    生成的文件信息
    """
    def __init__(self, appId=None, ownerId=None, fileName=None, fileURL=None, secretKey=None):
        # 文件所属AppID
        self.appId = appId
        # 文件所有者ID
        self.ownerId = ownerId
        # 文件名
        self.fileName = fileName
        # 文件路径
        self.fileURL = fileURL
        # 文件加密秘钥
        self.secretKey = secretKey
