import json

from pip._vendor import requests

from model.ChainModel import ChainModel
from util.DsRepChainUtil import registerBlockChain
from util.StringUtil import httpUrlValid, notEmpty, chainUserId

class FileEncryption:

    def __init__(self, chainModel=None, fileEncryptKey=None, fileInfoEncryptKey=None):
        # 注册区块链信息
        self.chainModel = chainModel
        # 文件内容加密秘钥
        self.fileEncryptKey = fileEncryptKey
        # 文件信息加密秘钥（文件信息含文件内容加密秘钥，文件下载地址等）
        self.fileInfoEncryptKey = fileInfoEncryptKey

    def authentication(self, authenticationURL, appId, userId):
        """
         * SDK初始化
         *
         * @param authenticationURL    认证地址
         * @param appId                应用ID
         * @param userId               用户ID
         * @param logSwitch            日志开关
         * @return true: 初始化成功 | false: 初始化失败
        """
        try:
            if bool(1-httpUrlValid(authenticationURL)):
                raise Exception("未设置认证地址或该地址无效")
            if appId is None or appId <= 0:
                raise Exception("未设置AppId或AppId无效")
            if bool(1-notEmpty(str(userId))):
                raise Exception("未设置UserId或UserI无效")

            # 校验AppId有效性
            datas = {"id" : appId}
            resp = requests.get(authenticationURL + "/api/ecAppInfo/checkAppId", params=datas)
            result = json.loads(resp.text)
            print(result['data'])
            if bool(1-result['data']):
                raise Exception("无效的AppId")

            ##根据服务器返回结果再决定是否注册用户区块链信息
            datas = {"appId": appId, "userId": userId}
            resp = requests.get(authenticationURL + "/api/sysUserChainInfo/getUserChainInfo", params=datas)
            result = json.loads(resp.text)
            if result['data']:
                self.chainModel.appId = result['data']['appId']
                self.chainModel.userId = result['data']['userId']
                self.chainModel.userTxId = result['data']['userTxId']
                self.chainModel.privateKey = result['data']['privateKey']
                self.chainModel.certName = result['data']['certName']
                self.chainModel.certTxId = result['data']['certTxId']
                self.chainModel.cert = result['data']['cert']
                print(self.chainModel.userId)
        except Exception as err:
            print(err)
        finally:
            print("authentication end")