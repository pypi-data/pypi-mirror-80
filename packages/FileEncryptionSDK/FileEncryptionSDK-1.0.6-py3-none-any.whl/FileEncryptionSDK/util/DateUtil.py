from datetime import datetime


def getDateWithMS():
    """
    获取yyyyMMddhhmmssSSS格式时间戳
    Returns:
        获取当前日期，需要时分秒毫秒
    """
    signtime = datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
    print(signtime)
    return signtime