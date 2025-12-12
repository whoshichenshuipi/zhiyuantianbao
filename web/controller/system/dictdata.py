from web.routes import main_routes
from web.models import SysDictData
from flask import request, jsonify
from web import db
from flask_login import login_required
import flask_excel as excel
from web.decorator import permission


@main_routes.route('/system/dict/data/type/<dictType>', methods=['GET'])
@login_required
def sysdictdata_get_by_type(dictType):
    data_list = SysDictData.query.filter(SysDictData.dict_type == dictType)

    return jsonify({'msg': '操作成功', 'code': 200, 'data': [data.to_json() for data in data_list]})


@main_routes.route('/system/dict/data/list', methods=['GET'])
@login_required
@permission('system:dict:list')
def sysdict_data_list():
    filters = []
    if 'dictLabel' in request.args:
        filters.append(SysDictData.dict_label.like('%' + request.args['dictLabel'] + '%'))
    if 'dictType' in request.args:
        filters.append(SysDictData.dict_type.like('%' + request.args['dictType'] + '%'))

    if 'status' in request.args:
        filters.append(SysDictData.status == request.args['status'])

    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysDictData.query.filter(*filters).paginate(
        page=page, per_page=rows, error_out=False)
    data_list = pagination.items

    return jsonify({'msg': '操作成功', 'code': 200, 'rows': [data.to_json() for data in data_list], 'total': pagination.total})


@main_routes.route('/system/dict/data/<id>', methods=['GET'])
@login_required
@permission('system:dict:query')
def sysdict_data_get_by_id(id):
    data = SysDictData.query.get(id)

    return jsonify({'msg': '操作成功', 'code': 200, 'data': data.to_json()})


@main_routes.route('/system/dict/data', methods=['POST'])
@login_required
@permission('system:dict:add')
def sysdict_data_add():
    dictData = SysDictData()

    if 'dictLabel' in request.json: dictData.dict_label = request.json['dictLabel']
    if 'dictSort' in request.json: dictData.dict_sort = request.json['dictSort']
    if 'dictType' in request.json: dictData.dict_type = request.json['dictType']
    if 'dictValue' in request.json: dictData.dict_value = request.json['dictValue']
    if 'listClass' in request.json: dictData.list_class = request.json['listClass']
    if 'status' in request.json: dictData.status = request.json['status']
    if 'remark' in request.json: dictData.remark = request.json['remark']
    if 'isDefault' in request.json: dictData.is_default = request.json['isDefault']
    if 'cssClass' in request.json: dictData.css_class = request.json['cssClass']

    db.session.add(dictData)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dict/data', methods=['PUT'])
@login_required
@permission('system:dict:edit')
def sysdict_data_update():
    dictData = SysDictData.query.get(request.json['dictCode'])

    if 'dictLabel' in request.json: dictData.dict_label = request.json['dictLabel']
    if 'dictSort' in request.json: dictData.dict_sort = request.json['dictSort']
    if 'dictType' in request.json: dictData.dict_type = request.json['dictType']
    if 'dictValue' in request.json: dictData.dict_value = request.json['dictValue']
    if 'listClass' in request.json: dictData.list_class = request.json['listClass']
    if 'status' in request.json: dictData.status = request.json['status']
    if 'remark' in request.json: dictData.remark = request.json['remark']
    if 'isDefault' in request.json: dictData.is_default = request.json['isDefault']
    if 'cssClass' in request.json: dictData.css_class = request.json['cssClass']

    db.session.add(dictData)

    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/system/dict/data/<string:ids>', methods=['DELETE'])
@login_required
@permission('system:dict:remove')
def sydata_delete(ids):
    idList = ids.split(',')
    for id in idList:
        dictData = SysDictData.query.get(id)
        if dictData:
            db.session.delete(dictData)

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/system/dict/data/export', methods=['POST'])
@login_required
@permission('system:dict:export')
def sydata_export():
    rows = []
    rows.append(['字典编号', '字典名称', '字典类型', '状态', '备注', '创建时间'])
    types = SysDictData.query.filter(SysDictData.dict_type == request.values.get('dictType'))
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
