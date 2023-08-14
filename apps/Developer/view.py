import datetime
from flask import Blueprint, request, g, render_template, session, redirect, url_for, make_response
from apps.settings import Config
from models import *
import json
import requests
import base64
from sqlalchemy import extract

developer_bp = Blueprint('Developer', __name__, url_prefix='/developer')

# 需要进行权限验证的路由

required_login_list = ['/developer/', '/developer/myface', '/developer/myrecord', '/developer/mypassword',
                       '/alterpassword', '/developer/searchface', '/developer/myinfo', '/developer/searchpassword',
                       '/developer/deletepassword', '/developer/updatepassword', '/developer/addface',
                       '/developer/updateface', '/developer/addpassword']


# 判断是否已经登录
@developer_bp.before_app_request
def before_app_request():
    if request.path in required_login_list:  # 判断该路径是否需要权限验证
        if 'did' in session:
            Did = session['did']
            g.developer = Developer.query.get(Did)
        else:
            if 'aid' in session:
                Aid = session['aid']
                g.admin = Admin.query.get(Aid)
            else:
                return render_template('login.html', msg='请登录')


# 错误码转错误信息
def CodeToMessage(code):
    MessageDic = {1: '请求成功', 2: '请求失败，密钥错误', 3: '请求失败，外部应用不存在', 4: '请求失败，图片文件格式无效或无法加载',
                  5: '请求失败，未检测到人脸', 6: '请求失败，检测到多张人脸', 7: '请求失败，查询的人脸不存在', 8: '请求失败，视频文件格式无效或无法加载'}
    return MessageDic[code]


@developer_bp.route('/mypassword')
def MyPassword():
    applist = App.query.filter(Developer.Did == g.developer.Did)
    for app in applist:
        if app.Kdate.__lt__(datetime.datetime.date(datetime.datetime.now())):
            app.outofdate = 1
    db.session.commit()
    page_num = request.args.get('page', 1)
    passwordlist = App.query.filter(Developer.Did == g.developer.Did).paginate(page=int(page_num), per_page=12)

    return render_template('/Developer/mypassword.html', passwordlist=passwordlist)


@developer_bp.route('/myface')
def MyFace():
    page_num = request.args.get('page', 1)
    facelist = Face.query.join(App, Face.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
        .filter(Developer.Did == g.developer.Did).paginate(page=int(page_num), per_page=12)
    return render_template('/Developer/myface.html', facelist=facelist)


@developer_bp.route('/myrecord')
def MyRecord():
    page_num = request.args.get('page', 1)
    recordlist = Record.query.join(App, App.Apid == Record.Apid).join(Developer, Developer.Did == App.Did) \
        .filter(Developer.Did == g.developer.Did).paginate(page=int(page_num), per_page=12)
    return render_template('/Developer/myrecord.html', recordlist=recordlist)


@developer_bp.route('/searchface', methods=['post'])
def SearchFace():
    keyword = request.form.get('keyword')
    content = request.form.get('content')
    page_num = request.args.get('page', 1)
    if keyword == 'fid':
        facelist = Face.query.join(App, Face.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
            .filter(Developer.Did == g.developer.Did).filter(Face.Fid == content).paginate(page=int(page_num),
                                                                                           per_page=12)
    elif keyword == 'fname':
        facelist = Face.query.join(App, Face.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
            .filter(Developer.Did == g.developer.Did).filter(Face.Fname.contains(content)).paginate(page=int(page_num),
                                                                                                    per_page=12)
    else:
        facelist = Face.query.join(App, Face.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
            .filter(Developer.Did == g.developer.Did).filter(Face.Apid == content).paginate(page=int(page_num),
                                                                                            per_page=12)
    return render_template('/Developer/myface.html', facelist=facelist)


@developer_bp.route('/searchpassword', methods=['post'])
def SearchPassword():
    keyword = request.form.get('keyword')
    content = request.form.get('content')
    page_num = request.args.get('page', 1)
    if keyword == 'kid':
        passwordlist = App.query.filter(Developer.Did == g.developer.Did) \
            .filter(App.Apid == content).paginate(page=int(page_num), per_page=12)
    elif keyword == 'kname':
        passwordlist = App.query.filter(Developer.Did == g.developer.Did) \
            .filter(App.Kvalue.contains(content)).paginate(page=int(page_num), per_page=12)
    else:
        passwordlist = App.query.filter(Developer.Did == g.developer.Did) \
            .filter(App.Apname == content).paginate(page=int(page_num), per_page=12)
    return render_template('/Developer/mypassword.html', passwordlist=passwordlist)


@developer_bp.route('/myinfo')
def MyInfo():
    return render_template('/Developer/developerinfo.html', developer=g.developer)


@developer_bp.route('/addface', methods=['post', 'get'])
def AddFace():
    if request.method == 'GET':
        return render_template('/Developer/addface.html', msg='')
    else:
        fname = request.form.get('fname')
        apid = request.form.get('apid')
        Did = session['did']
        app = App.query.get(apid)
        if app.Developer.Did != Did:  # 检测用户输入的Apid和Did是否匹配
            return render_template('/Developer/addface.html', msg='应用编号错误')
        Kvalue = App.query.get(apid).Kvalue
        face = request.files.get('face')
        face_suffix = face.filename.rsplit('.')[-1]  # 取得文件格式
        if face_suffix not in ['gif', 'bmp', 'jpg']:  # 检查格式
            return render_template('/Developer/addface.html', msg="上传图片必须为jpg、png或bmp格式")
        else:
            base64_data = base64.b64encode(face.read())
            data = {'Fimg': base64_data, 'Fname': fname, 'Apid': apid, 'Kvalue': Kvalue}
            response = requests.post(Config.SERVER_IP + "/api/face", data=data)  # 调用api
            response_dic = json.loads(response.text)
            print(response_dic)
            msg_code = response_dic['msg_code']
            message = CodeToMessage(msg_code)
            return render_template('/Developer/addface.html', msg=message)


@developer_bp.route('/deleteface', methods=['get'])
def DeleteFace():
    Fid = request.args.get('fid')
    face = Face.query.get(Fid)
    Apid = face.App.Apid
    inputDid = face.App.Developer.Did
    realDid = session['did']
    Kvalue = App.query.get(Apid).Kvalue
    if realDid == inputDid:  # 检测权限
        data = {'Fid': Fid, 'Apid': Apid, 'Kvalue': Kvalue}
        response = requests.delete(Config.SERVER_IP + "/api/face", data=data)  # 调用api
    return redirect(url_for('Developer.MyFace'))


@developer_bp.route('/updateface', methods=['post', 'get'])
def UpdateFace():
    if request.method == 'GET':
        fid = request.args.get('fid')
        face = Face.query.get(fid)
        return render_template('/Developer/updateface.html', face=face)
    else:
        Did = session['did']
        fid = request.form.get('fid')
        face = Face.query.get(fid)
        fname = request.form.get('fname')
        apid = request.form.get('apid')
        if App.query.get(apid).Developer.Did != Did:  # 权限验证
            return render_template('/Developer/updateface.html', face= face,msg="应用编号不匹配")
        Kvalue = Face.query.get(fid).App.Kvalue
        face = request.files.get('face')
        face_suffix = face.filename.rsplit('.')[-1]  # 取得文件格式
        if face_suffix not in ['gif', 'bmp', 'jpg']:  # 检查格式
            return render_template('/Developer/updateface.html', face=face,msg="上传图片必须为jpg、png或bmp格式")
        else:
            base64_data = base64.b64encode(face.read())
            data = {'Fid': fid, 'Fimg': base64_data, 'Fname': fname, 'Apid': apid, 'Kvalue': Kvalue}
            response = requests.put(Config.SERVER_IP + "/api/face", data=data)  # 调用api
            response_dic = json.loads(response.text)
            msg_code = response_dic['msg_code']
            message = CodeToMessage(msg_code)
            return render_template('/Developer/updateface.html', face=face,msg=message)


@developer_bp.route('/checkface')
def CheckFace():
    return render_template('/Developer/checkface.html')


@developer_bp.route('/getface')
def GetFace():
    fid = request.args.get('fid')
    src = Face.query.get(fid).Fsrc
    suffix = src.rsplit('.')[-1]
    with open(src, 'rb') as f:
        bin = f.read()
    f.close()
    r = make_response(bin)
    r.headers['Content-Type'] = 'image/' + suffix
    return r


@developer_bp.route('deletepassword')
def deletepassword():
    id = request.args.get('id')
    # user = User.query.get(id)
    # user.isdelete = True
    # db.session.commit()
    user = App.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('Developer.MyPassword'))


@developer_bp.route('deleterecord')
def DeleteRecord():
    rid = request.args.get('rid')
    record = Record.query.get(rid)
    db.session.delete(record)
    db.session.commit()
    return redirect('/developer/myrecord')

@developer_bp.route('searchrecord')
def SearchRecord():
    keyword = request.form.get('keyword')
    content = request.form.get('content')
    page_num = request.args.get('page', 1)
    if keyword == 'rid':
        recordlist = Record.query.join(App, Record.Apid == App.Apid).join(Developer,App.Did == Developer.Did)\
                .filter(Developer.Did == g.developer.Did).filter(Record.Rid == content).paginate(page=int(page_num),
                                                                                           per_page=12)
    elif keyword == 'rtime':
        recordlist = Record.query.join(App, Record.Apid == App.Apid).join(Developer,App.Did == Developer.Did)\
                .filter(Developer.Did == g.developer.Did).filter(Record.Rtime.contains(content))\
                                                                            .paginate(page=int(page_num),per_page=12)
    else:
        recordlist = Record.query.join(App, Record.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
            .filter(Developer.Did == g.developer.Did).filter(Record.Apid == content) \
            .paginate(page=int(page_num), per_page=12)

    return render_template('/Developer/myrecord.html', recordlist = recordlist)

@developer_bp.route('updatepassword', methods=['post', 'get'])
def updatepassword():
    if request.method == 'GET':
        id = request.args.get('id')
        app = App.query.get(id)
        return render_template('/Developer/updatepassword.html', app=app)
    else:
        name = request.form.get('apname')
        id = request.form.get('apid')
        app = App.query.get(id)
        app.Apname = name
        db.session.commit()
        return redirect(url_for('Developer.MyPassword'))


@developer_bp.route('addpassword', methods=['post', 'get'])
def addpassword():
    if request.method == 'POST':
        name = request.form.get('apname')
        # app.Apname = name
        date = datetime.datetime.now()
        date1 = date + datetime.timedelta(days=+365)
        # app.Kdate = datetime.datetime.date(date1)
        # app.Did = session['did']
        app = App(session['did'], date1, name)
        db.session.add(app)
        db.session.commit()
        return render_template('/Developer/addpassword.html', msg='申请成功，等待管理员处理')
    else:
        return render_template('/Developer/addpassword.html', msg='')
    # if request.method == 'GET':
    #     return render_template('/Developer/addpassword.html', msg='')
    # else:
    #     name = request.form.get('apname')
    #     apid = request.form.get('apid')
    #     Did = session['did']
    #     app = App.query.get(apid)
    #     if app.Developer.Did != Did:  # 检测用户输入的Apid和Did是否匹配
    #         return render_template('/Developer/addpassword.html', msg='应用编号错误')
    #
    #     Kvalue = App.query.get(apid).Kvalue
    #     outofdate = App.query.get(apid).outofdate
    #     if Kvalue == None or outofdate == 1:
    #         a = string.ascii_letters + string.digits
    #         key = random.sample(a, 8)
    #         app.Kvalue = key
    #         db.session.commit()
    #         return redirect(url_for('Developer.MyPassword'))

@developer_bp.route('updaterecord',methods=['get','post'])
def UpdateRecord():
    if request.method == 'GET':
        rid = request.args.get('rid')
        record = Record.query.get(rid)
        return render_template('/Developer/updaterecord.html',record = record)
    else:
        rid = request.form.get('rid')
        record = Record.query.get(rid)
        rtime = request.form.get('rtime')
        isSuccess = True if request.form.get('isSuccess')=='是' else False
        apid = request.form.get('apid')
        did = session['did']
        if App.query.get(apid).Developer.Did != did: # 权限验证
            return render_template('/Developer/updaterecord.html', record=record,msg='请输入正确的应用编号')
        record.Rtime=rtime
        record.isSuccess=isSuccess
        record.apid = apid
        db.session.commit()
        return render_template('/Developer/updaterecord.html',record = record)


@developer_bp.route('/checkrecord')
def CheckRecord():
    rid = request.args.get('rid')
    return redirect('/developer/updaterecord?rid='+rid)

@developer_bp.route('/default')
def DeveloperDefault():
    Did = session['did']

    pCount = App.query.filter_by(Did=Did).count()
    fCount = Face.query.join(App, Face.Apid == App.Apid).join(Developer, App.Did == Developer.Did) \
        .filter(Developer.Did == Did).count()
    rCount = Record.query.join(App, App.Apid == Record.Apid).join(Developer, Developer.Did == App.Did) \
        .filter(Developer.Did == Did).count()
    version = System.query.order_by(System.time.desc()).first().version
    notice = System.query.order_by(System.time.desc()).first().notice
    time = System.query.order_by(System.time.desc()).first().time

    day_query = db.session.execute('select now();')
    today = day_query.fetchall()[0][0]  # 取得今天日期
    one_day = datetime.timedelta(days=1)
    i = 0
    dates = []
    values = []
    while i < 7:
        dates.append(today.strftime("%m-%d"))
        value = Record.query.filter(extract('month', Record.Rtime) == today.month) \
            .filter(extract('day', Record.Rtime) == today.day).count()
        values.append(value)
        today -= one_day
        i += 1
    dates.reverse()  # 过去过去七天的日期
    values.reverse()  # 取出对应的访问次数

    app_list = App.query.filter(App.Did==Did).all()
    for app in app_list:
        face_list = Face.query.filter(Face.Apid==app.Apid).all()
        app.count =len(face_list)
    return render_template("/body.html",pCount=pCount,fCount=fCount,rCount=rCount,version=version,notice=notice,\
                           time=time,dates=dates,values=values,app_list=app_list)

@developer_bp.route('test')
def TestDate():

    return "OK"