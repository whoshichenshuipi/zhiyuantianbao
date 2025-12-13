from flask import Blueprint, request, jsonify
from web.models.volunteer_plan import VolunteerPlan
from web import db
from web.decorator.permission import requires_roles, jwt_required

volunteer_bp = Blueprint('volunteer_plan', __name__, url_prefix='/api/volunteer')

@volunteer_bp.route('/plan', methods=['GET'])
@jwt_required
@requires_roles('student')
def list_volunteer_plans():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    user_id = request.args.get('user_id', type=int)
    query = VolunteerPlan.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@volunteer_bp.route('/plan/<int:plan_id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_volunteer_plan(plan_id):
    plan = VolunteerPlan.query.get(plan_id)
    if not plan:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": plan.to_dict()})

@volunteer_bp.route('/plan', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_volunteer_plan():
    data = request.get_json()
    plan = VolunteerPlan(
        user_id=data.get('user_id'),
        college_id=data.get('college_id'),
        major_id=data.get('major_id'),
        priority=data.get('priority'),
        status=data.get('status', 'draft')
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": plan.to_dict()})

@volunteer_bp.route('/plan/<int:plan_id>', methods=['PUT'])
@jwt_required
@requires_roles('student')
def update_volunteer_plan(plan_id):
    plan = VolunteerPlan.query.get(plan_id)
    if not plan:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['college_id', 'major_id', 'priority', 'status']:
        if field in data:
            setattr(plan, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": plan.to_dict()})

@volunteer_bp.route('/plan/<int:plan_id>', methods=['DELETE'])
@jwt_required
@requires_roles('student')
def delete_volunteer_plan(plan_id):
    plan = VolunteerPlan.query.get(plan_id)
    if not plan:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(plan)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})

@volunteer_bp.route('/recommend', methods=['POST'])
@jwt_required
@requires_roles('student')
def recommend_volunteer():
    """智能推荐接口 - 基于用户分数和偏好推荐志愿"""
    data = request.get_json()
    user_id = data.get('user_id')
    score = data.get('score')
    region_pref = data.get('region_pref')
    # TODO: 调用 recommendation_service 进行推荐计算
    # 暂时返回 mock 数据
    recommendations = [
        {"college_name": "清华大学", "major_name": "计算机科学", "probability": 0.75, "risk_level": "中"},
        {"college_name": "北京大学", "major_name": "软件工程", "probability": 0.68, "risk_level": "中"},
        {"college_name": "浙江大学", "major_name": "人工智能", "probability": 0.82, "risk_level": "低"},
    ]
    return jsonify({"code": 0, "msg": "成功", "data": recommendations})
