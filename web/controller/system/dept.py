from web.routes import main_routes
from web.models import SysDept
from flask import jsonify, request
from flask_login import login_required
from web import db
from datetime import datetime
from web.decorator import permission


@main_routes.route('/system/dept/list', methods=['GET'])
@login_required
@permission('system:dept:list')
def sysdept_tree_grid():
    filters = []
    if 'deptName' in request.args:
        filters.append(SysDept.dept_name.like('%' + request.args['deptName'] + '%'))
    if 'status' in request.args:
        filters.append(SysDept.status == request.args['status'])
    orgs = SysDept.query.filter(*filters)
    return jsonify({'msg': '操作成功', 'code': 200, "data": [org.to_json() for org in orgs]})


@main_routes.route('/system/user/deptTree', methods=['GET'])
@login_required
def sysdept_tree_select():
    orgs = SysDept.query.filter(SysDept.parent_id == 0)
    return jsonify({'msg': '操作成功', 'code': 200, "data": [org.to_tree_select_json() for org in orgs]}) 


@main_routes.route('/system/dept/list/exclude/<id>', methods=['GET'])
@login_required
def sysdept_dept_list_exclude(id):
    orgs = SysDept.query.filter(SysDept.dept_id != id)

    return jsonify({'msg': '操作成功', 'code': 200, "data": [org.to_json() for org in orgs]})


@main_routes.route('/system/dept/<string:id>', methods=['GET'])
@login_required
@permission('system:dept:query')
def sysdept_getById(id):
    org = SysDept.query.get(id)

    if org:
        return jsonify({'msg': '操作成功', 'code': 200, 'data': org.to_json()})
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@main_routes.route('/system/dept', methods=['PUT'])
@login_required
@permission('system:dept:edit')
def sysdept_update():
    org = SysDept.query.get(request.json['deptId'])

    if 'deptName' in request.json:  org.dept_name = request.json['deptName']
    if 'email' in request.json: org.email = request.json['email']
    if 'leader' in request.json: org.leader = request.json['leader']
    if 'phone' in request.json: org.phone = request.json['phone']
    if 'orderNum' in request.json:  org.order_num = request.json['orderNum']
    if 'parentId' in request.json: org.parent_id = request.json['parentId']
    if 'status' in request.json: org.status = request.json['status']

    db.session.add(org)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dept', methods=['POST'])
@login_required
@permission('system:dept:add')
def sysdept_save():
    org = SysDept()
    if 'deptName' in request.json:  org.dept_name = request.json['deptName']
    if 'email' in request.json: org.email = request.json['email']
    if 'leader' in request.json: org.leader = request.json['leader']
    if 'phone' in request.json: org.phone = request.json['phone']
    if 'orderNum' in request.json: org.order_num = request.json['orderNum']
    if 'parentId' in request.json: org.parent_id = request.json['parentId']
    if 'status' in request.json: org.status = request.json['status']
    # add organization to current user
    # current_user.dept.append(org)
    db.session.add(org)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dept/<id>', methods=['DELETE'])
@login_required
@permission('system:dept:remove')
def sysdept_delete(id):
    res = SysDept.query.get(id)
    if res:
        db.session.delete(res)
    return jsonify({'code': 200, 'msg': '操作成功'})
