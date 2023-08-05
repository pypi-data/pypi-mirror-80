

class ChainModel:
    """
    区块链信息
    """
    def __init__(self, appId=None, userId=None, privateKey=None, userTxId=None, certName=None, certTxId=None, cert=None, errorMsg=None):
        self.appId = appId
        self.userId = userId
        self.privateKey = privateKey
        self.userTxId = userTxId
        self.certName = certName
        self.certTxId = certTxId
        self.cert = cert
        self.errorMsg = errorMsg