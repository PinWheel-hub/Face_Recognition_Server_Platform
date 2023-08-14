from flask import Blueprint
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *
from .FaceHelper import *
from time import time
from datetime import datetime
from random import choice


face_api_bp = Blueprint('face_api', __name__)
api = Api(face_api_bp)

face_fields = {
    'Fid': fields.Integer(attribute='Fid'),
    'Fname': fields.String(attribute='Fname'),
    'Apid': fields.Integer(attribute='Apid'),
}

alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'


# 定义类视图
class FaceApi(Resource):
    # 查询某个App下全部人脸
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        faces = Face.query.filter(Face.Apid == Apid).all()
        if faces:
            return {'msg_code': 1, 'faces': marshal(faces, face_fields)}
        else:
            return {'msg_code': 7}, 404  # 查询的人脸不存在

    # 添加人脸
    def post(self):
        #try:
        parser = reqparse.RequestParser()
        parser.add_argument('Fimg', type=str)  # 人脸图片base64编码的str形式
        parser.add_argument('Fname', type=str, default=(str(time())).replace('.', '-'))
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Fimg = base64.b64decode(args.get('Fimg'))
        Fname = args.get('Fname')
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        try:
            img = load_image_frombytes(Fimg)
        except Exception:
            return {'msg_code': 4}, 415  # 图片文件格式无效或无法加载

        else:
            Fencoding, msg_code = encoding_fromarray(np.array(img))  # 获取人脸编码
            return_msg = {'msg_code': msg_code}
            if msg_code == 1:
                # Fsrc = save_img(Fimg, Fname + '-' + (str(time())).replace('.', '-') + choice(alphabet))
                img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/face_img')
                Fsrc = os.path.join(img_path, Fname + '-' + (str(time())).replace('.', '-') + choice(alphabet) + '.jpg')
                img.save(Fsrc)  # 图片存至本地
                face = Face(Fsrc, en2str(Fencoding), Fname, Apid)
                db.session.add(face)
                db.session.commit()
                return_msg['Fid'] = face.Fid
                return_msg['Fname'] = face.Fname
                return return_msg
            else:
                return return_msg
        '''except Exception as e:
            print(repr(e))'''

    # 修改人脸
    # @marshal_with(face_fields)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Fimg', type=str)  # 人脸图片base64编码的str形式
        parser.add_argument('Fname', type=str)
        parser.add_argument('Apid', type=int)
        parser.add_argument('Fid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()

        Fid = args.get('Fid')
        Fimg = base64.b64decode(args.get('Fimg'))
        Fname = args.get('Fname')
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        face = Face.query.get(Fid)
        if face:
            if Fimg is not None:
                try:
                    img = load_image_frombytes(Fimg)
                except Exception:
                    return {'msg_code': 4}, 415  # 图片文件格式无效或无法加载
                else:
                    Fencoding, msg_code = encoding_fromarray(np.array(img))
                    return_msg = {'msg_code': msg_code}
                    if msg_code == 1:
                        # Fsrc = save_img(Fimg, Fname + '-' + (str(time())).replace('.', '-') + choice(alphabet))
                        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                                'static/face_img')
                        Fsrc = os.path.join(img_path,
                                            Fname + '-' + (str(time())).replace('.', '-') + choice(alphabet) + '.jpg')
                        img.save(Fsrc)
                        face.Fencoding = en2str(Fencoding)
                        try:
                            os.remove(face.Fsrc)
                        except Exception:
                            pass
                        face.Fsrc = Fsrc
                    else:
                        return return_msg
            else:
                return_msg = {'msg_code': 1}, 200
            if Fname is not None:
                face.Fname = Fname
            db.session.commit()
            return_msg['Fid'] = face.Fid
            return_msg['Fname'] = face.Fname
            return return_msg
        else:
            return {'msg_code': 7}, 404  # 查询的人脸不存在

    # 删除人脸
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Fid', type=int)
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Fid = args.get('Fid')
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        face = Face.query.get(Fid)
        if face:
            try:
                os.remove(face.Fsrc)
            except Exception:
                pass
            return_msg = {'msg_code': 1, 'Fid': Fid, 'Fname': face.Fname}
            db.session.delete(face)
            db.session.commit()
            return return_msg
        else:
            return {'msg_code': 7}, 404  # 查询的人脸不存在


class SingleFace(Resource):
    # 查询单个人脸
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Fid', type=int)
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Fid = args.get('Fid')
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        face = Face.query.filter(Face.Fid == Fid, Face.Apid == Apid).first()
        if face:
            return_msg = {
                            'msg_code': 1,
                            'Fid': face.Fid,
                            'Fname': face.Fname,
                            }
            return return_msg
        else:
            return {'msg_code': 7}, 404  # 查询的人脸不存在


class Similarity(Resource):
    # 多张图片人脸相似度检测
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')
        i = 1
        similarities = []

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        parser.add_argument("Fimg%d" % i, type=str)
        args = parser.parse_args()
        while args.get("Fimg%d" % i) is not None:
            Fimg = base64.b64decode(args.get("Fimg%d" % i))
            try:
                img = load_image_frombytes(Fimg)
            except Exception:
                return {'msg_code': 4}, 415  # 图片文件格式无效或无法加载
            encoding, msg_code = encoding_fromarray(np.array(img))
            if msg_code == 1:
                if i == 1:
                    base_encoding = encoding
                else:
                    similarities.append(1 / (1 + fr.face_distance([base_encoding], encoding).tolist()[0]))
            else:
                return {'msg_code': msg_code}
            i += 1
            parser.add_argument("Fimg%d" % i, type=str)
            args = parser.parse_args()
        msg_code = 1
        return {'msg_code': msg_code, 'similarity': similarities}


class Detection(Resource):
    # 图片人脸检测
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Apid', type=int)
        parser.add_argument('Kvalue', type=str)
        args = parser.parse_args()
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')

        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            return {'msg_code': 3}, 404  # App不存在

        parser.add_argument('Fimg', type=str)
        args = parser.parse_args()
        Fimg = base64.b64decode(args.get('Fimg'))

        try:
            img = load_image_frombytes(Fimg)
        except Exception:
            return {'msg_code': 4}, 415  # 图片文件格式无效或无法加载

        locations = fr.face_locations(np.array(img))
        if len(locations) == 0:
            return {'msg_code': 5}  # 未检测到人脸
        else:
            return {'msg_code': 1, 'location': locations}


class Match(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Fid', type=int)
        parser.add_argument('Apid', type=int)
        parser.add_argument('Fimg', type=str)
        parser.add_argument('Kvalue', type=str)
        parser.add_argument('Threshold', type=float, default=0.6)
        args = parser.parse_args()
        Fid = args.get('Fid')
        Apid = args.get('Apid')
        Kvalue = args.get('Kvalue')
        Fimg = base64.b64decode(args.get('Fimg'))
        Threshold = args.get('Threshold')

        record = Record(datetime.now(), Apid, False)
        app = App.query.get(Apid)
        if app and app.Kvalue:
            if Kvalue != app.Kvalue:
                db.session.add(record)
                db.session.commit()
                return {'msg_code': 2}, 403  # 密钥错误
        else:
            db.session.add(record)
            db.session.commit()
            return {'msg_code': 3}, 404  # App不存在

        try:
            img = load_image_frombytes(Fimg)
        except Exception:
            db.session.add(record)
            db.session.commit()
            return {'msg_code': 4}, 415  # 图片文件格式无效或无法加载
        encoding_to_check, msg_code = encoding_fromarray(np.array(img))
        if msg_code != 1:
            db.session.add(record)
            db.session.commit()
            return {'msg_code': msg_code}

        face = Face.query.get(Fid)
        if face:
            if fr.compare_faces([str2en(face.Fencoding)], encoding_to_check, Threshold)[0]:
                same = True
                record.isSuccess = True
            else:
                same = False
            db.session.add(record)
            db.session.commit()
            return {'msg_code': 1, 'match': same}
        else:
            db.session.add(record)
            db.session.commit()
            return {'msg_code': 7}, 404  # 查询的人脸不存在


api.add_resource(FaceApi, '/api/face')
api.add_resource(SingleFace, '/api/singleface')
api.add_resource(Similarity, '/api/similarity')
api.add_resource(Detection, '/api/detection')
api.add_resource(Match, '/api/match')
