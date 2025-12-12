from web.routes import main_routes
from web.models import SysPost
from flask import request, jsonify
from web import db
from flask_login import login_required
import flask_excel as excel
from web.decorator import permission


@main_routes.route('/system/post/list', methods=['GET'])
@login_required
@permission('system:post:list')
def sys_post_list():
    filters = []
    if 'postName' in request.args:
        filters.append(SysPost.post_name.like('%' + request.args['postName'] + '%'))
    if 'postCode' in request.args:
        filters.append(SysPost.post_code == request.args['postCode'])
    if 'status' in request.args:
        filters.append(SysPost.status == request.args['status'])

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysPost.query.filter(*filters).paginate(page=page, per_page=rows, error_out=False)
    post_list = pagination.items

    return jsonify({'msg': '操作成功', 'code': 200, 'rows': [post.to_json() for post in post_list], 'total': pagination.total})


@main_routes.route('/system/post/<id>', methods=['GET'])
@login_required
@permission('system:post:query')
def sys_post_get_by_id(id):
    post = SysPost.query.get(id)

    return jsonify({'msg': '操作成功', 'code': 200, 'data': post.to_json()})


@main_routes.route('/system/post', methods=['POST'])
@login_required
@permission('system:post:add')
def sys_post_add():
    post = SysPost()
    if 'postCode' in request.json: post.post_code = request.json['postCode']
    if 'postName' in request.json: post.post_name = request.json['postName']
    if 'postSort' in request.json: post.post_sort = request.json['postSort']
    if 'remark' in request.json: post.remark = request.json['remark']
    if 'status' in request.json: post.status = request.json['status']

    db.session.add(post)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/post', methods=['PUT'])
@login_required
@permission('system:post:edit')
def sys_post_update():
    post = SysPost.query.get(request.json['postId'])

    if 'postCode' in request.json: post.post_code = request.json['postCode']
    if 'postName' in request.json: post.post_name = request.json['postName']
    if 'postSort' in request.json: post.post_sort = request.json['postSort']
    if 'status' in request.json: post.status = request.json['status']
    if 'remark' in request.json: post.remark = request.json['remark']

    db.session.add(post)

    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/system/post/<string:ids>', methods=['DELETE'])
@login_required
@permission('system:post:remove')
def sys_post_delete(ids):
    idList = ids.split(',')
    for id in idList:
        post = SysPost.query.get(id)
        if post:
            db.session.delete(post)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/post/export', methods=['POST'])
@login_required
@permission('system:post:export')
def post_export():
    rows = []
    rows.append(['岗位ID', '岗位编码', '岗位名称', '显示顺序', '状态', '备注', '创建时间'])
    posts = SysPost.query.all()
    for post in posts:
        row = []
        row.append(post.post_id)
        row.append(post.post_code)
        row.append(post.post_name)
        row.append(post.post_sort)
        if post.status == '0':
            row.append('正常')
        elif post.status == '1':
            row.append('停用')
        row.append(post.remark)
        row.append(post.create_time)

        rows.append(row)

    return excel.make_response_from_array(rows, "xlsx",
                                          file_name="post")
