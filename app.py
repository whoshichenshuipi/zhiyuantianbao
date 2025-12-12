import os

from web import create_app, db, scheduler
from flask import request, render_template, current_app
from web.models.common.BaseModel import BaseModel
from web.models import SysJob
from web.controller.system.job import add_job
from web.utils import tool
import inspect


app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
with app.app_context():
    db.create_all()


@db.event.listens_for(BaseModel, 'before_update', propagate=True)
def execute_before_update(mapper, connection, target):
    with app.test_request_context():
        current_app.preprocess_request()
        target.before_update(mapper, connection, target)


@db.event.listens_for(BaseModel, 'before_insert', propagate=True)
def execute_before_insert(mapper, connection, target):
    with app.test_request_context():
        current_app.preprocess_request()
        target.before_insert(mapper, connection, target)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.before_request
def before():
    url = request.path
    token = request.headers.get('Authorization')
    if token:
        source_code = inspect.getsource(app.view_functions[request.endpoint])
        if '@login_required' in source_code and url not in ['/logout']:
            try:
                token = token.split(' ')[1]  # 去除 "Bearer " 前缀
                data = tool.verify_token(token, app.config['SECRET_KEY'], expiration=7200)
                if data is None:
                    return {'msg': f'请求访问：{url}，认证失败，无法访问系统资源', 'code': 401}
            except:
                return {'msg': f'请求访问：{url}，认证失败，无法访问系统资源', 'code': 401}
    if os.getenv('demonstrate') and url not in ['/login', '/logout'] and request.method in ['POST', 'PUT', 'DELETE']:
        return {'msg': '演示模式，不允许操作', 'code': 500}


def load_jobs():
    with app.app_context():
        jobs = SysJob.query.filter_by(status='0').all()
        for job in jobs:
            add_job(job.to_json())


load_jobs()
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)