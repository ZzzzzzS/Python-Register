'''
Author: 周子顺
Date: 2021-05-13 11:25:32
LastEditors: 周子顺
LastEditTime: 2021-05-13 17:11:32
'''

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from datetime import datetime
import platform
import os


class LicenseChecker:
    def __init__(self, LicenseFileName: str, DecryptKey: str) -> None:
        self.LicenseFile = self.__LoadLicenseFile(LicenseFileName)

        try:
            f = open(DecryptKey)
            self.key = f.read()
            f.close()
        except:
            print("Can't open key file")
            self.__ErrorInfo()
            self.key = []

    def CheckLicenseAvailable(self) -> bool:

        if len(self.key) == 0:
            return False

        if len(self.LicenseFile) == 0:
            return False

        rsakey = RSA.importKey(self.key)  # 导入读取到的私钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
        # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        text = cipher.decrypt(base64.b64decode(self.LicenseFile), "ERROR")

        LicenseStr = text.decode(encoding="utf-8")
        LicenseObject = eval(LicenseStr)
        LicenseDeviceID = LicenseObject["DeviceID"]
        LicenseExpireTime = datetime.strptime(
            LicenseObject["ExpireTime"], '%Y/%m/%d')

        DeviceID = self.__GetHardwareFingerprint()
        DeviceTime = datetime.now()

        if DeviceID != LicenseDeviceID:
            print("Current device does NOT match registed device")
            self.__ErrorInfo()
            return False

        if DeviceTime > LicenseExpireTime:
            print("This License has expired")
            self.__ErrorInfo()
            return False

        return True

    def __GetHardwareFingerprint(self) -> str:
        if platform.system() == "Windows":
            Fingerprint = os.popen("wmic csproduct get UUID")
            f = Fingerprint.readline()
            f = Fingerprint.readline()
            f = Fingerprint.readline()  # 为了读取第三行
            f = f.strip('\n')
            print("Windows Machine-id="+f)
            return f
        elif platform.system() == "Linux":
            Fingerprint = os.popen("cat /var/lib/dbus/machine-id")
            f = Fingerprint.read()
            f = f.strip('\n')
            print("Linux Machine-id="+f)
            return f
        else:
            print("Unsupported platform, cannot get system ID")

    def __LoadLicenseFile(self, LicenseFileName: str) -> str:
        try:
            f = open(LicenseFileName)
            file = f.read()
            f.close()
        except:
            print("Can't open LICENSE.txt")
            self.__ErrorInfo()
            file = []
        return file

    def __ErrorInfo(self):
        print("激活产品失败：请获取新的 LICENSE.txt")
        ID = self.__GetHardwareFingerprint()
        print("设备ID: ", ID)


if __name__ == '__main__':
    a = LicenseChecker("LICENSE.txt", "key-Decrypt.key")
    print(a.CheckLicenseAvailable())
