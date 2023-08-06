# 文件上传下载Python功能包
# 1. **功能包介绍**
NAS文件操作系统 - Grpc 版本Python包，python2.7及以上Python版本可使用  
**前一包的版本为：NASGrpcFileSystem==1.2.2** 
**当前包的版本为：NASGrpcFileSystem==1.3.2 兼容1.2.2 当前包支持连接复用** 

# 2. **如何使用**
# 入参说明：
*各个接口的 **`容灾路径参数`** 待定*
# 1. 创建文件接口：

参数名 | 类型 | 作用 | 是否可选 | 关联参数
- | - | - | - | -
caller_code | String | 调用方编码 | 否 | -
remote_path | String | 远程存储目录 | 否 | -
x_type | String | 业务类型，若mount_path为空，则根据不同业务类型、存储不同的服务器mount目录 | 否 | -
req_url | String | 请求IP:PORT | 是 | 当使用连接复用方式时，不需要传此参数 
file | String / base64 | 文件流，可以选择文件路径或者文件流，也可以是base64编码的文件 | 是 | filename
filename | String | 文件名称， 当上传对象为文件流时必传 | 是 | file
file_path | String | 本地文件路径，可以选择文件路径或者文件流 | 是 | -
mount_path | String | 服务器mount地址 | 是 | -
replace | Boolean | 当文件已在服务器存在时是否强制替换，默认替换 | 是 | -
recovery_path | String | 容灾路径，当文件上传非正常失败时（调用接口非正常错误码），将文件存储的本地地址，此时返回的mount_path为空 | 是 | -
timeout | Int | 超时时间，默认3秒 | 是 | -
logger | Object | 日志对象 | 是 | -

# 2. 返回文件接口：

参数名 | 类型 | 作用 | 是否可选 | 关联参数
- | - | - | - | -
caller_code | String | 调用方编码 | 否 | -|
remote_full_path | String | 远程文件存储路径及完整文件名称，全地址 | 否 | -|
recovery_full_path | String | 容灾目录文件，当非正常错误发生时，读取此文件 | 是 | -|
req_url | String | 请求IP:PORT | 是 | 当使用连接复用方式时，不需要传此参数|
local_full_path | String | 下载的文件本地存储路径包含文件名，全地址 | 是 | return_file|
return_file | String | 是否需要将文件流返回, 如不返回则需要传入local_full_path，同时返回"" | 是 | local_full_path|
timeout | Int | 超时时间，默认3秒 | 是 | -|
logger | Object | 日志对象 | 是 | -|

# 3. 修改文件名称接口：

参数名 | 类型 | 作用 | 是否可选 | 关联参数
- | - | - | - | -
caller_code | String | 调用方编码 | 否 | -|
remote_full_path | String | 远程文件存储路径及完整文件名称，全地址 | 否 | -|
req_url | String | 请求IP:PORT | 是 | 当使用连接复用方式时，不需要传此参数|
modified_file_name | String | 修改后的文件名称 | 否 | -|
recovery_full_path | String | 容灾目录文件，当非正常错误发生时，修改此文件名称 | 是 | -|
replace | Boolean | 如果服务器已有要改的文件名，是否强制覆盖，默认覆盖 | 是 | - | 
timeout | Int | 超时时间，默认3秒 | 是 | -|
logger | Object | 日志对象 | 是 | -|

# 4. 复制文件接口：

参数名 | 类型 | 作用 | 是否可选 | 关联参数
- | - | - | - | -
caller_code | String | 调用方编码 | 否 | -|
original_full_path | String | 远程文件存储路径及完整文件名称，全地址 | 否 | -|
req_url | String | 请求IP:PORT | 是 | 当使用连接复用方式时，不需要传此参数|
new_full_path | String | 复制后的文件路径（传文件名则变更文件名称，不传则为原文件名称）；路径存在直接移动，不存在则创建 | 否 | -|
timeout | Int | 超时时间，默认3秒 | 是 | -|
logger | Object | 日志对象 | 是 | -|

# 5. 移动文件接口：

参数名 | 类型 | 作用 | 是否可选 | 关联参数
- | - | - | - | -
caller_code | String | 调用方编码 | 否 | -|
original_full_path | String | 远程文件存储路径及完整文件名称，全地址 | 否 | -|
req_url | String | 请求IP:PORT | 是 | 当使用连接复用方式时，不需要传此参数|
new_full_path | String | 移动后的文件存储路径（存在直接移动，不存在则创建），不包含文件名（移动后文件名称与原文件名一致） | 否 | -|
timeout | Int | 超时时间，默认3秒 | 是 | -|
logger | Object | 日志对象 | 是 | -|

# 返回参数说明：
# 1. 创建文件接口：
- 元组，包含错误码，错误描述，服务器存储的mount地址  

>> 当返回错误码为0时：  
>>>* 错误描述对应错误说明表。  
>>>* 如果存储地址为本地的容灾目录，则mount地址为空字符串。

>> 当返回错误码非0时：  
>>>* 错误描述对应错误说明表。  
>>>* mount地址为空字符串。  


值 | 类型 | 描述
- | - | -
错误码 | Int | 详见错误码说明
错误描述 | String | 详见错误码说明
mount地址 | String | 服务器存储的mount地址

> (0, '成功', '/picture/CERTIFICATE/')

# 2. 返回文件接口：
- 元组，包含错误码，错误描述，文件流（如果入参return_file = False, 则此值为" "）

> 当返回错误码非0时：
>> * 错误描述对应错误说明表。   
>> * 文件流分为以下几种情况:  
>>>1. 若获取不到容灾目录文件（入参为空或文件不存在），返回文件流为" "  
>>>2. 若获取到了容灾目录文件，而入参return_file = False, 则返回文件流为" "  
>>>3. 若获取到了容灾目录文件，而入参return_file = True, 则返回读取到的文件流  

# 3. 修改文件名称接口：
- 元组，包含错误码，错误描述

> 当返回错误码非0时：
>> * 错误描述对应错误说明表。  


值 | 类型 | 描述
- | - | -
错误码 | Int | 详见错误码说明
错误描述 | String | 详见错误码说明

> (0, '操作成功')

# 4. 复制文件接口：
- 元组，包含错误码，错误描述

> 当返回错误码非0时：
>> * 错误描述对应错误说明表。  


值 | 类型 | 描述
- | - | -
错误码 | Int | 详见错误码说明
错误描述 | String | 详见错误码说明

> (0, '操作成功')

# 5. 移动文件接口：
- 元组，包含错误码，错误描述

> 当返回错误码非0时：
>> * 错误描述对应错误说明表。  


值 | 类型 | 描述
- | - | -
错误码 | Int | 详见错误码说明
错误描述 | String | 详见错误码说明

> (0, '操作成功')


# 错误码说明：

|错误码 | 错误码描述 | 备注|
|---- | ----|----|
|0 | 操作成功 | |
|1 | 请求失败 | |
|128501 | 参数异常 | |
|128502 | 缺少请求必传参数 | |
|128503 | 文件缺少扩展名 | |
|128504 | 目录不存在 | |
|128505 | 文件不存在 | |
|128506 | 不是文件 | |
|128507 | 文件已存在 | |
|128508 | 目录已存在 | |
|128509 | 读取超时 | |
|128510 | 保存文件失败 | |
|128511 | 文件夹创建失败 | |
|128512 | 连接超时 | |
|128513 | 读取文件失败 | |
|128514 | 权限不足 | |
|128515 | 业务场景不存在 | |


# 安装使用：
- 安装包

> ``pip install NASGrpcFileSystem``

- 使用示例

```python
# coding: utf-8
import base64
from future.utils import raise_
from NASGrpcFileSystem import create_file, describe_file, modify_file, copy_file, move_file, FileHandler


def gen_file(file_path, size=1024*1024):
    """
    :param file_path:
    :param size: 生成器每次迭代文件流大小
    :return: 生成器对象
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(size)
            while data:
                yield data
                data = f.read(size)
    except Exception as exc:
        raise_(Exception, exc)


def img_to_64(path):
    """
    对图片内容base64编码
    :param path: 文件路径
    :return: BASE64编码后的文件内容
    """
    after_base64 = None, None
    try:
        with open(path, 'rb') as f:  # 二进制方式打开图文件
            after_base64 = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    except Exception as exc:
        raise_(Exception, exc)
    return after_base64


def call_create_file(caller_code, remote_path, x_type, req_url, file, filename, mount_path, recovery_path=None):
    try:
        res = create_file(caller_code, remote_path, x_type, req_url, file, filename, file_path=None,
                          mount_path=mount_path, replace=True, recovery_path=recovery_path, timeout=3, logger=None)
    except Exception as exc:
        res = (1, '', '')
    return res
    
    
def call_create_file_path(caller_code, remote_path, x_type, req_url, file_path, mount_path, recovery_path="/demo"):
    try:
        res = create_file(caller_code, remote_path, x_type, req_url, file_path=file_path, mount_path=mount_path, recovery_path=recovery_path, timeout=30, logger=None)
    except Exception as exc:
        res = (1, '', '')
    return res


def call_describe_file(caller_code, remote_full_path, req_url, local_full_path, recovery_full_path):
    try:
        res = describe_file(caller_code, remote_full_path, req_url, local_full_path,
                            recovery_full_path, return_file=True, timeout=3, logger=None)
    except Exception as exc:
        res = (1, '', '')
    return res


def call_modify_file(caller_code, remote_full_path, req_url, modified_file_name, recovery_full_path=None):
    try:
        res = modify_file(caller_code, remote_full_path, req_url, modified_file_name,
                          recovery_full_path=recovery_full_path, timeout=3, logger=None)
    except Exception as exc:
        res = (1, '')
    return res
    

def call_copy_file(caller_code, original_full_path, req_url, new_file_path):
    try:
        res = copy_file(caller_code, original_full_path, req_url, new_file_path, timeout=30, logger=None)
    except Exception as exc:
        res = (1, '')
    return res


def call_move_file(caller_code, original_full_path, req_url, new_file_path):
    try:
        res = move_file(caller_code, original_full_path, req_url, new_file_path, timeout=30, logger=None)
    except Exception as exc:
        res = (1, '')
    return res


if __name__ == "__main__":
    # 准一地址
    req_url = "172.16.50.55:31214"
    caller_code = "test_python_sdk"
    try:
        # 不同形式的文件流
        file_ = gen_file("./test/c1.jpg", 2048)
        # file_ = img_to_64("./test/c1.jpg")
    except Exception as exc:
        file_ = " "

#### 连接复用方式，初始化文件处理类，通过类调用接口 ###################
    grpc_handler = FileHandler(req_url)
    # 创建文件
    res_create = grpc_handler.create_file(caller_code, "test/", "m10805", file_path="./test/c1.jpg", mount_path="/picture/CERTIFICATE/")
    # 获取文件
    res_desc = grpc_handler.describe_file(caller_code, '/picture/CERTIFICATE/test/g2.jpg', "./ccc.jpg")
    # 修改文件
    res_modify = grpc_handler.modify_file(caller_code, '/picture/CERTIFICATE/test/g2.jpg', "g1.jpg")
    # 复制文件
    res_copy = grpc_handler.copy_file(caller_code, '/picture/CERTIFICATE/test/g1.jpg', "/picture/CERTIFICATE/test_move1/g1.jpg")
    # 移动文件
    res_move = grpc_handler.move_file(caller_code, '/picture/CERTIFICATE/test_move1/g1.jpg', "/picture/CERTIFICATE/test")

#### 一次请求一个连接方式 ###################
    res_up = call_create_file(caller_code, "test/", "m10805", req_url, file_, "c1.jpg", "/picture/CERTIFICATE/")
    print(res_up)

    res_up = call_create_file_path(caller_code, "test/", "m10805", req_url, "./test/c1.jpg", "/picture/CERTIFICATE/")
    print(res_up)

    res_down = call_describe_file(caller_code, '/picture/CERTIFICATE/test/c1.jpg', req_url, "./g0.jpg", None)
    print(res_down)

    res_modify = call_modify_file(caller_code, '/picture/CERTIFICATE/test/c1.jpg', req_url, "c2.jpg", "./test/c1.jpg")
    print(res_modify)

    res_copy = call_copy_file(caller_code, '/picture/CERTIFICATE/test/c2.jpg', req_url, "/picture/CERTIFICATE/test_move1/copyc1.jpg")
    print(res_copy)

    res_move = call_move_file(caller_code, '/picture/CERTIFICATE/test_move1/copyc1.jpg', req_url, "/picture/CERTIFICATE/test")
    print(res_move)
```
