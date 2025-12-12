from datetime import datetime

from flask_login import current_user
from web.routes import main_routes
from web.models import SysDictData, SysDictType
from flask import request, jsonify
from web import db
from flask_login import login_required
import flask_excel as excel
from web.decorator import permission


@main_routes.route('/system/dict/type/list', methods=['GET'])
@login_required
@permission('system:dict:list')
def sysdict_type_list():
    filters = []
    if 'dictName' in request.args:
        filters.append(SysDictType.dict_name.like('%' + request.args['dictName'] + '%'))
    if 'dictType' in request.args:
        filters.append(SysDictType.dict_type.like('%' + request.args['dictType'] + '%'))

    if 'status' in request.args:
        filters.append(SysDictType.status == request.args['status'])


    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysDictType.create_time >  request.args['params[beginTime]'])
        filters.append(SysDictType.create_time <  request.args['params[endTime]'])

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysDictType.query.filter(*filters).paginate(
        page=page, per_page=rows, error_out=False)
    types = pagination.items

    return jsonify({'msg': '操作成功', 'code': 200, 'rows': [type.to_json() for type in types], 'total': pagination.total})


@main_routes.route('/system/dict/type/<id>', methods=['GET'])
@login_required
@permission('system:dict:query')
def sysdict_type_get_by_id(id):
    type = SysDictType.query.get(id)

    return jsonify({'msg': '操作成功', 'code': 200, 'data': type.to_json()})


@main_routes.route('/system/dict/type', methods=['POST'])
@login_required
@permission('system:dict:add')
def sysdict_type_add():
    dictType = SysDictType()

    if 'dictName' in request.json: dictType.dict_name = request.json['dictName']
    if 'status' in request.json: dictType.status = request.json['status']
    if 'remark' in request.json: dictType.remark = request.json['remark']
    if 'dictType' in request.json: dictType.dict_type = request.json['dictType']

    db.session.add(dictType)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dict/type', methods=['PUT'])
@login_required
@permission('system:dict:edit')
def sysdict_type_update():
    dictType = SysDictType.query.get(request.json['dictId'])

    if 'dictName' in request.json: dictType.dict_name = request.json['dictName']
    if 'status' in request.json: dictType.status = request.json['status']
    if 'remark' in request.json: dictType.remark = request.json['remark']
    if 'dictType' in request.json: dictType.dict_type = request.json['dictType']

    db.session.add(dictType)

    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/system/dict/type/<string:ids>', methods=['DELETE'])
@login_required
@permission('system:dict:remove')
def systype_delete(ids):
    idList = ids.split(',')
    for id in idList:
        #id == refreshCache todo清除缓存
        dictType = SysDictType.query.get(id)
        if dictType:
            db.session.delete(dictType)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dict/type/optionselect', methods=['GET'])
@login_required
def sysdict_type_all():
    types = SysDictType.query.all()

    return jsonify({'msg': '操作成功', 'code': 200, 'data': [type.to_json() for type in types]})


@main_routes.route('/system/dict/type/export', methods=['POST'])
@login_required
@permission('system:dict:export')
def systype_export():
    rows = []
    rows.append(['字典编号', '字典名称', '字典类型', '状态', '备注', '创建时间'])
    types = SysDictData.query.all()
    for type in types:
        row = []
        row.append(type.dict_code)
        row.append(type.dict_label)
        row.append(type.dict_type)
        if type.status == '0':
            row.append('正常')
        elif type.status == '1':
            row.append('停用')
        row.append(type.remark)
        row.append(type.create_time)
        rows.append(row)
    return excel.make_response_from_array(rows, "xlsx", file_name="post")
