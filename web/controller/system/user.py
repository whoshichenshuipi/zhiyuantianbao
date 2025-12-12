# coding:utf-8
from web.routes import main_routes
from web.models import SysUser, SysDept, SysRole, SysLogininfor, SysPost
from flask import request, jsonify, current_app, url_for
import bcrypt
import re
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from web import db, cache
import uuid
from sqlalchemy import asc, desc
import flask_excel as excel
from web.utils import captcha, tool
from .config import select_config_key
from web.decorator import permission, dataScope
import os


@main_routes.route('/system/user/authRole', methods=['PUT'])
@login_required
@permission('system:role:edit')
def grant_user_role():
    """
    修改用户信息
    ---
    tags:
      - 用户信息
    description:
        修改用户信息接口，json格式
    parameters:
      - name: userId
        type: string
        required: true
        description: 用户id
      - name: roleIds
        type: string
        required: true
        description: 角色id
    responses:
      200:
          description: 用户信息
    """
    id = request.args['userId']
    ids = request.args['roleIds']
    user = SysUser.query.get(id)

    if not ids:
        user.roles = []
    else:
        idList = ids.split(',')
        user.roles = [SysRole.query.get(rid) for rid in idList]

    db.session.add(user)

    return jsonify({'code': 200, 'msg': '操作成功'})


def record_login_history(status,msg,user_name):
    user_agent_str = request.headers.get('User-Agent')
    # 解析操作系统信息
    os_pattern = re.compile(r'(Windows|Linux|Mac OS|iOS|Android)')
    os_match = os_pattern.search(user_agent_str)
    operating_system = os_match.group(1) if os_match else "未知操作系统"
    # 解析浏览器信息
    browser_pattern = re.compile(r'(Chrome|Firefox|Safari|Edge|Internet Explorer|Opera)')
    browser_match = browser_pattern.search(user_agent_str)
    browser = browser_match.group(1) if browser_match else "未知浏览器"
    logininfor = SysLogininfor()
    logininfor.user_name = user_name
    logininfor.ipaddr = request.remote_addr
    logininfor.login_location =''
    logininfor.browser = browser
    logininfor.os = operating_system
    logininfor.status = status
    logininfor.msg = msg
    logininfor.login_time = datetime.now()
    db.session.add(logininfor)


@login_required
def record_login_info(user):
    user.login_ip = request.remote_addr
    user.login_date = datetime.now()
    db.session.commit()


@main_routes.route('/logout', methods=['POST'])
@login_required
def do_logout():
    record_login_history(0,'退出成功',current_user.user_name)
    logout_user()
    return jsonify({'msg': '退出成功~', 'code': 200})


@main_routes.route('/login', methods=['POST'])
def do_login():
    verify_key = cache.get(f'captcha_codes@验证码@{request.json["uuid"]}')
    if verify_key is None:
        return jsonify({'msg': '验证码已失效', 'code': 500})
    elif verify_key != request.json['code']:
        return jsonify({'msg': '验证码错误', 'code': 500})
    # 检查用户名是否存在
    user = SysUser.query.filter_by(user_name=request.json['username']).first()
    if user is not None:
        if user.status != "0":
            record_login_history("1", "登录失败", request.json['username'])
            return jsonify({'msg': '登录失败,账号状态无效', 'code': 500})
        # 密码同数据库哈希密码比较
        if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            # 更新用户表 LoginIp和LoginDate
            record_login_info(user)
            record_login_history("0", "登录成功", request.json['username'])
            token = tool.generate_token(user.user_id, current_app.secret_key)  # str(uuid.uuid4())
            return jsonify({'msg': '登录成功~', 'code': 200, 'url': '/', 'token': token})
    record_login_history("1", "登录失败", request.json['username'])
    return jsonify({'msg': '登录失败,账号密码错误~', 'code': 500})


@main_routes.route('/captchaImage', methods=['GET'])
def captcha_image():
    captcha_enabled = True if select_config_key('sys.account.captchaEnabled').config_value == 'true' else False
    if captcha_enabled:
        # with current_app.app_context():
            uuid_str = str(uuid.uuid4())
            captcha_type = current_app.config['CAPTCHA_TYPE']
            captcha_image_base64, captcha_text, result = captcha.generate_captcha_image_base64(captcha_type)
            cache.set(f'captcha_codes@验证码@{uuid_str}', result, timeout=60)
            return jsonify({'msg': '操作成功', 'code': 200, 'captchaEnabled': captcha_enabled, 'uuid': uuid_str, 'img': captcha_image_base64})
    else:
        return jsonify({'msg': '操作成功', 'code': 200, 'captchaEnabled': captcha_enabled})


@main_routes.route('/system/user/list', methods=['GET'])
@login_required
@permission('system:user:list')
@dataScope('sys_user.create_by')
def user_grid(filters=[]):
    if 'userName' in request.args:
        filters.append(SysUser.user_name.like('%' + request.args['userName'] + '%'))
    if 'phonenumber' in request.args:
        filters.append(SysUser.phonenumber.like('%' + request.args['phonenumber'] + '%'))
    if 'status' in request.args:
        filters.append(SysUser.status == request.args['status'])
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysUser.create_time > request.args['params[beginTime]'])
        filters.append(SysUser.create_time < request.args['params[endTime]'])

    order_by = []
    if request.form.get('sort'):
        if request.form.get('order') == 'asc':
            order_by.append(asc(getattr(SysUser, request.form.get('sort').upper())))
        elif request.form.get('order') == 'desc':
            order_by.append(desc(getattr(SysUser, request.form.get('sort').upper())))
        else:
            order_by.append(getattr(SysUser, request.form.get('sort').upper()))

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    if 'deptId' in request.args:
        # Define a recursive CTE
        dept_cte = (
            db.session.query(SysDept.dept_id)
            .filter(SysDept.dept_id == request.args['deptId'])
            .cte('dept_tree', recursive=True)
        )

        # Recursive part of the CTE
        dept_cte = dept_cte.union_all(
            db.session.query(SysDept.dept_id)
            .join(dept_cte, SysDept.parent_id == dept_cte.c.dept_id)
        )
        pagination = SysUser.query.join(
            dept_cte, SysUser.dept_id == dept_cte.c.dept_id).filter(*filters).params(
            dept_id=request.args['deptId']).order_by(*order_by).paginate(
            page=page, per_page=rows, error_out=False)
    else:
        pagination = SysUser.query.filter(*filters).order_by(*order_by).paginate(
            page=page, per_page=rows, error_out=False)
    users = pagination.items
    return jsonify({'rows': [user.to_json() for user in users], 'total': pagination.total, 'code': 200, 'msg': '查询成功'})


@main_routes.route('/system/user/', methods=['GET'])
@login_required
def sysuser_get():
    json = {'code': 200, 'msg': ''}
    json['roles'] = [role.to_json() for role in SysRole.query.all()]
    json['posts'] = [post.to_json() for post in SysPost.query.all()]
    return jsonify(json)


@main_routes.route('/system/user/<id>', methods=['GET'])
@login_required
@permission('system:user:query')
def sysuser_query(id):
    user = SysUser.query.get(id)

    if user:
        json = {'code': 200, 'msg': '', 'data': user.to_json()}
        if len(user.roles.all()) > 0:
            # json['roles'] = [role.to_json() for role in user.roles]
            json['roles'] = [role.to_json() for role in SysRole.query.all()]
            json['roleIds'] = [role.role_id for role in user.roles]
            json['posts'] = [post.to_json() for post in SysPost.query.all()]
            json['postIds'] = [post.post_id for post in user.posts]

        return jsonify(json)
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@main_routes.route('/system/user', methods=['PUT'])
@login_required
@permission('system:user:edit')
def sysuser_update():
    id = request.json['userId']
    user = SysUser.query.get(id)
    if 'nickName' in request.json: user.nick_name = request.json['nickName']
    if 'sex' in request.json: user.sex = request.json['sex']
    if 'email' in request.json: user.email = request.json['email']
    if 'phonenumber' in request.json: user.phonenumber = request.json['phonenumber']
    if 'deptId' in request.json: user.dept_id = request.json['deptId']
    if 'roleIds' in request.json: user.roles = [SysRole.query.get(roleId) for roleId in request.json['roleIds']]
    if 'postIds' in request.json: user.posts = [SysPost.query.get(postId) for postId in request.json['postIds']]
    if 'status' in request.json: user.status = request.json['status']
    if 'remark' in request.json: user.remark = request.json['remark']

    db.session.add(user)

    return jsonify({'code': 200, 'msg': '更新成功！'})


@main_routes.route('/system/user', methods=['POST'])
@login_required
@permission('system:user:add')
def sysuser_add():
    if SysUser.query.filter_by(user_name = request.json['userName']).first():
        return jsonify({'code': 500, 'msg': '新建用户失败，用户名已存在！'})

    user = SysUser()
    # 对密码进行哈希处理
    user.password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt(rounds=10))

    with db.session.no_autoflush:
        if 'nickName' in request.json: user.nick_name = request.json['nickName']
        if 'sex' in request.json: user.sex = request.json['sex']
        if 'email' in request.json: user.email = request.json['email']
        if 'phonenumber' in request.json: user.phonenumber = request.json['phonenumber']
        if 'deptId' in request.json: user.dept_id = request.json['deptId']
        if 'roleIds' in request.json:
            user.roles = [SysRole.query.get(roleId) for roleId in request.json['roleIds']]
        if 'postIds' in request.json:
            user.posts = [SysPost.query.get(postId) for postId in request.json['postIds']]
        if 'status' in request.json: user.status = request.json['status']
        if 'remark' in request.json: user.remark = request.json['remark']

        user.user_name = request.json['userName']

        # add current use to new user
        #current_user.roles.append(user)

        db.session.add(user)

    return jsonify({'code': 200, 'msg': '新建用户成功！'})


@main_routes.route('/system/user/<id>', methods=['DELETE'])
@login_required
@permission('system:user:remove')
def sysuser_remove(id):
    user = SysUser.query.get(id)
    if user:
        db.session.delete(user)

    return jsonify({'code': 200, 'msg': '删除成功'})


@main_routes.route('/system/user/profile/updatePwd', methods=['PUT']) 
@login_required
def sysuser_update_pwd():
    user = SysUser.query.get(current_user.user_id)
    if user:
        if not bcrypt.checkpw(request.args.get('oldPassword').encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'code': 400, 'msg': '旧密码错误'})
        # 对密码进行哈希处理
        user.password = bcrypt.hashpw(request.args.get('newPassword').encode('utf-8'), bcrypt.gensalt(rounds=10))
        db.session.add(user)
    return jsonify({'code': 200, 'msg': '修改成功'})


@main_routes.route('/getInfo', methods=['GET'])
@login_required
def sysuser_info():
    resources = []
    resourceTree = []
    if current_user.user_id!=1:
        resources += [res for role in current_user.roles for res in role.resources if role.resources]
        # remove repeat
        new_dict = dict()
        for obj in resources:
            if obj.menu_id not in new_dict:
                new_dict[obj.menu_id] = obj

        for resource in new_dict.values():
            resourceTree.append(resource.perms)
    else:
        resourceTree.append('*:*:*')

    return jsonify({'msg': '登录成功~', 'code': 200, \
        # 'user1': {'userName': current_user.user_name, 'avatar': current_user.avatar, 'nickName': current_user.nick_name, 'userId': current_user.user_id}, \
        'user':current_user.to_json(),\
        'roles': [role.role_key for role in current_user.roles], 'permissions': resourceTree})


@main_routes.route('/system/user/profile', methods=['GET'])
@login_required
def sysuser_profile():
     return jsonify({'msg': '操作成功', 'code': 200, \
        'data': current_user.to_json(), \
        'postGroup': ', '.join([post.post_name for post in current_user.posts]), \
        'roleGroup': ', '.join([role.role_name for role in current_user.roles])})


@main_routes.route('/system/user/profile', methods=['PUT'])
@login_required
def sysuser_update_profile():
    user = SysUser.query.get(current_user.user_id)
    if 'nickName' in request.json: user.nick_name = request.json['nickName']
    if 'sex' in request.json: user.sex = request.json['sex']
    if 'email' in request.json: user.email = request.json['email']
    if 'phonenumber' in request.json: user.phonenumber = request.json['phonenumber']

    db.session.add(user)

    return jsonify({'code': 200, 'msg': '更新成功！'})


@main_routes.route('/system/user/profile/avatar', methods=['POST'])
@login_required
def sysuser_upload_profile_file():
    user_id = current_user.user_id
    file = request.files['avatarfile']
    new_filename = f'{user_id}_{datetime.now().strftime("%Y%m%d%H%M%S%f")}'
    path = os.path.join(current_app.root_path, 'static', current_app.config['PROFILE'])
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, new_filename))
    filename = f'{current_app.config["PROFILE"]}/{new_filename}'

    current_user.avatar = filename
    file_url = url_for('static', filename=filename, _external=True)
    return jsonify({'code': 200, 'msg': '更新成功！', 'imgUrl': file_url})


@main_routes.route('/system/user/authRole/<id>', methods=['GET'])
@login_required
def sysuser_auth_role(id):
    user = SysUser.query.get(id)
    userRoles = [role for role in user.roles]
    allRoles = SysRole.query.all()
    for allRole in allRoles:
        for userRole in userRoles:
            if userRole.role_id == allRole.role_id:
                allRole.flag = True

    return jsonify({'code': 200, 'msg': '操作成功', 'roles': [role.to_json() for role in allRoles], 'user': user.to_json()})


@main_routes.route('/system/user/export', methods=['POST'])
@login_required
def sysuser_export():
    rows = []
    rows.append(['登录名', '姓名', '创建时间', '修改时间', '性别'])

    users = SysUser.query.all()
    for user in users:
        row = []
        row.append(user.user_name)
        row.append(user.nick_name)
        row.append(user.create_time)
        row.append(user.update_time)
        if user.sex == '0':
            row.append('女')
        elif user.sex == '1':
            row.append('男')
        rows.append(row)

    return excel.make_response_from_array(rows, "xlsx",
                                          file_name="user")


@main_routes.route('/system/user/changeStatus', methods=['PUT'])
@login_required
@permission('system:user:edit')
def sysuser_status_update():
    user = SysUser.query.get(request.json['userId'])
    if 'status' in request.json: user.status = request.json['status']
    db.session.add(user)

    return jsonify({'code': 200, 'msg': '操作成功'})

