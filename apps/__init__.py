from flask import Flask
from apps.User.view import user_bp
from apps.Admin.view import admin_bp
from apps.Developer.view import developer_bp
from apps.api.face_api import face_api_bp
from apps.api.video_anti_spoofing import anti_spoofing_bp
from apps.settings import Config
from apps.ext import db
from flask_ckeditor import CKEditor

ckeditor = CKEditor()

def create_app():
        app = Flask(__name__,template_folder='../templates',static_folder='../static')
        app.config.from_object(Config)  # 修改配置属性
        db.init_app(app)
        ckeditor.init_app(app)

        # 注册蓝图
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(developer_bp)
        app.register_blueprint(face_api_bp)
        app.register_blueprint(anti_spoofing_bp)
        return app
