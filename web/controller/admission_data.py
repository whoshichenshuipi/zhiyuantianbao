from flask import Blueprint, request, jsonify
from web.models.admission_data import AdmissionData
from web import db
from web.decorator.permission import requires_roles, jwt_required

admission_data_bp = Blueprint('admission_data', __name__, url_prefix='/api/admission_data')

@admission_data_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('college')
def list_admission_data():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = AdmissionData.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@admission_data_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('college')
def get_admission_data(id):
    record = AdmissionData.query.get(id)
    if not record:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": record.to_dict()})

@admission_data_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('college')
def create_admission_data():
    data = request.get_json()
    record = AdmissionData(
        college_id=data.get('college_id'),
        major_id=data.get('major_id'),
        year=data.get('year'),
        province=data.get('province'),
        score_line=data.get('score_line'),
        rank=data.get('rank')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": record.to_dict()})

@admission_data_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('college')
def update_admission_data(id):
    record = AdmissionData.query.get(id)
    if not record:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['college_id', 'major_id', 'year', 'province', 'score_line', 'rank']:
        if field in data:
            setattr(record, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": record.to_dict()})

@admission_data_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('college')
def delete_admission_data(id):
    record = AdmissionData.query.get(id)
    if not record:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
