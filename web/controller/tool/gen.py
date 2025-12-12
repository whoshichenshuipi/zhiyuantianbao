from web.routes import main_routes
from web.models import GenTable, GenTableColumn
from flask import request, jsonify, render_template, send_file
from flask_login import login_required, current_user
from web.decorator import permission
from sqlalchemy import text
from web import db
from web.utils.tool import convert_to_camel_case, convert_to_camel_case_upper
import json
from collections import defaultdict
from datetime import datetime
import zipfile
import os
import time

@main_routes.route('/tool/gen/list', methods=['GET'])
@login_required
@permission('tool:gen:list')
def tool_gen():
    filters = []
    if request.args.get('tableName'):
        filters.append(GenTable.table_name.like('%' + request.args.get('tableName') + '%'))
    if request.args.get('tableComment'):
        filters.append(GenTable.table_comment.like('%' + request.args.get('tableComment') + '%'))
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(GenTable.create_time >  request.args['params[beginTime]'])
        filters.append(GenTable.create_time <  request.args['params[endTime]'])
    order_by = []
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = GenTable.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    genTables = pagination.items
    return jsonify({'total': pagination.total, 'rows': [genTable.to_json() for genTable in genTables], 'code': 200})


@main_routes.route('/tool/gen/db/list', methods=['GET'])
@login_required
@permission('tool:gen:db')
def tool_gen_db():
    filters = []
    base_query = """
        update_time FROM information_schema.tables
        WHERE table_schema = (SELECT database())
        AND table_name NOT LIKE 'qrtz\_%' AND table_name NOT LIKE 'gen\_%'
        AND table_name NOT IN (SELECT table_name FROM gen_table)
    """
    if request.args.get('tableName'):
        filters.append(f"AND lower(table_name) like lower(concat('%', '{request.args.get('tableName')}', '%'))")
    if request.args.get('tableComment'):
        filters.append(f"AND lower(table_comment) like lower(concat('%', '{request.args.get('tableComment')}', '%'))")
    if filters:
        query = base_query + ' ' + ' '.join(filters) + ' ORDER BY create_time DESC'
    else:
        query = base_query + ' ORDER BY create_time DESC'
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = db.session.query(text("table_name"), text("table_comment"), text("create_time"), text(query)).paginate(page=page, per_page=rows, error_out=False)
    tables = pagination.items
    rows =[]
    for table in tables:
        genTable = GenTable()
        genTable.table_name = table[0]
        genTable.table_comment = table[1]
        genTable.create_time = table[2]
        genTable.update_time = table[3]
        rows.append(genTable)
    return jsonify({'total': pagination.total, 'rows': [row.to_json() for row in rows], 'code': 200})


def init_table(genTable):
    genTable.class_name = convert_to_camel_case_upper(genTable.table_name)
    genTable.package_name = "web.controller.system"
    genTable.module_name = "system"
    genTable.business_name = genTable.table_name.split("_")[-1] if len(genTable.table_name.split("_")) > 1 else genTable.table_name
    genTable.function_name = genTable.table_comment.replace("表", "").replace("若依", "")
    genTable.function_author = 'djsoft'


def initColumnField(column, gen_table_column, genTable):
    data_type = column[6].decode('utf-8').split('(')[0] if '(' in column[6].decode('utf-8') else column[6].decode('utf-8')
    column_name = column[0]
    gen_table_column.column_name = column_name
    gen_table_column.table_id = genTable.table_id
    gen_table_column.is_required = column[1]
    gen_table_column.is_pk = column[2]
    gen_table_column.sort = column[3]
    gen_table_column.column_comment = column[4].decode('utf-8')
    gen_table_column.is_increment = column[5]
    gen_table_column.column_type = column[6].decode('utf-8')

    # 设置java字段名
    gen_table_column.java_field = convert_to_camel_case(column_name)
    # 设置默认类型
    gen_table_column.java_type = 'String'
    gen_table_column.query_type = 'EQ'
    column_type_str = {"char", "varchar", "nvarchar", "varchar2"}
    column_type_text = {"tinytext", "text", "mediumtext", "longtext"}
    column_type_time = {"datetime", "time", "date", "timestamp" }
    column_type_number = {"tinyint", "smallint", "mediumint", "int", "number", "integer", "bit", "bigint", "float", "double", "decimal"}
    column_name_not_edit = {"id", "create_by", "create_time", "del_flag"}
    column_name_not_list = {"id", "create_by", "create_time", "del_flag", "update_by", "update_time"}
    column_name_not_query = {"id", "create_by", "create_time", "del_flag", "update_by", "update_time", "remark"}
    if data_type in column_type_str or data_type in column_type_text:
        # 字符串长度超过500设置为文本域 varchar(500)
        column_length = int(column[6].decode('utf-8').split('(')[1].split(')')[0]) if '(' in column[6].decode('utf-8') else 0
        html_type ='textarea' if column_length >= 500 or data_type in column_type_text else 'input'
        gen_table_column.html_type = html_type
    elif data_type in column_type_time:
        gen_table_column.java_type = 'Date'
        gen_table_column.html_type = 'datetime'
    elif data_type in column_type_number:
        gen_table_column.html_type = 'input'
        # 如果是浮点型 统一用BigDecimal
        str = column[6].decode('utf-8').split('(')[1].split(')')[0].split(',') if '(' in column[6].decode('utf-8') else []
        if len(str) ==2 and int(str[1]) >0:
            gen_table_column.java_type = 'BigDecimal'
        # 如果是整形
        elif column[6].decode('utf-8') == 'int' or (len(str) == 1 and int(str[1]) <= 10):
            gen_table_column.java_type = 'Integer'
        # 长整形
        else:
            gen_table_column.java_type = 'Long'

    # 插入字段（默认所有字段都需要插入）
    gen_table_column.is_insert = '1'
    # 编辑字段
    if column_name not in column_name_not_edit and column[2]!='1':
        gen_table_column.is_edit = '1'
    # 列表字段
    if column_name not in column_name_not_list and column[2]!='1':
        gen_table_column.is_list = '1'
    # 查询字段
    if column_name not in column_name_not_query and column[2]!='1':
        gen_table_column.is_query = '1'
    # 查询字段类型
    if column_name.lower().endswith('name'):
        gen_table_column.query_type = 'LIKE'
    # 状态字段设置单选框
    if column_name.lower().endswith('status'):
        gen_table_column.html_type = 'radio'
    # // 类型&性别字段设置下拉框
    elif column_name.lower().endswith('type') or column_name.lower().endswith('sex'):
        gen_table_column.html_type = 'select'
    # 图片字段设置图片上传控件
    elif column_name.lower().endswith('image'):
        gen_table_column.html_type = 'imageUpload'
    # 文件字段设置文件上传控件
    elif column_name.lower().endswith('file'):
        gen_table_column.html_type = 'fileUpload'
    # 内容字段设置富文本控件
    elif column_name.lower().endswith('content'):
        gen_table_column.html_type = 'editor'


@main_routes.route('/tool/gen/importTable', methods=['POST'])
@login_required
@permission('tool:gen:import')
def tool_gen_import_table():
    tableNames = request.args.get('tables').split(",")
    table_name = "('" + "', '".join(tableNames) + "')"
    base_query = f"""
        Select table_name, table_comment, create_time, update_time FROM information_schema.tables
        WHERE table_schema = (SELECT database())
        AND table_name NOT LIKE 'qrtz\_%' AND table_name NOT LIKE 'gen\_%'
        AND table_name IN {table_name}
    """
    result = db.session.execute(text(base_query))
    tables = result.fetchall()
    for table in tables:
        genTable = GenTable()
        genTable.table_name = table[0]
        genTable.table_comment = table[1]
        init_table(genTable)
        db.session.add(genTable)
        db.session.commit()
        # table_id = genTable.table_id
        select_db_table_columns_by_name = f""" 
            select column_name, (case when (is_nullable = 'no' and column_key != 'PRI') then '1' else '0' end) as is_required, (case when column_key = 'PRI' then '1' else '0' end) as is_pk, ordinal_position as sort, column_comment, (case when extra = 'auto_increment' then '1' else '0' end) as is_increment, column_type
            from information_schema.columns where table_schema = (select database()) and table_name = '{table[0]}'
            order by ordinal_position
        """
        result_columns = db.session.execute(text(select_db_table_columns_by_name))
        table_columns = result_columns.fetchall()
        for column in table_columns:
            gen_table_column = GenTableColumn()
            gen_table_column.create_by = current_user.user_name
            initColumnField(column, gen_table_column, genTable)
            db.session.add(gen_table_column)
    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/tool/gen/<tableId>', methods=['GET'])
@login_required
@permission('tool:gen:query')
def tool_gen_getInfo(tableId):
    table_info = GenTable.query.get(tableId)
    table_columns = GenTableColumn.query.filter(GenTableColumn.table_id == tableId).all()
    gen_tables = GenTable.query.all()
    return jsonify({'code': 200, 'msg': '操作成功', 'data': {'info': table_info.to_json(), 'rows': [table_column.to_json() for table_column in table_columns], 'tables': [gen_table.to_json() for gen_table in gen_tables]}})


@main_routes.route('/tool/gen', methods=['PUT'])
@login_required
@permission('tool:gen:edit')
def tool_gen_update():
    if 'tree' == request.json['tplCategory']:
        if 'treeCode' not in request.json['params']:
            return jsonify({'msg': '树编码字段不能为空', 'code': 500})
        elif 'treeParentCode' not in request.json['params']:
            return jsonify({'msg': '树父编码字段不能为空', 'code': 500})
        elif 'treeName' not in request.json['params']:
            return jsonify({'msg': '树名称字段不能为空', 'code': 500})
    elif 'sub' == request.json['tplCategory']:
        if request.json['subTableName'] == '':
            return jsonify({'msg': '关联子表的表名不能为空', 'code': 500})
        elif request.json['subTableFkName'] == '':
            return jsonify({'msg': '子表关联的外键名不能为空', 'code': 500})
    table_info = GenTable.query.get(request.json['tableId'])
    if 'tableName' in request.json: table_info.table_name = request.json['tableName']
    if 'tableComment' in request.json: table_info.table_comment = request.json['tableComment']
    if 'className' in request.json: table_info.class_name = request.json['className']
    if 'functionAuthor' in request.json: table_info.function_author = request.json['functionAuthor']
    if 'remark' in request.json: table_info.remark = request.json['remark']

    if 'packageName' in request.json: table_info.package_name = request.json['packageName']
    if 'moduleName' in request.json: table_info.module_name = request.json['moduleName']
    if 'businessName' in request.json: table_info.business_name = request.json['businessName']
    if 'functionName' in request.json: table_info.function_name = request.json['functionName']
    if 'tplCategory' in request.json: table_info.tpl_category = request.json['tplCategory']
    if 'tplWebType' in request.json: table_info.tpl_web_type = request.json['tplWebType']
    if 'subTableName' in request.json: table_info.sub_table_name = request.json['subTableName']
    if 'subTableFkName' in request.json: table_info.sub_table_fk_name = request.json['subTableFkName']
    if 'genType' in request.json: table_info.gen_type = request.json['genType']
    if 'genPath' in request.json: table_info.gen_path = request.json['genPath']
    if 'tplCategory' in request.json: table_info.tpl_category = request.json['tplCategory']
    if 'tplCategory' in request.json: table_info.tpl_category = request.json['tplCategory']
    table_info.options = json.dumps(request.json['params'])
    for table_column in table_info.columns:
        for column in request.json['columns']:
            if column['columnId'] == table_column.column_id:
                table_column.column_comment = column['columnComment']
                table_column.java_field = column['javaField']
                table_column.java_type = column['javaType']
                table_column.dict_type = column['dictType']
                table_column.html_type = column['htmlType']
                table_column.is_insert = column['isInsert']
                table_column.is_edit = column['isEdit']
                table_column.is_list = column['isList']
                table_column.is_query = column['isQuery']
                table_column.query_type = column['queryType']
                table_column.is_required = column['isRequired']
    db.session.add(table_info)
    return jsonify({'msg': '操作成功', 'code': 200})


@main_routes.route('/tool/gen/<string:ids>', methods=['DELETE'])
@login_required
@permission('tool:gen:remove')
def tool_gen_remove(ids):
    idList = ids.split(',')
    for id in idList:
        gen_table = GenTable.query.get(id)
        for gen_table_column in gen_table.columns:
            if gen_table_column:
                db.session.delete(gen_table_column)
        if gen_table:
            db.session.delete(gen_table)
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/tool/gen/synchDb/<string:tableName>', methods=['GET'])
@login_required
@permission('tool:gen:edit')
def tool_gen_synchDb(tableName):
    genTable = GenTable.query.filter(GenTable.table_name == tableName).first()
    select_db_table_columns_by_name = f""" 
            select column_name, (case when (is_nullable = 'no' and column_key != 'PRI') then '1' else '0' end) as is_required, (case when column_key = 'PRI' then '1' else '0' end) as is_pk, ordinal_position as sort, column_comment, (case when extra = 'auto_increment' then '1' else '0' end) as is_increment, column_type
            from information_schema.columns where table_schema = (select database()) and table_name = '{tableName}'
            order by ordinal_position
        """
    result_columns = db.session.execute(text(select_db_table_columns_by_name))
    db_table_columns = result_columns.fetchall()
    if len(db_table_columns) == 0:
        return jsonify({'code': 500, 'msg': '同步数据失败，原表结构不存在'})
    tableColumnMap = defaultdict(dict)
    for gen_table_column in genTable.columns:
        tableColumnMap[gen_table_column.column_name] = gen_table_column

    db_table_column_map = []
    for db_column in db_table_columns:
        gen_table_column = GenTableColumn()
        # gen_table_column.create_by = current_user.user_name
        initColumnField(db_column, gen_table_column, genTable)
        db_table_column_map.append(gen_table_column.column_name)
        if gen_table_column.column_name in tableColumnMap:
            prev_column = tableColumnMap[gen_table_column.column_name]
            # gen_table_column.column_id = prev_column.column_id
            if gen_table_column.is_list == '1':
                # 如果是列表，继续保留查询方式/字典类型选项
                gen_table_column.dict_type = prev_column.dict_type
                gen_table_column.query_type = prev_column.query_type
            column_json = gen_table_column.to_json()
            if prev_column.is_required == '1' and gen_table_column.is_pk != '1' and (gen_table_column.is_insert == '1' or gen_table_column.is_edit == '1') and (column_json['usableColumn'] or (not column_json['superColumn'])):
                # 如果是(新增/修改&非主键/非忽略及父属性)，继续保留必填/显示类型选项
                gen_table_column.is_required = prev_column.is_required
                gen_table_column.html_type = prev_column.html_type
            prev_column.column_comment = gen_table_column.column_comment
            prev_column.java_type = gen_table_column.java_type
            prev_column.java_field = gen_table_column.java_field
            prev_column.is_insert = gen_table_column.is_insert
            prev_column.is_edit = gen_table_column.is_edit
            prev_column.is_list = gen_table_column.is_list
            prev_column.is_query = gen_table_column.is_query
            prev_column.is_required = gen_table_column.is_required
            prev_column.query_type = gen_table_column.query_type
            prev_column.html_type = gen_table_column.html_type
            prev_column.dict_type = gen_table_column.dict_type
            prev_column.sort = gen_table_column.sort
        else:
            db.session.add(gen_table_column)
    for tableColumn in tableColumnMap:
        if tableColumn not in db_table_column_map:
            db.session.delete(tableColumnMap[tableColumn])
    return jsonify({'code': 200, 'msg': '操作成功'})


def set_sub_table(gen_table):
    sub_table_name = gen_table.sub_table_name
    if not (sub_table_name is None or sub_table_name == ''):
        gen_sub_table = GenTable.query.filter(GenTable.table_name == sub_table_name).first()
        gen_table.sub_table = gen_sub_table


def set_pk_column(gen_table):
    for gen_table_column in gen_table.columns:
        if gen_table_column.is_pk == '1':
            gen_table.pk_column = gen_table_column
            break
    if gen_table.pk_column is None:
        gen_table.pk_column = gen_table.columns[0]
    if gen_table.tpl_category == 'sub':
        for gen_table_sub_column in gen_table.sub_table.columns:
            if gen_table_sub_column.is_pk == '1':
                gen_table.sub_table.pk_column = gen_table_sub_column
        if gen_table.sub_table.pk_column is None:
            gen_table.sub_table.pk_column = gen_table.sub_table.columns[0]


def get_template_list(tpl_category, tpl_web_type):
    use_web_type = 'vm/vue'
    if tpl_web_type == 'element-plus':
        use_web_type = 'vm/vue/v3'
    templates = []
    templates.append('vm/python/domain.java.vm')
    templates.append('vm/python/models.py.vm')
    templates.append('vm/python/controller.py.vm')
    templates.append('vm/sql/sql.vm')
    templates.append('vm/js/api.js.vm')
    if tpl_category == 'crud':
        templates.append(f'{use_web_type}/index.vue.vm')
    elif tpl_category == 'tree':
        templates.append(f'{use_web_type}/index-tree.vue.vm')
    elif tpl_category == 'sub':
        templates.append(f'{use_web_type}/index.vue.vm')
        templates.append('vm/java/sub-domain.java.vm')
    return templates


def add_dicts(dicts, columns):
    for column in columns:
        if not column['superColumn'] and column['dictType'] !='' and column['htmlType'] in {'select', 'radio', 'checkbox'} :
            dicts.append(f"'{column['dictType']}'")


def get_dicts(gen_table_context):
    columns = gen_table_context['columns']
    dicts = []
    add_dicts(dicts, columns)
    if 'subTable' in gen_table_context:
        sub_columns = gen_table_context['subTable']['columns']
        add_dicts(dicts, sub_columns)
    return ','.join(dicts)


def get_expand_column(gen_table_context):
    tree_name = gen_table_context['treeName']
    num = 0
    for column in gen_table_context['columns']:
        if column['list']:
            num = num + 1
            if column['columnName'] == tree_name:
                break
    return num


def prepare_context(gen_table_context):
    module_name = gen_table_context['moduleName']
    business_name = gen_table_context['businessName']
    package_name = gen_table_context['packageName']
    tpl_category = gen_table_context['tplCategory']
    function_name = gen_table_context['functionName']
    gen_table_context['functionName'] = '【请填写功能名称】' if (function_name is None or function_name == '') else function_name
    gen_table_context['ClassName'] = gen_table_context['className']
    gen_table_context['BusinessName'] = business_name.capitalize()
    gen_table_context['basePackage'] = package_name.split('.')[-1] if len(package_name.split('.')) > 1 else package_name
    gen_table_context['author'] = gen_table_context['functionAuthor']
    gen_table_context['datetime'] = datetime.now().strftime('%Y-%m-%d')
    gen_table_context['importList'] = '暂时不处理 importList'
    gen_table_context['permissionPrefix'] = f'{module_name}:{business_name}'
    gen_table_context['table'] = gen_table_context
    gen_table_context['dicts'] = get_dicts(gen_table_context)
    if tpl_category == 'tree':
        gen_table_context['expandColumn'] = get_expand_column(gen_table_context)
        if gen_table_context['treeParentCode'] is not None:
            gen_table_context['tree_parent_code'] = gen_table_context['treeParentCode']
        if gen_table_context['treeName'] is not None:
            gen_table_context['tree_name'] = gen_table_context['treeName']
    if tpl_category == 'sub':
        sub_table = gen_table_context['subTable']
        sub_table_name = gen_table_context['subTableName']
        sub_table_fk_name = gen_table_context['subTableFkName']
        sub_class_name = sub_table['className']
        sub_table_fk_class_name = convert_to_camel_case_upper(sub_table_fk_name)
        gen_table_context['subTableFkClassName'] = sub_table_fk_class_name
        gen_table_context['subTableFkclassName'] = sub_table_fk_name
        gen_table_context['subClassName'] = sub_class_name
        gen_table_context['subclassName'] = sub_class_name
        gen_table_context['subImportList'] = '暂时不处理 importList'
    return gen_table_context


@main_routes.route('/tool/gen/preview/<table_id>', methods=['GET'])
@login_required
@permission('tool:gen:preview')
def tool_gen_preview(table_id):
    data_map = defaultdict(dict)
    # 查询表信息
    gen_table = GenTable.query.get(table_id)
    # 设置主子表信息
    set_sub_table(gen_table)
    # 设置主键列信息
    set_pk_column(gen_table)
    context = prepare_context(gen_table.to_json())
    # 获取模板列表
    templates = get_template_list(gen_table.tpl_category, gen_table.tpl_web_type)
    for template in templates:
        # 渲染模板
        data_map[template] = render_template(template, **context)
    # render_template('vm/sql/sql.vm', **context)
    return jsonify({'code': 200, 'data': data_map, 'msg': '操作成功'})


@main_routes.route('/tool/gen/batchGenCode', methods=['GET'])
@login_required
@permission('tool:gen:code')
def tool_gen_batch_gen_code():
    table_names = request.args.get('tables').split(",")
    gen_tables = GenTable.query.filter(GenTable.table_name.in_(table_names)).all()
    current_timestamp = time.time()
    zip_filename = f'web/static/cache/{current_timestamp}/ruoyi.zip'
    os.makedirs(os.path.dirname(zip_filename), exist_ok=True)
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for gen_table in gen_tables:
            data_map = tool_gen_preview(gen_table.table_id)
            business_name = gen_table.business_name
            class_name = gen_table.class_name
            module_name = gen_table.module_name
            for key in data_map.json['data']:
                file_path = ''
                if key == 'vm/js/api.js.vm':
                    file_path = f'vue/api/{module_name}/{business_name}.js'
                elif key == 'vm/python/controller.py.vm':
                    file_path = f'web/controller/{module_name}/{business_name}.py'
                elif key == 'vm/python/models.py.vm':
                    file_path = f'web/models/{module_name}/{class_name}.py'
                elif key == 'vm/sql/sql.vm':
                    file_path = f'{business_name}.sql'
                elif key == 'vm/vue/index.vue.vm':
                    file_path = f'vue/views/{module_name}/{business_name}/index.vue'
                else:
                    continue
                file_path = f'web/static/cache/{current_timestamp}/{file_path}'
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(data_map.json['data'][key])
                zipf.write(file_path,os.path.relpath(file_path, f'web/static/cache/{current_timestamp}'))
                os.remove(file_path)
    response = send_file(zip_filename.replace('web/', ''), as_attachment=True)
    os.remove(zip_filename)
    # shutil.rmtree（更强大但也危险）
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/views/system/config')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/views/system/notice')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/views/system')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/views')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/api/system')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue/api')
    os.rmdir(f'web/static/cache/{current_timestamp}/vue')
    os.rmdir(f'web/static/cache/{current_timestamp}/web/controller/system')
    os.rmdir(f'web/static/cache/{current_timestamp}/web/controller')
    os.rmdir(f'web/static/cache/{current_timestamp}/web/models/system')
    os.rmdir(f'web/static/cache/{current_timestamp}/web/models')
    os.rmdir(f'web/static/cache/{current_timestamp}/web')
    os.rmdir(f'web/static/cache/{current_timestamp}')
    return response


@main_routes.route('/tool/gen/createTable/<sql>', methods=['POST'])
@login_required
@permission('admin')
def tool_gen_create_table(sql):
    return jsonify({'code': 500,  'msg': '根据models生成表结构'})