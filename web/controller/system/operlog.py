from web.routes import main_routes
from web.models import SysOperLog
from flask import request, jsonify
from sqlalchemy import asc, desc
import flask_excel as excel
from flask_login import login_required
from web.decorator import permission


@main_routes.route('/monitor/operlog/list', methods=['GET'])
@login_required
@permission('monitor:operlog:list')
def grid_operlog():
    filters = []
    if request.args.get('operName'):
        filters.append(SysOperLog.oper_name.like('%' + request.args.get('operName') + '%'))
    if request.args.get('title'):
        filters.append(SysOperLog.ipaddr.like('%' + request.args.get('title') + '%'))
    if request.args.get('operIp'):
        filters.append(SysOperLog.oper_ip.like('%' + request.args.get('operIp') + '%'))
    if request.args.get('status'):
        filters.append(SysOperLog.status == request.args.get('status'))
    if request.args.get('businessType'):
        filters.append(SysOperLog.business_type == request.args.get('businessType'))

    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysOperLog.oper_time >  request.args['params[beginTime]'])
        filters.append(SysOperLog.oper_time <  request.args['params[endTime]'])

    order_by = []
    if request.form.get('sort'):
        if request.form.get('order') == 'asc':
            order_by.append(asc(getattr(SysOperLog,request.form.get('sort').upper())))
        elif request.form.get('order') == 'desc':
            order_by.append(desc(getattr(SysOperLog,request.form.get('sort').upper())))
        else:
            order_by.append(getattr(SysOperLog,request.form.get('sort').upper()))

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysOperLog.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    sysOperLogs = pagination.items

    return jsonify({'total': pagination.total, 'rows': [sysOperLog.to_json() for sysOperLog in sysOperLogs], 'code': 200})


@main_routes.route('/monitor/operlog/export', methods=['POST'])
@login_required
@permission('monitor:operlog:export')
def operlog_export():
    rows = []
    rows.append(['标题', '方法名称', '请求方式', '请求参数'])
    sysOperLogs = SysOperLog.query.all()
    for sysOperLog in sysOperLogs:
        row = []
        row.append(sysOperLog.title)
        row.append(sysOperLog.method)
        row.append(sysOperLog.request_method)
        row.append(sysOperLog.oper_param)
        rows.append(row)
    return excel.make_response_from_array(rows, "xlsx",file_name="sysOperLog")


@main_routes.route('/monitor/operlog/clean', methods=['DELETE'])
@login_required
@permission('monitor:operlog:clean')
def operlog_clean():
    return jsonify({'code': 500, 'msg': '不支持清空'})


@main_routes.route('/monitor/operlog/<string:ids>', methods=['DELETE'])
@login_required
@permission('monitor:operlog:remove')
def operlog_delete(ids):
    idList = ids.split(',')
    # for id in idList:
    #     sysOperLog = SysOperLog.query.get(id)
    #     if sysOperLog:
    #         db.session.delete(sysOperLog)

    return jsonify({'code': 500, 'msg': '不支持删除'})