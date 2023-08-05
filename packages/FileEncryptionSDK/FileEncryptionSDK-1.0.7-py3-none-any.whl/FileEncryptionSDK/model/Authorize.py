

class Authorize:
    def __init__(self, userId=None, expire=None, surplus=None):
        # 被授权用户ID
        self.userId = userId
        # 授权文件过期时间
        self.expire = expire
        # 授权文件下载次数
        self.surplus = surplus

    def setExpireWithMin(self, min):
        self.expire = min * 60 * 1000;