from web.routes import main_routes
from web.models import SysLogininfor
from flask import request, jsonify
from sqlalchemy import asc, desc
import flask_excel as excel
from flask_login import login_required
from web.decorator import permission


@main_routes.route('/monitor/logininfor/list', methods=['GET'])
@login_required
@permission('monitor:logininfor:list')
def grid_online():
    filters = []
    if request.args.get('userName'):
        filters.append(SysLogininfor.user_name.like('%' + request.args.get('userName') + '%'))
    if request.args.get('ipaddr'):
        filters.append(SysLogininfor.ipaddr.like('%' + request.args.get('ipaddr') + '%'))
    if request.args.get('status'):
        filters.append(SysLogininfor.status == request.args.get('status'))
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysLogininfor.login_time >  request.args['params[beginTime]'])
        filters.append(SysLogininfor.login_time <  request.args['params[endTime]'])

    order_by = []
    if request.form.get('sort'):
        if request.form.get('order') == 'asc':
            order_by.append(asc(getattr(SysLogininfor,request.form.get('sort').upper())))
        elif request.form.get('order') == 'desc':
            order_by.append(desc(getattr(SysLogininfor,request.form.get('sort').upper())))
        else:
            order_by.append(getattr(SysLogininfor,request.form.get('sort').upper()))

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysLogininfor.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    sysLogininfors = pagination.items

    return jsonify({'total': pagination.total, 'rows': [sysLogininfor.to_json() for sysLogininfor in sysLogininfors], 'code': 200})


@main_routes.route('/monitor/logininfor/export', methods=['POST'])
@login_required
@permission('monitor:logininfor:export')
def online_export():
    rows = []
    rows.append(['登录名', 'IP地址', '创建时间', '描述'])
    sysLogininfors = SysLogininfor.query.all()
    for sysLogininfor in sysLogininfors:
        row = []
        row.append(sysLogininfor.user_name)
        row.append(sysLogininfor.ipaddr)
        row.append(sysLogininfor.login_time)
        row.append(sysLogininfor.msg)
        rows.append(row)
    return excel.make_response_from_array(rows, "xlsx",file_name="logininfor")


@main_routes.route('/monitor/logininfor/clean', methods=['DELETE'])
@login_required
@permission('monitor:logininfor:clean')
def logininfor_clean():
    return jsonify({'code': 500, 'msg': '不支持清空'})


@main_routes.route('/monitor/logininfor/<string:ids>', methods=['DELETE'])
@login_required
@permission('monitor:logininfor:remove')
def logininfor_delete(ids):
    idList = ids.split(',')
    # for id in idList:
    #     sysLogininfor = SysLogininfor.query.get(id)
    #     if sysLogininfor:
    #         db.session.delete(sysLogininfor)
    return jsonify({'code': 500, 'msg': '不支持删除'})


@main_routes.route('/monitor/logininfor/unlock/<string:ids>', methods=['GET'])
@login_required
@permission('monitor:logininfor:unlock')
def logininfor_unlock(ids):
    idList = ids.split(',')
    # for id in idList:
    #     sysLogininfor = SysLogininfor.query.get(id)
    #     if sysLogininfor:
    #         db.session.delete(sysLogininfor)
    return jsonify({'code': 500, 'msg': '暂时不需要解锁'})