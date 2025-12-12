from web.routes import main_routes
from web.models import SysMenu, SysRole
from flask import jsonify, request
from web import db
from sqlalchemy import asc
from flask_login import login_required
from web.decorator import permission


@main_routes.route('/system/menu/list', methods=['GET'])
@login_required
@permission('system:menu:list')
def sys_menu_tree_grid():
    filters = []
    if 'menuName' in request.args:
        filters.append(SysMenu.menu_name.like('%' + request.args['menuName'] + '%'))
    if 'status' in request.args:
        filters.append(SysMenu.status == request.args['status'])

    order_by = []
    order_by.append(asc(getattr(SysMenu, 'parent_id')))
    order_by.append(asc(getattr(SysMenu, 'order_num')))

    res_list = db.session.query(SysMenu).filter(*filters).order_by(*order_by)

    return jsonify({"msg": "操作成功", "code": 200, "data": [org.to_json() for org in res_list]})


@main_routes.route('/system/menu/<id>', methods=['GET'])
@login_required
@permission('system:menu:query')
def sys_menu_get_id(id):
    res = db.session.query(SysMenu).get(id)

    if res:
        return jsonify({'code': 200, 'msg': '操作成功', 'data': res.to_json()})
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@main_routes.route('/system/menu', methods=['PUT'])
@login_required
@permission('system:menu:edit')
def sys_menu_update():
    res = db.session.query(SysMenu).get(request.json['menuId'])
    if 'icon' in request.json: res.icon = request.json['icon']
    if 'component' in request.json: res.component = request.json['component']
    if 'path' in request.json: res.path = request.json['path']
    if 'menuName' in request.json: res.menu_name = request.json['menuName']
    if 'orderNum' in request.json: res.order_num = request.json['orderNum']
    if 'perms' in request.json: res.perms = request.json['perms']
    if 'menuType' in request.json: res.menu_type = request.json['menuType']
    if 'parentId' in request.json: res.parent_id = request.json['parentId']
    if 'status' in request.json: res.status = request.json['status']
    if 'isCache' in request.json: res.is_cache = request.json['isCache']
    if 'isFrame' in request.json: res.is_frame = request.json['isFrame']
    if 'remark' in request.json: res.remark = request.json['remark']
    if 'visible' in request.json: res.visible = request.json['visible']
    if 'query' in request.json: res.query = request.json['query']
    if 'routeName' in request.json: res.route_name = request.json['routeName']

    db.session.add(res)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/menu', methods=['POST'])
@login_required
@permission('system:menu:add')
def sys_menu_add():
    res = SysMenu()
    if 'icon' in request.json: res.icon = request.json['icon']
    if 'component' in request.json: res.component = request.json['component']
    if 'path' in request.json: res.path = request.json['path']
    if 'menuName' in request.json: res.menu_name = request.json['menuName']
    if 'orderNum' in request.json: res.order_num = request.json['orderNum']
    if 'perms' in request.json: res.perms = request.json['perms']
    if 'menuType' in request.json: res.menu_type = request.json['menuType']
    if 'parentId' in request.json: res.parent_id = request.json['parentId']
    if 'status' in request.json: res.status = request.json['status']
    if 'isCache' in request.json: res.is_cache = request.json['isCache']
    if 'isFrame' in request.json: res.is_frame = request.json['isFrame']
    if 'remark' in request.json: res.remark = request.json['remark']
    if 'visible' in request.json: res.visible = request.json['visible']
    if 'query' in request.json: res.query = request.json['query']
    if 'routeName' in request.json: res.route_name = request.json['routeName']
    db.session.add(res)
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/menu/<id>', methods=['DELETE'])
@login_required
@permission('system:menu:remove')
def sys_menu_remove(id):
    res = db.session.query(SysMenu).get(id)
    if res:
        db.session.delete(res)
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/menu/treeselect', methods=['GET'])
@login_required
def sys_menu_tree_select():
    resList = db.session.query(SysMenu).filter(SysMenu.parent_id == 0)

    return jsonify({'msg': '操作成功', 'code': 200, "data": [res.to_tree_select_json() for res in resList]})


@main_routes.route('/system/menu/roleMenuTreeselect/<roleId>', methods=['GET'])
@login_required
def sys_menu_role_tree_select(roleId):
    role = SysRole.query.get(roleId)
    resList = db.session.query(SysMenu).filter(SysMenu.parent_id == 0)

    return jsonify({'msg': '操作成功', 'code': 200, \
        "menus": [res.to_tree_select_json() for res in resList], \
        "checkedKeys": [res.menu_id for res in role.resources]})

