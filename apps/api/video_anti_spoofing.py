from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import *
import cv2
from random import sample
from .FaceHelper import *
from .face_landmarks_2 import face_landmarks_2

alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

anti_spoofing_bp = Blueprint('anti_spoofing', __name__)
api = Api(anti_spoofing_bp)


class VideoDetection(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        parser.add_argument('Fid', type=int)
        parser.add_argument('Action', type=int, default=1)
        parser.add_argument('Fvideo', type=str)
        parser.add_argument('Threshold', type=float, default=0.6)
        args = parser.parse_args()
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')
        Fid = args.get('Fid')
        Action = args.get('Action')
        Fvideo = base64.b64decode(args.get('Fvideo'))
        Threshold = args.get('Threshold')

        count_confirm = 0
        count_eye = 0
        count_mouth = 0
        real = False

        app = App.query.get(Apid)
        if app is not None:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        face = Face.query.get(Fid)
        if not face:
            return {'msg_code': 7}, 404  # 查询的人脸不存在
        known_encoding = str2en(face.Fencoding)

        Vsrc = save_video(Fvideo, ''.join(sample(alphabet, 10)))  # 将视频解码并存至本地，返回存储路径
        try:
            video = cv2.VideoCapture(Vsrc)
        except Exception:
            os.remove(Vsrc)
            return {'msg_code': 8}, 415  # 视频文件格式无效或无法加载
        else:
            i = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break

                if i % 6 != 0:  # 抽帧，间隔为5
                    i += 1
                    continue
                rgb_frame = frame[:, :, ::-1]

                face_locations = fr.face_locations(rgb_frame)
                if len(face_locations) == 0:
                    continue

                main_face_location = find_main_face(face_locations)  # 找出主要的人脸位置
                main_face_landmarks = face_landmarks_2(rgb_frame, main_face_location)  # 获取主要人脸的特征点

                # 人脸识别
                if i % 24 == 0:
                    main_face_encoding = fr.face_encodings(rgb_frame, main_face_location)[0]  # 获取主要人脸的编码
                    match = fr.compare_faces([known_encoding], main_face_encoding, Threshold)[0]
                    if match:
                        count_confirm += 1

                    if i == 0:
                        backup_encoding = main_face_encoding
                    else:
                        same_face = fr.compare_faces([backup_encoding], main_face_encoding)  # 判断本帧中的人脸是否和上一帧中的相同
                        if not same_face:
                            count_confirm = 0
                        backup_encoding = main_face_encoding

                # 活体检测
                if Action == 1:
                    left_eye = main_face_landmarks[0]['left_eye']
                    right_eye = main_face_landmarks[0]['right_eye']
                    if eye_close_detection(left_eye, right_eye):
                        count_eye += 1
                    else:
                        if count_eye >= 1:
                            real = True
                            count_eye = 0

                elif Action == 2:
                    mouth = main_face_landmarks[0]['mouth']
                    if mouth_open_detection(mouth):
                        count_mouth += 1
                    else:
                        if count_mouth >= 1:
                            real = True
                            count_mouth = 0

                i += 1
                if real and count_confirm:
                    break

            video.release()
            os.remove(Vsrc)
            if i == 0:
                return {'msg_code': 8}, 415
            if count_confirm:
                return {'msg_code': 1, 'match': True, 'real': real}
            else:
                return {'msg_code': 1, 'match': False, 'real': real}

    def get(self):
        return {'test': 'test'}


api.add_resource(VideoDetection, '/api/living')
