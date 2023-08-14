from io import BytesIO
import numpy as np
import face_recognition as fr
import base64
import os
from struct import unpack_from
from PIL import Image


def load_image_frombytes(img_binary):
    """
    从二进制数据加载图片，返回PIL.Image类

    :param img_binary: 图片的二进制数据
    :type img_binary: bytes
    :return: Image类
    """
    try:
        img = Image.open(BytesIO(img_binary)).convert('RGB')
    except Exception:
        raise Exception()
    else:
        return img


def save_video(Video, Vname):
    """
    将视频二进制数据存至本地，返回存储路径。

    :param Video: 视频的二进制数据
    :param Vname: 视频名
    :type Video: bytes
    :type Vname: str
    :return: 存储路径str
    """

    video_name = Vname + '.dat'
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/temp')
    Vsrc = os.path.join(video_path, video_name)
    file = open(Vsrc, 'wb')
    file.write(Video)
    file.close()
    return Vsrc


def eye_close_detection(left_eye, right_eye, ear_threshold=0.25):
    """
    判断眼睛是否闭上
    :param left_eye: 左眼特征点
    :param right_eye: 右眼特征点
    :param ear_threshold: 用于判断眼睛是否闭上的眼睛纵横比阈值
    :return: Bool
    """

    # ear即eye aspect ratio(眼睛纵横比)，用于判断眼睛是否张开/合上
    ear_left = get_ear(left_eye)
    ear_right = get_ear(right_eye)

    if ear_left <= ear_threshold and ear_right <= ear_threshold:
        return True
    else:
        return False


def get_ear(eye):
    # 计算眼睛纵横比eye aspect ratio
    A = ((eye[1][0] - eye[5][0])**2 + (eye[1][1] - eye[5][1])**2)**0.5
    B = ((eye[2][0] - eye[4][0])**2 + (eye[2][1] - eye[4][1])**2)**0.5
    C = ((eye[0][0] - eye[3][0])**2 + (eye[0][1] - eye[3][1])**2)**0.5
    ear = (A + B) / (2.0 * C)
    return ear


# 判断是否张嘴
def mouth_open_detection(mouth, mar_threshold=0.7):
    """
    判断是否张嘴
    :param mouth: 嘴巴特征点
    :param mar_threshold: 用于判断嘴巴是否张开的嘴巴纵横比阈值
    :return: Bool
    """
    mouth_mar = get_mar(mouth)
    if mouth_mar >= mar_threshold:
        return True
    else:
        return False


def get_mar(mouth):
    # 计算嘴巴纵横比mouth aspect ratio
    A = ((mouth[2][0] - mouth[10][0]) ** 2 + (mouth[2][1] - mouth[10][1]) ** 2) ** 0.5
    B = ((mouth[4][0] - mouth[8][0]) ** 2 + (mouth[4][1] - mouth[8][1]) ** 2) ** 0.5
    C = ((mouth[0][0] - mouth[6][0]) ** 2 + (mouth[0][1] - mouth[6][1]) ** 2) ** 0.5
    ear = (A + B) / (2.0 * C)
    return ear


def save_img(Fimg, Fname):
    """
    将图片存至本地，返回存储路径。

    :param Fimg: 图片的二进制数据
    :param Fname: 人脸名
    :type Fimg: bytes
    :type Fname: str
    """

    '''file_type_map = {
        '6677': '.bmp',
        '13780': '.png',
        '255216': '.jpg',
    }

    img_data = base64.b64decode(Fimg)  # 人脸图片二进制数据
    file_info = unpack_from("BB", img_data)  # 二进制数据前两个字节的信息，其内容代表文件类型
    file_type_code = str(file_info[0]) + str(file_info[1])
    if file_type_code not in file_type_map:
        return None
    else:
        file_type = file_type_map[file_type_code]

    img_name = Fname + file_type'''
    img_name = Fname + '.jpg'
    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/face_img')
    Fsrc = os.path.join(img_path, img_name)
    '''file = open(Fsrc, 'wb')
    file.write(Fimg)
    file.close()'''

    return Fsrc


def find_main_face(face_locations):
    """
    找到图片中面积最大的人脸

    :param face_locations: 人脸位置列表
    :type face_locations: list
    :return: 最大人脸的位置列表
    """
    max_area = 0
    max_face = face_locations[0]
    max_face_location = []
    for face in face_locations:
        area = abs((face[0] - face[2]) * (face[1] - face[3]))
        if area > max_area:
            max_area = area
            max_face = face

    max_face_location.append(max_face)

    return max_face_location


def encoding_fromarray(img):
    count = len(fr.face_locations(img))
    if count == 1:
        encoding = fr.face_encodings(img)[0]
        return encoding, 1  # 信息码，成功
    elif count == 0:
        return None, 5  # 信息码，未检测到人脸
    else:
        return None, 6  # 信息码，测到多张人脸


def encoding_fromfile(img_path):
    """
        从图片获取图片中人脸编码

        :param img_path: 图片路径
        :type img_path: str
        """

    img = fr.load_image_file(img_path)
    count = len(fr.face_locations(img))
    if count == 1:
        encoding = fr.face_encodings(img)[0]
        return encoding, 1  # 信息码，成功
    elif count == 0:
        return None, 5  # 信息码，未检测到人脸
    else:
        return None, 6  # 信息码，测到多张人脸


def en2str(face_encoding):
    """
    将人脸编码转换为字符串

    :param face_encoding: 人脸编码
    :type face_encoding: numpy.ndarray
    :return: str
    """

    '''byte = face_encoding.tobytes()
    string = str(byte, encoding='ISO-8859-1')  # encoding='ISO-8859-1'''
    encoding_list = face_encoding.tolist()
    for i in range(0, len(encoding_list)):
        encoding_list[i] = str(encoding_list[i])
    string = ','.join(encoding_list)
    return string


def str2en(face_string):
    """
    将字符串转换为人脸编码

    :param face_string: 人脸编码字符串形式
    :type face_string: str
    :return: 人脸编码
    """
    '''byte = bytes(face_string, encoding='ISO-8859-1')
    encoding = np.frombuffer(byte)'''
    encoding = np.fromstring(face_string, dtype=float, sep=',')
    return encoding
