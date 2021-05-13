'''
Author: 周子顺
Date: 2021-05-13 11:25:13
LastEditors: 周子顺
LastEditTime: 2021-05-13 17:35:06
'''
import sys
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import platform
import os


def GetSimulationID():
    if platform.system() == "Windows":
        Fingerprint = os.popen("wmic csproduct get UUID")
        f = Fingerprint.readline()
        f = Fingerprint.readline()
        f = Fingerprint.readline()  # 为了读取第三行
        f = f.strip('\n')
        print("Machine-id="+f)
        return f
    elif platform.system() == "Linux":
        Fingerprint = os.popen("cat /var/lib/dbus/machine-id")
        f = Fingerprint.read()
        f = f.strip('\n')
        print("Machine-id="+f)
        return f
    else:
        print("Unsupported platform, cannot get system ID")


def GenerateKey(Name: str):

    (PublicKey, PrivateKey) = rsa.newkeys(1024)
    PublicKeyPem = PublicKey._save_pkcs1_pem()
    PrivateKeyPem = PrivateKey._save_pkcs1_pem()
    PublicFileName = Name+"-Encrypt.key"
    PrivateFileName = Name+"-Decrypt.key"

    PublicFile = open(PublicFileName, "w+")
    PublicFile.write(PublicKeyPem.decode('utf-8'))
    PublicFile.close()
    PrivateFile = open(PrivateFileName, "w+")
    PrivateFile.write(PrivateKeyPem.decode('utf-8'))
    PrivateFile.close()


def GenerateLicense(EncryptKey: str, Fingerprint: str, ExpireTime: str):
    messagestr = '{"DeviceID":"'+Fingerprint+'","ExpireTime":"'+ExpireTime+'"}'
    message = bytes(messagestr, 'utf-8')
    f = open(EncryptKey)
    key = f.read()
    rsakey = RSA.importKey(key)  # 导入读取到的公钥
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
    cipher_text = base64.b64encode(
        cipher.encrypt(message))
    print(cipher_text.decode(encoding="utf-8"))

    LicenseFile = open("LICENSE.txt", 'w+')
    LicenseFile.write(cipher_text.decode(encoding="utf-8"))
    LicenseFile.close()


def PrintHelp():
    print("License Generator\n")
    print("Usage:")
    print(
        "     -k [filename]   Generate public key and private key file with given name")
    print("     -g              Generate license file with given device fingerprint and expire data")
    print("     -gl             Generate license file with local device ID and given expire data")


if __name__ == '__main__':

    if len(sys.argv) == 1:
        PrintHelp()
    elif sys.argv[1] == "-k":
        if len(sys.argv) != 3:
            print("Invalid Arguments\n")
            PrintHelp()
        else:
            GenerateKey(sys.argv[2])

    elif sys.argv[1] == "-g":
        KeyName = input("Input Private Key File Name:\n")
        FingerprintName = input("Input Fingerprint Name:\n")
        ExpireTime = input("Input ExpireTime (e.g. 2021/07/07):\n")

        GenerateLicense(KeyName, FingerprintName, ExpireTime)
    elif sys.argv[1] == "-gl":
        KeyName = input("Input Private Key File Name:\n")
        FingerprintName = GetSimulationID()
        ExpireTime = input("Input ExpireTime (e.g. 2021/07/07):\n")

        GenerateLicense(KeyName, FingerprintName, ExpireTime)
