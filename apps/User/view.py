from flask import Blueprint, redirect, render_template, request, flash, g, session
from models import Developer,Admin
from apps.ext import db

user_bp = Blueprint('User',__name__,url_prefix=None)

@user_bp.route('/')
def index():
    return render_template('login.html')

# 登录
@user_bp.route('/login/',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    flag = request.form.get('identity')

    if flag == '1': # 判断是否是开发者
        developer = Developer.query.filter_by(Dname=username).first()
        if developer:
            if developer.Dpwd == password:
                session['did'] = developer.Did
                dname = developer.Dname
                return render_template('/Developer/developer.html',dname = dname)

    if flag == '0':    # 判断是否是管理员
        admin = Admin.query.filter_by(Aname=username).first()
        if admin:
            if admin.Apwd == password:
                session['aid'] = admin.Aid
                aname = admin.Aname
                return render_template('back.html',aname = aname)
    # 登录失败
    return render_template('login.html',msg='用户名或密码错误')

@user_bp.route('/makeregister/',endpoint='makeregister')
def makeRegister():
    return render_template('register.html')

@user_bp.route('/register/',endpoint='register',methods=['post'])
def userRegister():
    username = request.form.get('username')
    password = request.form.get('password')
    rpassword = request.form.get('rpassword')
    phone = request.form.get('phone')

    if password!=rpassword:
        return render_template('register.html',msg='两次输入的密码不一致')

    if len(phone)!=11 or (not phone.isdigit()):
        return render_template('register.html',msg='请输入正确的手机号')
    developer = Developer.query.filter_by(Dname=username).first()
    admin = Admin.query.filter_by(Aname=username).first()

    if developer or admin:
        render_template('register.html', msg='该用户名已被占用')

    newDeveloper = Developer(username,password,phone)
    db.session.add(newDeveloper)
    db.session.commit()     # 写入数据库中

    return render_template('register.html',msg='注册成功')

@user_bp.route('/body')
def body():
    return render_template('body.html')

# 修改密码
@user_bp.route('/alterpassword',methods=['post','get'],endpoint='alterpassword')
def alterpassword():
    if request.method =='POST':
        oldpassword = request.form.get('oldpassword')
        rpassword = request.form.get('rpassword')
        newpassword = request.form.get('newpassword')

        if newpassword != rpassword:
            return render_template('alterpassword.html',msg='两次输入的密码不一致')

        if hasattr(g,'developer'):
            if oldpassword != g.developer.Dpwd:
                return render_template('alterpassword.html', msg='密码错误')
            developer = Developer.query.get(g.developer.Did)
            developer.Dpwd=newpassword
            db.session.commit()
            return render_template('alterpassword.html',msg=('修改成功'))
        if hasattr(g,'admin'):
            if oldpassword != g.admin.Apwd:
                return render_template('alterpassword.html', msg='密码错误')
            admin = Admin.query.get(g.admin.Aid)
            admin.Apwd = newpassword
            db.session.commit()
            return render_template('alterpassword.html',msg='修改成功')
    else:
        return render_template('alterpassword.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')