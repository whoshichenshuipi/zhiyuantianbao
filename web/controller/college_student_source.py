from flask import Blueprint, request, jsonify
from web.models.college_student_source import CollegeStudentSource
from web import db
from web.decorator.permission import requires_roles, jwt_required

college_source_bp = Blueprint('college_student_source', __name__, url_prefix='/api/college_student_source')

@college_source_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('college')
def list_college_sources():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = CollegeStudentSource.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@college_source_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('college')
def get_college_source(id):
    src = CollegeStudentSource.query.get(id)
    if not src:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": src.to_dict()})

@college_source_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_college_source():
    data = request.get_json()
    src = CollegeStudentSource(
        college_id=data.get('college_id'),
        candidate_count=data.get('candidate_count'),
        score_distribution=data.get('score_distribution'),
        region_distribution=data.get('region_distribution')
    )
    db.session.add(src)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": src.to_dict()})

@college_source_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('admin')
def update_college_source(id):
    src = CollegeStudentSource.query.get(id)
    if not src:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['college_id', 'candidate_count', 'score_distribution', 'region_distribution']:
        if field in data:
            setattr(src, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": src.to_dict()})

@college_source_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('admin')
def delete_college_source(id):
    src = CollegeStudentSource.query.get(id)
    if not src:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(src)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
