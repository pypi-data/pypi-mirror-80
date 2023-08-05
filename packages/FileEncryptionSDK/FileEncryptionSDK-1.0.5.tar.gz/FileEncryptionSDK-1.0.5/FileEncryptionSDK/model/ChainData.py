
class ChainData:
    """
    上链数据
    """
    def __init__(self, action=None, appid=None, ip=None, coctime=None, version=None, content=None, remark=None):
        # 数据类型，对应key值中的ACTION值
        self.action = action
        # DS链后台申请的APPid值
        self.appid = appid
        # 本机IP地址
        self.ip = ip
        # 上链时间，用时间戳的形式
        self.coctime = coctime
        # sdk的版本号（非必填）
        self.version = version
        # 日志操作内容描述，可以为json格式
        self.content = content
        # 日志上链备注（非必填）
        self.remark = remark
