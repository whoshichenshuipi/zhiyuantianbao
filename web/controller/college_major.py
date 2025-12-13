from flask import Blueprint, request, jsonify
from web.models.college_major import CollegeMajor
from web import db
from web.decorator.permission import requires_roles, jwt_required

college_major_bp = Blueprint('college_major', __name__, url_prefix='/api/college_major')

@college_major_bp.route('/', methods=['GET'])
def list_college_majors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    query = CollegeMajor.query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@college_major_bp.route('/<int:id>', methods=['GET'])
def get_college_major(id):
    major = CollegeMajor.query.get(id)
    if not major:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": major.to_dict()})

@college_major_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_college_major():
    data = request.get_json()
    major = CollegeMajor(
        college_id=data.get('college_id'),
        major_id=data.get('major_id'),
        region=data.get('region'),
        level=data.get('level'),
        category=data.get('category'),
        course_setting=data.get('course_setting')
    )
    db.session.add(major)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": major.to_dict()})

@college_major_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('admin')
def update_college_major(id):
    major = CollegeMajor.query.get(id)
    if not major:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['college_id', 'major_id', 'region', 'level', 'category', 'course_setting']:
        if field in data:
            setattr(major, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": major.to_dict()})

@college_major_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('admin')
def delete_college_major(id):
    major = CollegeMajor.query.get(id)
    if not major:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(major)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
