# coding:utf-8
from web.routes import main_routes
from web.models import SysRole, SysMenu, SysUser, SysDept
from flask import request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import desc, asc
from web import db
from web.decorator import permission, dataScope


@main_routes.route('/system/role/authUser/cancelAll', methods=['PUT'])
@login_required
def cancel_all_role():
    roleId = request.args.get('roleId')
    userIds = request.args.get('userIds')
    #role = SysRole.query.get(roleId)
    idList = userIds.split(',')
    #toCancelUsers = [User.query.get(uid) for uid in idList]
    #role.users = [user2  for user2 in role.users.all() for user in toCancelUsers if user2.ID != user.ID ]
    for userId in idList:
        user = SysUser.query.get(userId)
        user.roles = [role for role in user.roles.all() if role.role_id != int(roleId)]
        db.session.add(user)

    return jsonify({'code': 200, 'msg': '取消成功'})


@main_routes.route('/system/role/authUser/cancel', methods=['PUT'])
@login_required
def cancel_role():
    roleId = request.json.get('roleId')
    userId = request.json.get('userId')
    user = SysUser.query.get(userId)
    user.roles = [role for role in user.roles.all() if role.role_id != int(roleId)]
    db.session.add(user)

    return jsonify({'code': 200, 'msg': '取消成功'})


@main_routes.route('/system/role/list', methods=['GET'])
@login_required
@permission('system:role:list')
@dataScope('sys_role.create_by')
def grid(filters=[]):
    if request.args.get('roleName'):
        filters.append(SysRole.role_name.like('%' + request.args.get('roleName') + '%'))
    if request.args.get('roleKey'):
        filters.append(SysRole.role_key.like('%' + request.args.get('roleKey') + '%'))
    if 'status' in request.args:
        filters.append(SysRole.status == request.args.get('status'))
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysRole.create_time >  request.args['params[beginTime]'])
        filters.append(SysRole.create_time <  request.args['params[endTime]'])

    order_by = []
    if request.form.get('sort'):
        if request.form.get('order') == 'asc':
            order_by.append(asc(getattr(SysRole,request.form.get('sort').upper())))
        elif request.form.get('order') == 'desc':
            order_by.append(desc(getattr(SysRole,request.form.get('sort').upper())))
        else:
            order_by.append(getattr(SysRole,request.form.get('sort').upper()))

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    # pagination = current_user.roles.filter(*filters).order_by(*order_by).paginate(page=page, per_page=rows, error_out=False)
    pagination = SysRole.query.filter(*filters).order_by(*order_by).paginate(page=page, per_page=rows, error_out=False)
    roles = pagination.items

    return jsonify({'rows': [role.to_json() for role in roles], 'total': pagination.total})


@main_routes.route('/system/role/<string:id>', methods=['GET'])
@login_required
@permission('system:role:query')
def sys_role_get_id(id):
    role = SysRole.query.get(id)
    if role:
        return jsonify({'code': 200, 'msg': '操作成功', 'data': role.to_json()})
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@main_routes.route('/system/role', methods=['PUT'])
@login_required
@permission('system:role:edit')
def sys_role_update():
    role = SysRole.query.get(request.json['roleId'])

    role.role_name = request.json['roleName']
    role.remark = request.json['remark']
    role.role_sort = request.json['roleSort']
    if 'roleKey' in request.json: role.role_key = request.json['roleKey']
    if 'dataScope' in request.json: role.data_scope = request.json['dataScope']

    if 'menuIds' in request.json:
        res_list = [db.session.query(SysMenu).get(menuId) for menuId in request.json['menuIds']]
        role.resources = res_list

    db.session.add(role)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/role', methods=['POST'])
@login_required
@permission('system:role:add')
def sys_role_add():
    role = SysRole()
    role.role_name = request.json['roleName']
    if 'roleKey' in request.json: role.role_key = request.json['roleKey']
    if 'remark' in request.json: role.remark = request.json['remark']
    if 'status' in request.json: role.status = request.json['status']

    role.role_sort = request.json['roleSort']
    if 'dataScope' in request.json: role.data_scope = request.json['dataScope']
    if 'menuIds' in request.json:
        res_list = [db.session.query(SysMenu).get(menuId) for menuId in request.json['menuIds']]
        role.resources = res_list
    # add current use to new role
    current_user.roles.append(role)
    db.session.add(role)
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/role/<string:id>', methods=['DELETE'])
@login_required
@permission('system:role:remove')
def sys_role_remove(id):
    role = SysRole.query.get(id)
    if role:
        db.session.delete(role)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/role/authUser/allocatedList', methods=['GET'])
@login_required
def allocatedList():
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysUser.query.join(SysRole, SysUser.roles).filter(SysRole.role_id == request.args['roleId']).paginate(
        page=page, per_page=rows, error_out=False)
    users = pagination.items

    return jsonify({'rows': [user.to_json() for user in users], 'total': pagination.total})


@main_routes.route('/system/role/authUser/unallocatedList', methods=['GET'])
@login_required
def unallocated_list():
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    # 子查询：查询在role_id=2中有关联的用户ID
    subquery = db.session.query(SysUser.user_id).join(SysUser.roles).filter(SysRole.role_id == int(request.args['roleId'])).group_by(SysUser.user_id).subquery()

    pagination = SysUser.query.filter(~SysUser.user_id.in_(subquery)).paginate(page=page, per_page=rows, error_out=False)
    # pagination = SysUser.query.join(SysRole, SysUser.roles).filter(or_(SysRole.role_id != int(request.args['roleId']), SysRole.role_id == None)).paginate(
    #     page=page, per_page=rows, error_out=False)
    users = pagination.items

    return jsonify({'rows': [user.to_json() for user in users], 'total': pagination.total})


@main_routes.route('/system/role/deptTree/<id>', methods=['GET'])
@login_required
def role_dept_tree_select(id):
    role = SysRole.query.get(id)
    depts = SysDept.query.filter(SysDept.parent_id == 0)
    deptIds_not = []
    if role.dept_check_strictly == 1:
        for dept in role.depts:
            if dept.parent_id not in deptIds_not:
                deptIds_not.append(dept.parent_id)
    return jsonify({'code': 200, 'msg': '操作成功', 'checkedKeys': [dept.dept_id for dept in role.depts if dept.dept_id not in deptIds_not], \
         'depts': [dept.to_tree_select_json() for dept in depts ]})


@main_routes.route('/system/role/dataScope', methods=['PUT'])
@login_required
def sys_role_data_scope():
    role = SysRole.query.get(request.json['roleId'])
    if 'deptCheckStrictly' in request.json: role.dept_check_strictly = request.json['deptCheckStrictly']
    if 'dataScope' in request.json: role.data_scope = request.json['dataScope']
    if 'deptIds' in request.json:
        dept_list = [SysDept.query.get(deptId) for deptId in request.json['deptIds']]
        role.depts = dept_list
    
    db.session.add(role)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/role/authUser/selectAll', methods=['PUT'])
@login_required
def sys_role_auth_user_select_all():
    role = SysRole.query.get(request.args.get('roleId'))
    userIds = request.args.get('userIds')
    user_ids_exit=[str(user.user_id) for user in role.users.all()]
    idList = userIds.split(',')
    for userId in idList:
        if not userId in user_ids_exit:
            user = SysUser.query.get(userId)
            user.roles.append(role)
            db.session.add(user)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/role/changeStatus', methods=['PUT'])
@login_required
@permission('system:role:edit')
def sys_role_status_update():
    role = SysRole.query.get(request.json['roleId'])

    if 'status' in request.json: role.STATUS = request.json['status']

    db.session.add(role)

    return jsonify({'code': 200, 'msg': '操作成功'})
