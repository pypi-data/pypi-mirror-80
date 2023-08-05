
__all__ = [
    'checkFileOnTheChain',
    'fileInfoUpChain',
    'logFileUploadChain',
    'private_key_signature',
    'public_key_verify',
    'fileAuthorize',
    'logChain',
    'queryFileChain',
    'logFileDownloadChain',
    'logFileDecodeChain',
    ]


import json
import random

import rsa
from model import UserAction
from model.ChainData import ChainData
from model.ChainResult import ChainResult
from util.DateUtil import getDateWithMS
from util.DsRepChainUtil import authorize, getCryptionWithPrivateKey, getFileInfo, logUpChain, fileUpChain
from util.EncryptionUtil import aesDecrypt
from util.StringUtil import chainUserId
from util.SystemUtil import getCurrentIP
from base64 import b64encode, b64decode

from Crypto.Cipher import PKCS1_v1_5

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA



def fileHash(key, fileEncryption):
    return str(fileEncryption.chainModel.appId) + "_" + key


def checkFileOnTheChain(key, fileOwnerId, fileEncryption):
    """
    检测文件是否已经上链
    Args:
        key文件唯一查询Key
    Returns:
        检测结果
    """
    chainResult = ChainResult()
    chainResult.result.code = 200
    print("checkFileOnTheChain, key:"+key+","+"fileOwnerId:"+fileOwnerId)

    strFileHash = fileHash(key, fileEncryption)
    #getCryptionWithPrivateKey(strFileHash, fileOwnerId)

    return chainResult

def fileInfoUpChain(key, fileInfo, fileEncryption):
    """
    文件信息上链（文件上传至服务器时）
    [数据上链]
    Args:
        key: 文件唯一识别Key
        fileInfo: 文件信息
    Returns:
        上链结果
    """
    chainResult = ChainResult()
    chainResult.result.code = 200
    print("fileInfoUpChain, key:"+key+","+"fileInfo:"+fileInfo)
    strFileHash = fileHash(key, fileEncryption)
    fileUpChain(strFileHash, fileInfo)
    return chainResult

def logFileUploadChain(fileName, fileEncryption):
    """
    文件上传日志上链
    Args:
        fileName: 文件名
    Returns:
        上链结果
    """
    chainResult = ChainResult()
    chainResult.result.code = 200
    #print("logFileUploadChain, fileName:"+fileName)
    #print(UserAction.UserAction.FILEUP.value)
    logChain(fileName, UserAction.UserAction.FILEUP.value, fileEncryption)
    return chainResult

def private_key_signature(message, privateKey):
    """
    私钥签名
    """
    #use private key certificate to signature
    privatekey = RSA.importKey(privateKey)
    signer = PKCS1_v1_5.new(privatekey)
    return b64encode(signer.sign(SHA.new(message)))

def public_key_verify(message, sign, publicKey):
    """
    公钥验签
    """
    #use public key certificate to verify
    publickey = RSA.importKey(publicKey)
    verifier = PKCS1_v1_5.new(publickey)
    return verifier.verify(SHA.new(message), b64decode(sign))



def fileAuthorize(param, fileEncryption):
    """
    文件授权
    Args:
        param: 授权参数
    Returns:
        授权结果
    """
    chainModel = fileEncryption.chainModel
    strFileHash = fileHash(param.key, fileEncryption)
    privateKey = chainModel.privateKey
    # 生成签名
    #sign = rsa.sign(strFileHash, privateKey, 'SHA-1')
    #sign = privateKey.sign(strFileHash, ec.ECDSA(hashes.SHA1()))
    #sign = private_key_signature(strFileHash, privateKey)

    # 随机生成秘钥对（公钥 + 私钥）
    (pubkey, privkey) = rsa.newkeys(1024)

    # 私钥加密
    fileSecret = rsa.encrypt(fileEncryption.fileInfoEncryptKey, privkey)
    markerInfo = {"pk":pubkey, "fileSecret":fileSecret}
    return authorize(privateKey, chainModel.userId, chainModel.certName, fileHash,
                     None, param.getAuthorizeValue(), markerInfo)


def logChain(fileName, userAction, fileEncryption):
    """
    日志上链
    Args:
        fileName: 文件名
        userAction: 用户动作
    Returns:
        上链结果
    """
    return logUpChain(generateKey(userAction, fileEncryption), value(fileName, userAction, "", fileEncryption))


def value(fileName, action, remark, fileEncryption):
    value = ChainData()
    value.action = action
    value.appid = fileEncryption.chainModel.appId

    value.ip = getCurrentIP()
    value.coctime = getDateWithMS()
    value.version = '1.0'
    value.remark = remark

    content = ""
    userId = fileEncryption.chainModel.userId
    print(str(UserAction.UserAction.FILEUP.value))
    if action == UserAction.UserAction.FILEUP.value:
        content = "用户" + userId + "对" + fileName + "上传"
    elif action == UserAction.UserAction.FILEDOWN.value:
        content = "用户" + userId + "对" + fileName + "下载"
    elif action == UserAction.UserAction.DECODE.value:
        content = "用户" + userId + "对" + fileName + "解密"
    elif action == UserAction.UserAction.DATACOC.value:
        content = "用户" + userId + "对" + fileName + "上链"
    elif action == UserAction.UserAction.DATAQYC.value:
        content = "用户" + userId + "对" + fileName + "查询"

    value.content = content
    return str(value)


def generateKey(action, fileEncryption):
    key = 'DS-LOG-' + str(fileEncryption.chainModel.appId) + '-' + str(action) + '-' + getDateWithMS() + '-' + str(((random.randint(1,10)*9+1)*1000))
    return key

def queryFileChain(key, fileOwnerId, fileEncryption):
    """
    查询链上的文件信息
    Args:
        key: 文件唯一识别Key
        fileOwnerId: 文件所有者用户ID
    Returns:
        文件信息
    """
    # 查询文件对称加密秘钥
    chainModel = fileEncryption.getChainModel()
    privateKey = chainModel.getPrivateKey()
    strFileHash = fileHash(key, fileEncryption)

    # 生成签名
    sign = rsa.sign(fileHash, privateKey, 'SHA-1')
    fileOwnerId = chainUserId(fileEncryption.chainModel.getAppId(), fileOwnerId)
    jsonObject = getCryptionWithPrivateKey(privateKey, fileEncryption.chainModel.getUserId(),
                                           fileEncryption.chainModel.getCertName(),
                                            strFileHash, fileOwnerId, sign)

    # 取出密文和公钥
    pk = jsonObject.pk
    fileSecret = jsonObject.fileSecret

    # RSA解密出文件对称加密秘钥
    fileInfoSecretKey = rsa.decrypt(fileSecret, pk)

    # 查询文件私密信息
    fileSecretInfoResult = getFileInfo(privateKey, chainModel.getUserId(), chainModel.getCertName(), fileOwnerId, fileHash)

    # 解密
    fileSecretInfo = aesDecrypt(fileSecretInfoResult.reason, fileInfoSecretKey)
    chainFile = json.loads(fileSecretInfo)

    # 查询日志上链
    queryLogChain = logChain(chainFile.getFileName(), UserAction.DATAQYC, fileEncryption)

    return chainFile


def logFileDownloadChain(fileName, fileEncryption):
    """
    文件下载日志上链
    Args:
        fileName: 文件名
    Returns:
        上链结果
    """
    return logChain(fileName, UserAction.FILEDOWN, fileEncryption)


def logFileDecodeChain(fileName, fileEncryption):
    """
    解密文件日志上链
    Args:
        fileName: 文件名
    Returns:
        上链结果
    """
    return logChain(fileName, UserAction.DECODE, fileEncryption)





