import base64

from cryptography.hazmat.primitives.asymmetric import ec

import rechain.peer_pb2 as peer
import time
from google.protobuf import timestamp_pb2
import uuid
import cryptography.hazmat.primitives.serialization as serial
import requests
import json
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Client:

    def __init__(self, host, jksPath, password, alias, creditCode, certName):
        self.host = host
        self.jksPath = jksPath
        self.password = password
        self.alias = alias
        self.creditCode = creditCode
        self.certName = certName

    def createTransaction(self, chaincodeInputFunc, param):
        trans = peer.Transaction()
        trans.id = str(uuid.uuid4())
        trans.cid.version = 5
        trans.cid.chaincodeName = "DSChain"
        trans.type = peer.Transaction.CHAINCODE_INVOKE
        trans.ipt.function = chaincodeInputFunc
        trans.ipt.args.append(param)
            
        # 生成时间戳
        # now = time.time()
        # seconds = int(now)
        # nanos = int((now - seconds) * 10**9)
        # deploy时取脚本内容hash作为 chaincodeId/name
        # invoke时调用者应该知道要调用的 chaincodeId
        # cid = peer.ChaincodeId()
        # cid.version = chaincodeVersion
        # cid.chaincodeName = chaincodeName
        # 构建运行代码
        # cip = peer.ChaincodeInput()
        # cip.function = chaincodeInputFunc
        # cip.args.append(param)
        # # 初始化链码
        # chaincodeDeploy = peer.ChaincodeDeploy()
        # chaincodeDeploy.timeout = 1000
        # chaincodeDeploy.code_package = spcPackage.encode('utf-8')
        # chaincodeDeploy.legal_prose = ""
        # chaincodeDeploy.ctype = ctype

        # trans.cid = cid

        # trans.payload.CopyFrom(chaincodeDeploy)
        # trans.metadata =  ''.encode('utf-8')
        # trans.timestamp.CopyFrom(timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos))
        # trans.confidentialityLevel = peer.PUBLIC
        # trans.confidentialityProtocolVersion = 'confidentialityProtocolVersion-1.0'
        # trans.nonce = 'nonce'.encode('utf-8')
        # trans.toValidators = 'toValidators'.encode('utf-8')
        # trans.signature = ''.encode('utf-8')

        # 构造证书（短地址）
        input_file = open(self.jksPath, 'rb')
        input = input_file.read()
        # input_file.close()
        
        # cert = load_pem_x509_certificate(input, default_backend())
        # pbkey = cert.public_key()
        # jks转换为pem文件后需要6位密码，这里是123456
        pvkey = serial.load_pem_private_key(input, '123456'.encode('utf-8'), default_backend())
        #privateKey = "-----BEGIN PRIVATE KEY-----MIGNAgEAMBAGByqGSM49AgEGBSuBBAAKBHYwdAIBAQQgPtHT816wJBatnif8laVoyW0R5NqtMiMkmECOYEAIzSWgBwYFK4EEAAqhRANCAASlh+oDBPdwHEkpQT4/g4RX9ubP7jMM2QodiFtsnv+ObQ3dxfQN/S515ePssn3HjPCwfzR3S1KY4O9vFtH1Jql9-----END PRIVATE KEY-----"
        #pvkey = rsa.PrivateKey.load_pkcs1(privateKey.encode())
        #pvkey = privateKey

        # generate_address的传入参数需要是一个65位的byte[]，包括0x04+x+y
        # pbkey_numbers.encode_point()返回的是0x04+x+y的65位byte
        # pbkey_serial是88位的序列化的公钥
        # DER进行base64编码后为PEM
        # pbkey_numbers = pbkey.public_numbers()
        # pbkey_numbers.encode_point()
        # pbkey_serial = pbkey.public_bytes(serial.Encoding.DER, serial.PublicFormat.SubjectPublicKeyInfo)
        # pvkey_serial = pvkey.private_bytes(serial.Encoding.PEM, serial.PrivateFormat.PKCS8, serial.NoEncryption())

        # short_addr = tool.generate_address(pbkey_numbers.encode_point())
        # trans.cert = short_addr.encode('utf-8')
        # trans.cert = "1MH9xedPTkWThJUgT8ZYehiGCM7bEZTVGN".encode('utf-8')

        # 构造签名
        # sig = pvkey.sign(hashlib.sha256(trans.SerializeToString()).digest(),ec.ECDSA(hashes.SHA1()))
        sig = pvkey.sign(trans.SerializeToString(), ec.ECDSA(hashes.SHA1()))
        # pbkey.verify(sig, hashlib.sha256(trans.SerializeToString()).digest(), ec.ECDSA(hashes.SHA1()))
        trans.signature.cert_id.credit_code = self.creditCode
        trans.signature.cert_id.cert_name = self.certName
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        trans.signature.tm_local.CopyFrom(timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos))
        trans.signature.signature = sig
        
        return trans

    def doPost(self, url, data):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        except requests.exceptions.Timeout as e:
            print('TimeOut: '+str(e.message))
        except requests.exceptions.HTTPError as e:
            print('HTTPError: '+str(e.message))
        return response
         
    def postTranByString(self, data):
        # data = createTransaction.trans
        # url ="http://"+self.host + "/transaction/postTranByString";
        url = self.host + "/transaction/postTranByString";
        # data类型为byte(bin),先转换成byte(hex),再转换成string(hex)
        data = binascii.hexlify(data.SerializeToString())
        jsonObject = self.doPost(url,data.decode('utf-8'));
        return jsonObject;

    def sign(self, fileHash):
        input_file = open(self.jksPath, 'rb')
        input = input_file.read()

        pvkey = serial.load_pem_private_key(input, '123456'.encode('utf-8'), default_backend())
        print(fileHash)
        fileHash = bytes(fileHash, encoding="utf8")
        signature = pvkey.sign(fileHash, ec.ECDSA(hashes.SHA1()))
        print('签名后数据： ', signature)

        signature = base64.b64encode(signature).decode()
        return signature