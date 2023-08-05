

class OperationResult:
    """
    封装动作执行结果
    """
    def __init__(self, successful=True, msg=None, data=None):
        self.successful = successful
        self.msg = msg
        self.data = data

    def success(self, data):
        """
        Args:
            data: 操作后返回的数据
        Returns:
            成功返回
        """
        return OperationResult(True, "成功", data)

    def fail(self , msg, data):
        """
        Args:
            msg: 操作结果描述
            data: 操作后返回的数据
        Returns:
            失败返回
        """
        return OperationResult(False, msg, data)