from flask import jsonify

# Dummy jwt_required decorator to avoid external dependency
def jwt_required(fn=None):
    if fn is None:
        return lambda f: f
    return fn

from functools import wraps
from flask_login import current_user


def permission(permission_id):
    def need_permission(func):
        @wraps(func)
        def inner(*args, **kargs):
            if not current_user.user_id:
                return jsonify(401, {"msg": "认证失败，无法访问系统资源"})
            else:
                if current_user.user_id ==1:
                    return func(*args, **kargs)
                resources = []
                resource_tree = []
                resources += [res for role in current_user.roles for res in role.resources if role.resources]
                # remove repeat
                new_dict = dict()
                for obj in resources:
                    if obj.menu_id not in new_dict:
                        new_dict[obj.menu_id] = obj
                for resource in new_dict.values():
                    resource_tree.append(resource.perms)
                if permission_id in resource_tree:
                    return func(*args, **kargs)
                else:
                    return jsonify({'msg': '当前操作没有权限', 'code': 403})
        return inner
    return need_permission


def requires_roles(*roles):
    """角色校验装饰器，检查当前用户是否拥有指定角色"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'code': 401, 'msg': '未登录'})
            # 超级管理员跳过角色检查
            if current_user.user_id == 1:
                return func(*args, **kwargs)
            # 获取用户角色列表
            user_roles = [role.role_key for role in current_user.roles]
            # 检查是否拥有任一所需角色
            if any(role in user_roles for role in roles):
                return func(*args, **kwargs)
            return jsonify({'code': 403, 'msg': '当前角色没有权限'})
        return wrapper
    return decorator

