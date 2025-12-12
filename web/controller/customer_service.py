from flask import Blueprint, request, jsonify
from web.models.customer_service import CustomerService
from web import db
from web.decorator.permission import requires_roles, jwt_required

cs_bp = Blueprint('customer_service', __name__, url_prefix='/api/customer_service')

@cs_bp.route('/', methods=['GET'])
@jwt_required
@requires_roles('student')
def list_customer_service():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = CustomerService.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@cs_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_customer_service(id):
    cs = CustomerService.query.get(id)
    if not cs:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": cs.to_dict()})

@cs_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('student')
def create_customer_service():
    data = request.get_json()
    cs = CustomerService(
        user_id=data.get('user_id'),
        college_id=data.get('college_id'),
        type=data.get('type'),
        message=data.get('message'),
        timestamp=data.get('timestamp')
    )
    db.session.add(cs)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": cs.to_dict()})

@cs_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('student')
def update_customer_service(id):
    cs = CustomerService.query.get(id)
    if not cs:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['type', 'message', 'timestamp']:
        if field in data:
            setattr(cs, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": cs.to_dict()})

@cs_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('student')
def delete_customer_service(id):
    cs = CustomerService.query.get(id)
    if not cs:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(cs)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
