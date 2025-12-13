from flask import Blueprint, request, jsonify
from web.models.news_policy import NewsPolicy
from web import db
from web.decorator.permission import requires_roles, jwt_required

news_bp = Blueprint('news_policy', __name__, url_prefix='/api/news')

@news_bp.route('/', methods=['GET'])
def list_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    pagination = NewsPolicy.query.paginate(page=page, per_page=per_page, error_out=False)
    data = [item.to_dict() for item in pagination.items]
    return jsonify({"code": 0, "msg": "成功", "data": {"rows": data, "total": pagination.total}})

@news_bp.route('/<int:id>', methods=['GET'])
@jwt_required
@requires_roles('student')
def get_news(id):
    news = NewsPolicy.query.get(id)
    if not news:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    return jsonify({"code": 0, "msg": "成功", "data": news.to_dict()})

@news_bp.route('/', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_news():
    data = request.get_json()
    news = NewsPolicy(
        title=data.get('title'),
        content=data.get('content'),
        category=data.get('category'),
        status=data.get('status'),
        publish_time=data.get('publish_time')
    )
    db.session.add(news)
    db.session.commit()
    return jsonify({"code": 0, "msg": "创建成功", "data": news.to_dict()})

@news_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@requires_roles('admin')
def update_news(id):
    news = NewsPolicy.query.get(id)
    if not news:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    data = request.get_json()
    for field in ['title', 'content', 'category', 'status', 'publish_time']:
        if field in data:
            setattr(news, field, data[field])
    db.session.commit()
    return jsonify({"code": 0, "msg": "更新成功", "data": news.to_dict()})

@news_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
@requires_roles('admin')
def delete_news(id):
    news = NewsPolicy.query.get(id)
    if not news:
        return jsonify({"code": 1, "msg": "未找到"}), 404
    db.session.delete(news)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})
