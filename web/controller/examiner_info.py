from flask import Blueprint, request, jsonify
from web.models.examiner_info import ExaminerInfo
from web import db
from web.decorator.permission import requires_roles, jwt_required

examiner_bp = Blueprint('examiner', __name__, url_prefix='/api/examiner')

@examiner_bp.route('/info', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_or_update_examiner():
    data = request.get_json()
    user_id = data.get('user_id')
    examiner = ExaminerInfo.query.filter_by(user_id=user_id).first()
    if examiner:
        # update fields
        examiner.interest = data.get('interest')
        examiner.region_pref = data.get('region_pref')
        examiner.subject_strength = data.get('subject_strength')
        examiner.score = data.get('score')
    else:
        examiner = ExaminerInfo(
            user_id=user_id,
            interest=data.get('interest'),
            region_pref=data.get('region_pref'),
            subject_strength=data.get('subject_strength'),
            score=data.get('score')
        )
        db.session.add(examiner)
    db.session.commit()
    return jsonify({"code": 0, "msg": "成功", "data": examiner.to_dict()})

@examiner_bp.route('/info/<int:user_id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_examiner(user_id):
    examiner = ExaminerInfo.query.filter_by(user_id=user_id).first()
    if not examiner:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": examiner.to_dict()})
