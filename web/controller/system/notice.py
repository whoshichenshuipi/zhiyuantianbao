from web.routes import main_routes
from web.models import SysNotice
from flask import request, jsonify
from web import db
from flask_login import login_required
from web.decorator import permission


@main_routes.route('/system/notice/list', methods=['GET'])
@login_required
@permission('system:notice:list')
def sys_notice_list():
    filters = []
    if 'noticeTitle' in request.args:
        filters.append(SysNotice.notice_title.like('%' + request.args['noticeTitle'] + '%'))
    if 'createBy' in request.args:
        filters.append(SysNotice.create_by.like('%' + request.args['createBy'] + '%'))
    if 'noticeType' in request.args:
        filters.append(SysNotice.notice_type == request.args['noticeType'])
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysNotice.create_time >  request.args['params[beginTime]'])
        filters.append(SysNotice.create_time <  request.args['params[endTime]'])

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysNotice.query.filter(*filters).paginate(page=page, per_page=rows, error_out=False)
    notice_list = pagination.items

    return jsonify({'msg': '操作成功', 'code': 200, 'rows': [notice.to_json() for notice in notice_list], 'total': pagination.total})


@main_routes.route('/system/notice/<id>', methods=['GET'])
@login_required
@permission('system:notice:query')
def sys_notice_get_by_id(id):
    notice = SysNotice.query.get(id)

    return jsonify({'msg': '操作成功', 'code': 200, 'data': notice.to_json()})


@main_routes.route('/system/notice', methods=['POST'])
@login_required
@permission('system:notice:add')
def sys_notice_add():
    notice = SysNotice()

    if 'noticeTitle' in request.json: notice.notice_title = request.json['noticeTitle']
    if 'noticeType' in request.json: notice.notice_type = request.json['noticeType']
    if 'noticeContent' in request.json: notice.notice_content = request.json['noticeContent'].encode('utf-8')
    if 'status' in request.json: notice.status = request.json['status']
    if 'remark' in request.json: notice.remark = request.json['remark']

    db.session.add(notice)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/notice', methods=['PUT'])
@login_required
@permission('system:notice:edit')
def sys_notice_update():
    notice = SysNotice.query.get(request.json['noticeId'])

    if 'noticeTitle' in request.json: notice.notice_title = request.json['noticeTitle']
    if 'noticeType' in request.json: notice.notice_type = request.json['noticeType']
    if 'noticeContent' in request.json: notice.notice_content = request.json['noticeContent'].encode('utf-8')
    if 'status' in request.json: notice.status = request.json['status']
    if 'remark' in request.json: notice.remark = request.json['remark']

    db.session.add(notice)

    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/system/notice/<string:ids>', methods=['DELETE'])
@login_required
@permission('system:notice:remove')
def sys_notice_remove(ids):
    id_list = ids.split(',')
    for id in id_list:
        #todo refreshCache
        notice = SysNotice.query.get(id)
        if notice:
            db.session.delete(notice)

    return jsonify({'code': 200, 'msg': '操作成功'})

