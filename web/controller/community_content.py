from flask import Blueprint, request, jsonify
from web.models.community_content import CommunityContent
from web import db
from web.decorator.permission import requires_roles, jwt_required

community_bp = Blueprint('community_content', __name__, url_prefix='/api/community')

@community_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('student')
def list_community():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = CommunityContent.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@community_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_community(id):
    item = CommunityContent.query.get(id)
    if not item:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": item.to_dict()})

@community_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_community():
    data = request.get_json()
    item = CommunityContent(
        user_id=data.get('user_id'),
        title=data.get('title'),
        body=data.get('body'),
        type=data.get('type'),
        parent_id=data.get('parent_id')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": item.to_dict()})

@community_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('student')
def update_community(id):
    item = CommunityContent.query.get(id)
    if not item:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['title', 'body', 'type', 'parent_id']:
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": item.to_dict()})

@community_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('student')
def delete_community(id):
    item = CommunityContent.query.get(id)
    if not item:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
