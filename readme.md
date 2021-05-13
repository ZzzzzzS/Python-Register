<!--
 * @Author: 周子顺
 * @Date: 2021-05-13 17:35:04
 * @LastEditors: 周子顺
 * @LastEditTime: 2021-05-13 18:00:42
-->

# 软件注册信息生成器

> 最近一个项目由于需要防止在多台电脑上使用，也为了防止用户无限期使用，于是简单做了一个注册器。由于用户电脑不能联网，因此就不能做联网验证，所以其实用户也很容易破解。

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
    ```cmd
    wmic csproduct get UUID #不需要管理员权限
    ```