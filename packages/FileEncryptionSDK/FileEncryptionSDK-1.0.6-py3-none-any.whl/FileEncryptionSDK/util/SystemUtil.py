import socket


def getCurrentIP():
    """
    获取本机IP（内网）
    Returns:
        本机IP（内网）
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

        return ip