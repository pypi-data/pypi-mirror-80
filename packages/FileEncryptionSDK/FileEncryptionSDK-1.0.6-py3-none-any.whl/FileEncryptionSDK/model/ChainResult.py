from model.Result import Result


class ChainResult:
    """
    上链结果
    """
    def __init__(self, txid=None, err=None, result=None):
        self.txid = txid
        self.err = err
        self.result = Result()

    def failed(self):
        if (self.result is None or self.result.code != 200):
            return False
        else:
            return True
