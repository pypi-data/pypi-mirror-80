__all__ = [
    'fileUpChain',
    'getCryptionWithPrivateKey',
    'registerBlockChain',
    'authorize',
    'getFileInfo',
    'logUpChain',
    ]


import json
from google.protobuf.text_format import MessageToString
from rechain.Client import Client
import rechain.peer_pb2 as peer

host = 'http://baas.repchain.net.cn/api/app/123/dschain'
jksPath = 'D:\\repchain1.0\\121000005l35120456.node1.pem'
password = '123'
alias = '121000005l35120456.node1'

# 以下为RepChian1.0调用存证合约参数/先部署后调用
tranType = peer.Transaction.CHAINCODE_INVOKE
chaincodeName = "DSChain"
chaincodeVersion = 5
creditCode = "121000005l35120456"
certName = "node1"

client = Client(host, jksPath, password, alias, creditCode, certName)

def fileUpChain(fileHash, cryptInfo):
    """
    文件信息上链
    """
    dict = {}
    dict['fileHash'] = fileHash
    dict['signature'] = client.sign(fileHash)
    dict['cryptInfo'] = cryptInfo
    fileInfo = {}
    dict['fileInfo'] = fileInfo
    param = json.dumps(dict)

    # 构造交易
    trans = client.createTransaction("fileProof", param)
    print(MessageToString(trans))

    # 发送交易
    result = client.postTranByString(trans)
    print(result.text)

def getCryptionWithPrivateKey(fileHash, ownerCreditCode):
    """
    获取解密信息
    """
    dict = {}
    dict['fileHash'] = fileHash
    dict['signature'] = client.sign(fileHash)
    dict['ownerCreditCode'] = ownerCreditCode
    param = json.dumps(dict)

    # 构造交易
    trans = client.createTransaction("getCryptionWithPermission", param, client.creditCode, client.certName)
    print(MessageToString(trans))

    # 发送交易
    result = client.postTranByString(trans)
    print(result.text)

def registerBlockChain(openid):
    """
    注册用户 账户和证书注册已分离，需要分别注册 账户和证书注册过后，使用对用的密钥初始化客户端构建签名交易
    """
    pass

def authorize(fileHash, ownerSignature, authMap, bcKeyMap):
    """
    授权
    """
    dict = {}
    dict['fileHash'] = fileHash
    dict['ownerSignature'] = client.sign(fileHash)
    dict['authMap'] = {'chain_27_805': {'expire': str(time), 'surplus': '12'}}
    dict['bckeyMap'] = {'sk': '12345678', 'fileSecret': '12345678'}
    param = json.dumps(dict)

    # 构造交易
    trans = client.createTransaction("getCryptionWithPermission", param, client.creditCode, client.certName)
    print(MessageToString(trans))

    # 发送交易
    result = client.postTranByString(trans)
    print(result.text)

def getFileInfo(privateKey, userId, certName, fileOwnerId, fileHash):
    """
    查询链上文件信息
    """

    pass

def logUpChain(oderId, content):
    """
    日志上链
    """

    dict = {}
    dict['logId'] = oderId
    dict['logContent'] = content
    param = json.dumps(dict)

    # 构造交易
    trans = client.createTransaction("logProof", param)
    print(MessageToString(trans))

    # 发送交易
    result = client.postTranByString(trans)
    print(result.text)

