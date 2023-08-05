

class FileAuthorize:
    """
    文件授权
    """
    def __init__(self, key=None, authorize=None):
        self.key = key
        self.authorize = authorize

    def getAuthorizeValue(self):
        auth = {'expire':self.authorize.expire, 'surplus':self.getAuthorize().surplus}
        value = {self.authorize.userId : auth}
        return value