from flask import Blueprint, request, jsonify
from web.models.admission_probability import AdmissionProbability
from web import db
from web.decorator.permission import requires_roles, jwt_required

admission_prob_bp = Blueprint('admission_probability', __name__, url_prefix='/api/admission_probability')

@admission_prob_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('student')
def list_admission_probabilities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = AdmissionProbability.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@admission_prob_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_admission_probability(id):
    prob = AdmissionProbability.query.get(id)
    if not prob:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": prob.to_dict()})

@admission_prob_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_admission_probability():
    data = request.get_json()
    prob = AdmissionProbability(
        plan_id=data.get('plan_id'),
        probability=data.get('probability'),
        risk_level=data.get('risk_level'),
        analysis_data=data.get('analysis_data')
    )
    db.session.add(prob)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": prob.to_dict()})

@admission_prob_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('student')
def update_admission_probability(id):
    prob = AdmissionProbability.query.get(id)
    if not prob:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['plan_id', 'probability', 'risk_level', 'analysis_data']:
        if field in data:
            setattr(prob, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": prob.to_dict()})

@admission_prob_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('student')
def delete_admission_probability(id):
    prob = AdmissionProbability.query.get(id)
    if not prob:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(prob)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
