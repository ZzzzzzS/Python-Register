<!--
 * @Author: 周子顺
 * @Date: 2021-05-13 17:35:04
 * @LastEditors: 周子顺
 * @LastEditTime: 2021-05-15 20:11:12
-->

# 软件注册信息生成器

> 最近一个项目由于需要防止在多台电脑上使用，也为了防止用户无限期使用，于是简单做了一个注册器。由于用户电脑不能联网，因此就不能做联网验证，所以其实用户也很容易破解。

# 使用说明

* 使用前请使用``pip install pycryptodome``命令按照软件包
* 使用**DecryptModule.py**模块进行解密运算，该模块运行在用户的计算机中。
* 使用**EncryptModule.py** 进行加密运算，该模块仅需运行在LICENSE管理员的计算机中。


## LICENSE签发过程

* 首先生成加密解密用的密钥对，命令如下：

```bash
python3 ./EncryptModule.py -k LICENSE

#将得到 LICENSE-Decrypt.key 和 LICENSE-Encrypy.key 两个文件，分别用于解密和加密
```

* 第二步根据用户机器的唯一识别码，过期时间，和加密密钥产生LICENSE文件，命令如下：

```bash
python ./EncryptModule.py -g 

Input Private Key File Name:
LICENSE-Encrypt.key # 输入加密密钥的完整名称

Input Fingerprint Name: # 输入用户提供的设备ID（解密模块找不到密钥时会自动提供）
123456

Input ExpireTime (e.g. 2021/07/07): # 输入期望的过期时间，格式为yyyy/mm/DD
2021/07/07

```

* 第三步，将生成的``LICENSE.txt``和``LICENSE-Decrypt.key``发送给用户，放在软件的同级文件夹下

## LICENSE校验过程

**使用DecryptModule中的LicenseChecker类来判断LICENSE是否有效**

例程如下：

```Python
    a = LicenseChecker("LICENSE.txt", "key-Decrypt.key")
    print(a.CheckLicenseAvailable())
```

# 基本原理

* 获取用户电脑的识别码，根据用户的唯一识别码和预设的过期时间加密计算出LICENSE.txt

* 用户打开软件时根据LICENSE.txt 解密出识别码和过期时间，根据识别码和过期时间判断是否换电脑和是否过期

# 标识符的选择

识别码可以选择网卡的MAC地址，但是考虑到用户计算机上可能没有网卡，因此该方法失效。因此在Windows端选择计算机序列号uuid，在Linux端使用Machine-id

## Linux端标识符

```bash
cat /var/lib/dbus/machine-id # 不需要root权限

cat /sys/class/dmi/id/board_serial #需要root权限
cat /sys/class/dmi/id/product_uuid
```

## Windows端标识符

```powershell
wmic csproduct get UUID #不需要管理员权限
```