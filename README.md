

# <span id="index">目录</span>

#### [/api/face](#face)

#### [/api/singleface](#singleface)

#### [/api/similarity](#similarity)

#### [/api/detection](#detection)

#### [/api/match](#match)

#### [/api/living](#living)

#### [信息码参照表](#jump)



## <span id="face">`/api/face`</span>                                                                                              [返回目录](#index)

### 请求方法：GET

#### 功能

​	查询单个应用下的所有人脸

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释               |
| ------ | ---- | ------ | :----------------- |
| Apid   | 是   | number | 外部应用编号       |
| Kvalue | 是   | string | 外部应用对应的密钥 |

#### 示例

```python
import requests
request_data = {'Apid': Apid, 'Kvalue': password}
r = requests.get('localhost:5000/api/face', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "faces": [{"Fid": 19, "Fname": "test_face", "Apid": 1},{"Fid": 20, "Fname": "test_face", "Apid": 1}]}
```

| 字段     | 必选 | 类型   | 解释                                                    |
| -------- | ---- | ------ | :------------------------------------------------------ |
| msg_code | 是   | number | 信息码，仅在查询失败时返回，请对照[信息码参照表](#jump) |
| faces    | 否   | array  | 人脸信息列表，仅当msg_code为1时返回                     |



### 请求方法：POST

#### 功能

​	添加人脸

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释                             |
| ------ | ---- | ------ | :------------------------------- |
| Fimg   | 是   | string | 人脸图像base64编码的字符串形式   |
| Fname  | 否   | string | 人脸名，若为空则自动以时间戳命名 |
| Apid   | 是   | number | 外部应用编号                     |
| Kvalue | 是   | string | 外部应用对应的密钥               |

#### 示例

```python
import requests
request_data = {'Fimg': base64_encoding, 'Fname': name, 'Apid': Apid, 'Kvalue': password}
r = requests.post('localhost:5000/api/face', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "Fid": 20, "Fname": "name"}
```

| 字段     | 必选 | 类型   | 解释                                |
| -------- | ---- | ------ | :---------------------------------- |
| msg_code | 是   | number | 信息码，请对照[信息码参照表](#jump) |
| Fid      | 否   | number | 人脸id，仅当msg_code为1时返回       |
| Fname    | 否   | string | 人脸名，仅当msg_code为1时返回       |



### 请求方法：PUT

#### 功能

​	修改人脸

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释                             |
| ------ | ---- | ------ | :------------------------------- |
| Fid    | 是   | number | 需要修改的人脸的id               |
| Fimg   | 否   | string | 新人脸图像base64编码的字符串形式 |
| Fname  | 否   | string | 新人脸名                         |
| Apid   | 是   | number | 外部应用编号                     |
| Kvalue | 是   | string | 外部应用对应的密钥               |

#### 示例

```python
import requests
request_data = {'Fid': face_id, 'Fimg': base64_encoding, 'Fname': name, 'Apid': Apid, 'Kvalue': password}
r = requests.put('localhost:5000/api/face', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "Fid": 19, "Fname": "new_name"}
```

| 字段     | 必选 | 类型   | 解释                                    |
| -------- | ---- | ------ | :-------------------------------------- |
| msg_code | 是   | number | 信息码，请对照[信息码参照表](#jump)     |
| Fid      | 否   | number | 人脸id，仅当msg_code为1时返回           |
| Fname    | 否   | string | 新人脸名，仅当msg_code为1时返回新人脸名 |



### 请求方法：DELETE

#### 功能

​	删除人脸

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释               |
| ------ | ---- | ------ | :----------------- |
| Fid    | 是   | number | 需要删除的人脸的id |
| Apid   | 是   | number | 外部应用编号       |
| Kvalue | 是   | string | 外部应用对应的密钥 |

#### 示例

```python
import requests
request_data = {'Fid': face_id, 'Apid': Apid, 'Kvalue': password}
r = requests.delete('localhost:5000/api/face', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "Fid": 19, "Fname": "face_name"}
```

| 字段     | 必选 | 类型   | 解释                                    |
| -------- | ---- | ------ | :-------------------------------------- |
| msg_code | 是   | number | 信息码，请对照[信息码参照表](#jump)     |
| Fid      | 否   | number | 成功删除的人脸id，仅当msg_code为1时返回 |
| Fname    | 否   | string | 成功删除的人脸名，仅当msg_code为1时返回 |



## <span id="singleface">`/api/singleface`</span>                                                                                [返回目录](#index)

### 请求方法：GET

#### 功能

​	查询单个人脸

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释               |
| ------ | ---- | ------ | :----------------- |
| Fid    | 是   | string | 需要查询的人脸的id |
| Apid   | 是   | number | 外部应用编号       |
| Kvalue | 是   | string | 外部应用对应的密钥 |

#### 示例

```python
import requests
request_data = {'Fid': face_id, 'Apid': Apid, 'Kvalue': password}
r = requests.get('localhost:5000/api/singleface', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "Fid": 19, "Fname": "name"}
```

| 字段     | 必选 | 类型   | 解释                                |
| -------- | ---- | ------ | :---------------------------------- |
| msg_code | 是   | number | 信息码，请对照[信息码参照表](#jump) |
| Fid      | 否   | number | 人脸id，仅当msg_code为1时返回       |
| Fname    | 否   | string | 人脸名，仅当msg_code为1时返回       |



## <span id="similarity">`/api/similarity`</span>                                                                                [返回目录](#index)

### 请求方法：POST

#### 功能

​	查询n-1张人脸各自与第1张人脸的相似度

#### 请求字段说明

| 字段                  | 必选 | 类型      | 解释                                                         |
| --------------------- | ---- | --------- | :----------------------------------------------------------- |
| Apid                  | 是   | intnumber | 外部应用编号                                                 |
| Kvalue                | 是   | string    | 外部应用对应的密钥                                           |
| Fimg%d i(i=1,2,...,n) | 否   | string    | 人脸图片base64编码的字符串形式，编号需按顺序，如Fimg1, Fimg2, Fimg3,..., Fimgn，中间不可缺号 |

#### 示例

```python
import requests
# 对比两张人脸图片的相似度
request_data = {'Apid': Apid, 'Kvalue': password, 'Fimg1': base64_encoding, 'Fimg2': base64_encoding}
r = requests.post('localhost:5000/api/similarity', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "similarity": [0.5052671683728283]}
```

| 字段       | 必选 | 类型   | 解释                                         |
| ---------- | ---- | ------ | :------------------------------------------- |
| msg_code   | 是   | number | 信息码，请对照[信息码参照表](#jump)          |
| similarity | 否   | array  | 长度为n-1的相似度列表，仅当msg_code为1时返回 |



## <span id="detection">`/api/detection`</span>                                                                                  [返回目录](#index)

### 请求方法：POST

#### 功能

​	检测图片中的所有人脸并返回人脸坐标

#### 请求字段说明

| 字段   | 必选 | 类型   | 解释                       |
| ------ | ---- | ------ | :------------------------- |
| Fimg   | 是   | string | 图片base64编码的字符串形式 |
| Apid   | 是   | number | 应用编号               |
| Kvalue | 是   | string | 应用对应的密钥         |

#### 示例

```python
import requests
request_data = {'Fimg': base64_encoding, 'Apid': Apid, 'Kvalue': password}
r = requests.post('localhost:5000/api/detection', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "location": [[57,964,242,778], [47,408,202,253]]}
```

| 字段     | 必选 | 类型   | 解释                                                         |
| -------- | ---- | ------ | :----------------------------------------------------------- |
| msg_code | 是   | number | 信息码，请对照[信息码参照表](#jump)                          |
| location | 否   | array  | 仅当msg_code为1时，若图片中有n张脸，返回长度为n的人脸坐标列表，列表中每个元素为大小为4的tuple |



## <span id="match">`/api/match `</span>                                                                                            [返回目录](#index)

### 请求方法：GET

#### 功能

​	将上传的人脸图像与数据库中的人脸进行比对并返回比对结果

#### 请求字段说明

| 字段      | 必选 | 类型   | 解释                                                         |
| --------- | ---- | ------ | :----------------------------------------------------------- |
| Fid       | 是   | number | 已知的数据库中的人脸id                                       |
| Fimg      | 是   | string | 待比对图片base64编码的字符串形式                             |
| Apid      | 是   | number | 外部应用编号                                                 |
| Kvalue    | 是   | string | 外部应用对应的密钥                                           |
| Threshold | 否   | number | 取值范围[0,1]，人脸比对时欧氏距离的阈值，默认为0.6，越低越严格 |

#### 示例

```python
import requests
request_data = {'Fid': face_id, 'Fimg': base64_encoding, 'Apid': Apid, 'Kvalue': password, 'Threshold': 0.7}
r = requests.get('localhost:5000/api/match', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "match": true}
```

| 字段     | 必选 | 类型    | 解释                                                         |
| -------- | ---- | ------- | :----------------------------------------------------------- |
| msg_code | 是   | number  | 信息码，请对照[信息码参照表](#jump)                          |
| match    | 否   | boolean | 仅当msg_code为1时，若两张脸为同一人，返回True，否则返回False |



## <span id="living">`/api/living`</span>                                                                                         [返回目录](#index)

### 请求方法：POST

#### 功能

​	通过对上传的视频的抽帧分析，进行配合式活体检测及人脸比对

#### 请求字段说明

| 字段      | 必选 | 类型   | 解释                                                         |
| --------- | ---- | ------ | :----------------------------------------------------------- |
| Fid       | 是   | number | 已知的数据库中的待比对的人脸id                               |
| Action    | 是   | number | 进行活体检测的所需的动作，1为眨眼，2为张嘴，默认值为1        |
| Fvideo    | 是   | string | 人脸视频base64编码的字符串形式                               |
| Apid      | 是   | number | 应用编号                                                 |
| Kvalue    | 是   | string | 应用对应的密钥                                           |
| Threshold | 否   | number | 取值范围[0,1]，人脸比对时欧氏距离的阈值，默认值为0.6，越低越严格 |

#### 示例

```python
import requests
request_data = {'Fid': face_id, 'Action': 1, 'Fvideo': base64_encoding, 'Apid': Apid, 'Kvalue': password, 'Threshold': 0.7}
r = requests.post('localhost:5000/api/living', data=request_data)
```

#### 返回字段说明

```python
{"msg_code": 1, "match": true, "real": true}
```

| 字段     | 必选 | 类型    | 解释                                                         |
| -------- | ---- | ------- | :----------------------------------------------------------- |
| msg_code | 是   | number  | 信息码，请对照[信息码参照表](#jump)                          |
| match    | 否   | boolean | 仅当msg_code为1时，若视频中的脸与数据库中的人脸的欧氏距离小于一定阈值且此现象持续36帧以上，返回True（两张脸为同一人），否则返回False |
| real     | 否   | boolean | 仅当msg_code为1时，若视频中人脸通过活体检测，返回True，否则返回False |



## <span id="jump">信息码参照表 </span>                                                                                             [返回目录](#index)

| 信息码 | 解释                       |
| ------ | -------------------------- |
| 1      | 请求成功                   |
| 2      | 密钥错误                   |
| 3      | 外部应用不存在             |
| 4      | 图片文件格式无效或无法加载 |
| 5      | 未检测到人脸               |
| 6      | 检测到多张人脸             |
| 7      | 查询的人脸不存在           |
| 8      | 视频文件格式无效或无法加载 |

