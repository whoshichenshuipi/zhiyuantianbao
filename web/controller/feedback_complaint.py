from flask import Blueprint, request, jsonify
from web.models.feedback_complaint import FeedbackComplaint
from web import db
from web.decorator.permission import requires_roles, jwt_required

feedback_bp = Blueprint('feedback_complaint', __name__, url_prefix='/api/feedback')

@feedback_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('student')
def list_feedback():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = FeedbackComplaint.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@feedback_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_feedback(id):
    fb = FeedbackComplaint.query.get(id)
    if not fb:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": fb.to_dict()})

@feedback_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_feedback():
    data = request.get_json()
    fb = FeedbackComplaint(
        user_id=data.get('user_id'),
        type=data.get('type'),
        content=data.get('content'),
        attachment_path=data.get('attachment_path'),
        status=data.get('status')
    )
    db.session.add(fb)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": fb.to_dict()})

@feedback_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('admin')
def update_feedback(id):
    fb = FeedbackComplaint.query.get(id)
    if not fb:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['type', 'content', 'attachment_path', 'status']:
        if field in data:
            setattr(fb, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": fb.to_dict()})

@feedback_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('admin')
def delete_feedback(id):
    fb = FeedbackComplaint.query.get(id)
    if not fb:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(fb)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
