# 数据库模型
from apps.ext import db

'''
数据库初始化方法: 
1.在命令行输入python app.py db migrate
2.上一条命令执行后再输入python app.py db upgrade
'''


# 开发者
class Developer(db.Model):
    __tablename__ = 'developer'
    Did = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Dname = db.Column(db.String(20), nullable=False)
    Dpwd = db.Column(db.String(30))
    Dtel = db.Column(db.Integer)
    Dmale = db.Column(db.Boolean)
    Demail = db.Column(db.String(50))
    Dbirth = db.Column(db.Date)
    isDelete = db.Column(db.Boolean, default=False)
    AppList = db.relationship('App', backref='Developer', cascade='all, delete-orphan', passive_deletes=True)

    def __init__(self, Dname, Dpwd, Dtel):
        self.Dname = Dname
        self.Dpwd = Dpwd
        self.Dtel = Dtel

    def __repr__(self):
        return '<Developer %r>' % self.Dname


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    Aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Aname = db.Column(db.String(30), nullable=False)
    Apwd = db.Column(db.String(30), nullable=False)

    def __init__(self, Aname, Apwd):
        self.Aname = Aname
        self.Apwd = Apwd

    def __repr__(self):
        return '<Admin %r>' % self.Aname


# 外部应用
class App(db.Model):
    __tablename__ = 'app'
    Apid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Apname = db.Column(db.String(30), nullable=True)
    Kvalue = db.Column(db.String(50), nullable=True)  # 密钥值
    Kdate = db.Column(db.Date, nullable=True)  # 密钥过期日期
    outofdate = db.Column(db.Boolean, nullable=True)
    Did = db.Column(db.Integer, db.ForeignKey('developer.Did', ondelete='CASCADE'), nullable=False)
    FaceList = db.relationship('Face', backref='App', cascade='all, delete-orphan', passive_deletes=True)
    RecordList = db.relationship('Record', backref='App', cascade='all, delete-orphan', passive_deletes=True)

    def __init__(self, Did, KDate, Apname='未命名', ):
        self.Apname = Apname
        self.Did = Did
        # self.Kvalue = Kvalue
        self.Kdate = KDate

    def __repr__(self):
        return '<App %r>' % self.Apname


# 人脸
class Face(db.Model):
    __tablename__ = 'face'
    Fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fsrc = db.Column(db.String(100), nullable=False)
    Fencoding = db.Column(db.String(1024), nullable=False)
    Fname = db.Column(db.String(30), nullable=True)
    Apid = db.Column(db.Integer, db.ForeignKey('app.Apid', ondelete='CASCADE'), nullable=False)

    def __init__(self, Fsrc, Fencoding, Fname, Apid):
        self.Fsrc = Fsrc
        self.Fencoding = Fencoding
        self.Apid = Apid
        self.Fname = Fname

    def __repr__(self):
        return '<Face %r>' % self.Fname


# 比对记录
class Record(db.Model):
    __tablename__ = 'record'
    Rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Rtime = db.Column(db.DateTime, nullable=False)  # 比对时间
    Apid = db.Column(db.Integer, db.ForeignKey('app.Apid', ondelete='CASCADE'), nullable=False)  # 比对时的应用/密钥id
    isSuccess = db.Column(db.Boolean, nullable=False)  # 比对是否成功

    def __init__(self, Rtime, Apid, isSuccess):
        self.Rtime = Rtime
        self.Apid = Apid
        self.isSuccess = isSuccess

    def __repr__(self):
        return '<Record %r>' % self.Apid


# 系统数据
class System(db.Model):
    __tablename__ = 'system'
    id = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.Date,nullable=False)
    notice = db.Column(db.String(200))
    version = db.Column(db.String(20))
