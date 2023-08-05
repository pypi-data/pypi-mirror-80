import json
import os

from model.ChainFile import ChainFile
from model.FileInfo import FileInfo
from pathlib import Path

from model.OperationResult import OperationResult
from util import FileUtil, ChainDataUtil
from util.ChainDataUtil import fileInfoUpChain, logFileUploadChain, fileAuthorize, queryFileChain, logFileDownloadChain, \
    logFileDecodeChain
from util.EncryptionUtil import aesEncrypt
from util.StringUtil import hdfsUrlValid, notEmpty, httpUrlValid


class FEServer:
    def __init__(self, mConfig):
        self.mConfig = mConfig

    def init(self, config):
        if (bool(1-httpUrlValid(config.depositoryURL))):
            print("未设置远程服务地址或该地址无效")
            return False

        if (bool(1-notEmpty(config.depositoryDirPath))):
            print("未设置远程目录地址")
            return False

        self.mConfig = config
        return True

    def upload(self, key, uploadFile, fileEncryptKey, fileEncryption, client):
        """
         * 文件上传上链
         * 《流程》
         * 1、校验文件Key是否已经上链
         * 2、对本地待上传文件进行加密
         * 3、上传文件至HDFS服务器
         * 4、删除本地已加密文件
         * 5、对文件信息进行对称加密
         * 6、加密文件信息上链
         * 7、上传文件日志上链
         *
         * @param param 上传文件参数
         * @return 上传结果
        """
        fileInfo = FileInfo()
        operationResult = OperationResult()

        try:
            if key == '':
                print("无效的文件唯一识别Key")

            fileInfo.key = key
            my_file = Path(uploadFile)
            if my_file.is_file():
                print("指定的文件存在")
            else:
                print("找不到本地文件")

            if my_file.is_dir():
                print("无法上传文件夹")

            fileInfo.localPath = uploadFile

            # 检查文件是否上链
            print(fileEncryption.chainModel.userId)
            fileChain = ChainDataUtil.checkFileOnTheChain(key, fileEncryption.chainModel.userId, fileEncryption)
            if bool(1-fileChain.failed()):
                print("文件[Key: " + key + "]已上链")

            # 本地文件异或加密
            newFilePath = FileUtil.encFile(uploadFile, fileEncryptKey)
            (path, fileName) = os.path.split(newFilePath)
            #remoteFileURL = self.mConfig.getDepositoryURL() + self.mConfig.getDepositoryDirPath() + "/" + fileName
            remoteFileURL = self.mConfig.depositoryDirPath + "/" + fileName

            # 上传文件
            # clientStatus = client.status(remoteFileURL, False)
            # if clientStatus is None:
            #     client.upload(self.mConfig.depositoryDirPath, newFilePath)

            # 删除本地加密文件
            os.remove(newFilePath)

            # 生成文件信息
            chainFile = ChainFile()
            chainFile.appId = fileEncryption.chainModel.appId
            chainFile.ownerId = fileEncryption.chainModel.userId
            chainFile.fileName = fileName
            chainFile.fileURL = remoteFileURL
            chainFile.secretKey = fileEncryption.fileEncryptKey
            json_str = json.dumps(chainFile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

            # 使用AES对文件信息进行对称加密
            cipherText = aesEncrypt(str(fileEncryption.fileInfoEncryptKey), json_str)

            # 文件信息上链
            # fileInfoChain = fileInfoUpChain(key, cipherText, fileEncryption)
            # if bool(1-fileInfoChain.failed()):
            #     raise Exception(fileInfoChain.err)

            # 上传文件日志上链
            uploadLogChain = logFileUploadChain(fileName, fileEncryption)
            if bool(1-uploadLogChain.failed()):
                raise Exception(uploadLogChain.err)

            return operationResult.success(fileInfo)

        except Exception as err:
            print(err)
            return operationResult.fail(err, fileInfo)
        except IOError as err:
            print(err)
            return operationResult.fail("文件上传失败", fileInfo)

    def authorize(self, authorize, fileEncryption):
        operationResult = OperationResult()

        try:
            if bool(1-notEmpty(authorize.key)):
                raise Exception("无效的文件唯一识别Key")

            # 文件授权
            authorizeChain = fileAuthorize(authorize, fileEncryption)
            if (authorize.failed()):
                raise Exception(authorizeChain.err)

            return operationResult.success(True)

        except Exception as err:
            print(err)
            return operationResult.fail(err, False)

    def download(self, key, fileOwnerId, downloadDirPath, fileEncryption, client):
        """
         * 下载文件
         * 《流程》
         * 1、查询文件链上信息
         * 2、解密文件链上信息
         * 3、查询文件日志上链
         * 4、下载文件至本地下载目录
         * 5、对下载文件进行解密
         * 6、解密日志上链
         * 7、删除源文件保留解密后的文件
         *
         * @param key 文件唯一查询key
         * @param fileOwnerId 文件所有者ID
         * @param downloadDirPath 下载目录
         * @return 下载结果
        """
        fileInfo = FileInfo()
        fileInfo.key = key
        try:
            # 检查下载路径
            if (downloadDirPath.is_file() or downloadDirPath.is_dir()):
                raise Exception("无效的下载路径[" + downloadDirPath + "]")

            # 查询链上的文件信息
            chainFile = queryFileChain(key, fileOwnerId, fileEncryption)

            # 下载文件
            if (client.download(chainFile.fileURL, downloadDirPath+"/"+chainFile.fileName)):
                raise Exception("文件下载失败")

            # 下载日志上链
            logChain = logFileDownloadChain(chainFile.getFileName(), fileEncryption)
            if bool(1-logChain.failed()):
                raise Exception(logChain.err)

            # 文件解密
            newFilePath = FileUtil.encFile(downloadDirPath+chainFile.getFileName(), chainFile.getSecretKey())

            # 解密日志上链
            decodeChain = logFileDecodeChain(chainFile.getFileName())
            if bool(1-decodeChain.failed()):
                raise Exception(decodeChain.err)

            # 删除下载的源文件并将解密后的文件更名为源文件名
            os.remove(downloadDirPath+chainFile.getFileName())
            os.rename(newFilePath, downloadDirPath+chainFile.getFileName())
            fileInfo.setLocalPath(newFilePath)
            return fileInfo
        except Exception as err:
            print(err)




