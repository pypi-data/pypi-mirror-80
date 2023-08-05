


class ChainUploadParam:
    """
    文件上链参数
    """
    def __init__(self, key, uploadFile, fileEncryptKey):
        # 文件上链唯一识别key
        self.key = key
        # 待上传文件
        self.uploadFile = uploadFile
        # 文件内容加密秘钥
        self.fileEncryptKey = fileEncryptKey