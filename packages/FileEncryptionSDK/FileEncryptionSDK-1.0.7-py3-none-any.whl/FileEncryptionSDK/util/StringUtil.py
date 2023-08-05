__all__ = [
    'notEmpty',
    'hdfsUrlValid',
    'httpUrlValid',
    'httpUrlValid',
    'chainUserId',
    ]

def notEmpty(content):
    """
    检测字符串是否不为空或空串
    Args:
        content 待检测字符串
    Returns:
        true: 字符串不为空或空串 | false: 字符串为空或者空串
    """
    return len(content) != 0


def hdfsUrlValid(url):
    """
    检测HDFS远程地址有效性
    Args:
        url 待检测URL
    Returns:
        true: 有效的HDFS地址 | false: 无效的HDFS地址
    """
    return notEmpty(url) and url.startswith("hdfs://")

def httpUrlValid(url):
    """
    检测HTTP地址有效性
    Args:
        url 待检测URL
    Returns:
        true: 有效的HTTP地址 | false: 无效的HTTP地址
    """
    return notEmpty(url) and (url.startswith("https://") or url.startswith("http://"))

def chainUserId(appId, userId):
    """
    Args:
        appId  应用ID
        userId 用户ID
    Returns:
        区块链用户ID
    """
    return "chain_" + str(appId) + "_" + userId