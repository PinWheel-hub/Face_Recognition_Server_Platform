from flask import Flask, url_for, request, render_template, redirect, Blueprint
from sqlalchemy import or_, and_
import random
import string
from apps.ext import db
from models import Developer, Record, App,System

admin_bp = Blueprint('Admin', __name__)


# 管理员处理申请
@admin_bp.route('/pwd_process')
def pwd_process():
    page_num = request.args.get('page', 1)
    passwordlist = App.query.filter(and_(Developer.Did == App.Did, App.Kvalue == None)).paginate(page=int(page_num),
                                                                                                 per_page=12)
    #print(passwordlist)
    return render_template('Admin/pwd_process.html', passwordlist=passwordlist)


@admin_bp.route('/permit')
def permit():
    id = request.args.get('id')
    app = App.query.get(id)
    a = string.ascii_letters + string.digits
    key = random.sample(a, 8)
    # print(key)
    # print(type(key))
    kvalue = "".join(key)
    app.Kvalue = kvalue
    db.session.commit()
    return redirect(url_for('Admin.pwd_process'))


@admin_bp.route('/deny')
def deny():
    id = request.args.get('id')
    # user = User.query.get(id)
    # user.isdelete = True
    # db.session.commit()
    app = App.query.get(id)
    db.session.delete(app)
    db.session.commit()
    return redirect(url_for('Admin.pwd_process'))


@admin_bp.route('/deletepassword')
def deletepassword():
    id = request.args.get('id')
    # user = User.query.get(id)
    # user.isdelete = True
    # db.session.commit()
    user = App.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('Admin.admin_password'))


@admin_bp.route('/updatepassword', methods=['post', 'get'])
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
        return redirect(url_for('Admin.admin_password'))


# 管理员管理页面
@admin_bp.route('/manage', endpoint='manage')
def admin_manage():
    page_num = request.args.get('page', 1)
    developers = Developer.query.paginate(page=int(page_num), per_page=12)
    return render_template('Admin/manage.html', developers=developers)


# 管理员管理密钥页面
@admin_bp.route('/password')
def admin_password():
    page_num = request.args.get('page', 1)
    passwordlist = App.query.join(Developer, Developer.Did == App.Did).add_entity(Developer).paginate(
        page=int(page_num), per_page=12)
    print(passwordlist.items)
    return render_template('Admin/password.html', passwordlist=passwordlist)


# 管理员查询密钥
@admin_bp.route('/search_passwords')
def search_passwords():
    return render_template('Admin/password.html')


# 查询开发者
@admin_bp.route('/search', endpoint='search')
def developer_search():
    keyword = request.args.get('search')
    developer_list = Developer.query.filter(
        or_(Developer.Dname == keyword, Developer.Dtel == keyword, Developer.Did == keyword)).all()
    print(keyword)
    return render_template('Admin/manage.html', developers=developer_list)


# 查询比对记录
@admin_bp.route('/query', endpoint='query')
def record_query():
    record_list = Record.query.all()
    return render_template('Admin/manage.html', records=record_list)


# 删除开发者
@admin_bp.route('/delete', endpoint='delete')
def developer_delete():
    Did = request.args.get('Did')
    print(Did)
    developer = Developer.query.get(Did)
    db.session.delete(developer)
    db.session.commit()
    return redirect(url_for('Admin.manage'))


# 查询开发者
@admin_bp.route('/search_developers', endpoint='search_developers', methods=['POST'])
def developer_search():
    keyword = request.form.get('keyword')
    content = request.form.get('content')
    page_num = request.args.get('page', 1)
    if keyword == 'Did':
        developer_list = Developer.query.filter(Developer.Did == content).paginate(page=int(page_num),
                                                                                   per_page=12)
    elif keyword == 'Dname':
        developer_list = Developer.query.filter(Developer.Dname == content).paginate(page=int(page_num),
                                                                                     per_page=12)
    else:
        developer_list = Developer.query.filter(Developer.Dtel == content).paginate(page=int(page_num),
                                                                                    per_page=12)

    return render_template('Admin/manage.html', developers=developer_list)


# 更新开发者
@admin_bp.route('/update', endpoint='update', methods=['GET', 'POST'])
def developer_update():
    if request.method == 'POST':
        Dname = request.form.get('Dname')
        Dtel = request.form.get('Dtel')
        Did = request.form.get('id')
        # 修改密码
        # Dpwd = request.form.get('Dpwd')
        # 更新app列表
        # AppList = request.form.get('AppList')
        # 更新appKey列表
        # AppKeyList = request.form.get('AppKeyList')
        developer = Developer.query.get(Did)
        developer.Dname = Dname
        developer.Dtel = Dtel
        db.session.commit()
        return redirect(url_for('Admin.manage'))
    else:
        Did = request.args.get('Did')
        developer = Developer.query.get(Did)
        return render_template('Admin/update.html', developer=developer)
        # jfuiweai


@admin_bp.route('/allrecord', methods=['GET', 'POST'])
def AllRecord():
    if request.method == 'GET':
        page_num = request.args.get('page', 1)
        recordlist = db.session.query(Developer.Did, Developer.Dname, Record.Rid, Record.Rtime, Record.Apid,
                                      Record.isSuccess).paginate(page=int(page_num), per_page=12)
        return render_template('/Admin/allrecord.html', recordlist=recordlist)

@admin_bp.route('/system', methods=['GET', 'POST'])
def system_config():
    if request.method == 'GET':
        current_version = request.args.get('version')
        if current_version is not None:
            system = System.query.filter(System.version==current_version).first()
        else:
            system = System.query.first()
        version_list =[]
        for sys_version in System.query.all():
            version_list.append(sys_version.version)

        return render_template('/Admin/systemconfig.html',system = system,version_list=version_list)

    elif request.method == 'POST':
        notice_content = request.form.get('ckeditor')
        version = request.form.get('version_input')
        time = request.form.get('time_input')
        new_system_info = System(notice=notice_content,version=version,time=time)
        db.session.add(new_system_info)
        db.session.commit()
        return redirect(url_for('Admin.system_config'))