

class FEException(Exception):

    def __init__(self):
        self.appId = ''
        self.userId = ''
        self.privateKey = ''
        self.userTxId = ''
        self.certName = ''
        self.certTxId = ''
        self.cert = ''
        self.errorMsg = ''
