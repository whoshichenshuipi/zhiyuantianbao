from flask import Blueprint, request, jsonify
from web.models.college_info import CollegeInfo
from web import db
from web.decorator.permission import requires_roles, jwt_required

college_info_bp = Blueprint('college_info', __name__, url_prefix='/api/college_info')

@college_info_bp.route('/', methods=['GET'])
def list_college_info():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = CollegeInfo.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@college_info_bp.route('/<int:id>', methods=['GET'])
def get_college_info(id):
    info = CollegeInfo.query.get(id)
    if not info:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": info.to_dict()})

@college_info_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_college_info():
    data = request.get_json()
    info = CollegeInfo(
        name=data.get('name'),
        intro=data.get('intro'),
        photo=data.get('photo'),
        specialties=data.get('specialties')
    )
    db.session.add(info)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": info.to_dict()})

@college_info_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('admin')
def update_college_info(id):
    info = CollegeInfo.query.get(id)
    if not info:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['name', 'intro', 'photo', 'specialties']:
        if field in data:
            setattr(info, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": info.to_dict()})

@college_info_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('admin')
def delete_college_info(id):
    info = CollegeInfo.query.get(id)
    if not info:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(info)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
