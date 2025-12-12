from web.routes import main_routes
from flask_login import login_required, current_user
from flask import g, jsonify ,current_app
from ..models import SysMenu
from web import db


def setAccessable(resource, permitedIDList):
    if resource.menu_id not in permitedIDList:
        resource.hidden = True
    for child in resource.children:
        setAccessable(child, permitedIDList)


@main_routes.route('/getRouters')
@login_required
def getRouters():
    """
    获取路由信息
    ---
    tags:
      - 路由信息
    description:
        获取路由信息接口，json格式
    responses:
      200:
          description: 路由信息
    """
    allSysMenu = db.session.query(SysMenu).filter(SysMenu.parent_id == 0,SysMenu.status == '0').all()
    if current_user.user_id !=1:
        resources = []
        resources += [res for role in current_user.roles for res in role.resources if role.resources]
        ids = [res.menu_id for res in resources]
        for res in allSysMenu:
           setAccessable(res, ids)

    json = [res.to_router_json() for res in allSysMenu]
    return jsonify({'msg': '操作成功', 'code': 200, "data": json})

@main_routes.route('/spec')
def spec():

    swagger_doc = swagger(current_app)
    swagger_doc['info']['version'] = "1.0"
    swagger_doc['info']['title'] = "My API"
    return swagger_doc