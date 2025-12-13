"""
批量导入导出服务
支持Excel/CSV格式的数据导入导出
"""
import csv
import io
from flask import make_response
from web import db


def import_from_csv(file_content, model_class, field_mapping):
    """
    从CSV导入数据
    
    Args:
        file_content: CSV文件内容
        model_class: 目标模型类
        field_mapping: 字段映射 {csv列名: 模型字段名}
        
    Returns:
        dict: 导入结果 {success: int, failed: int, errors: list}
    """
    result = {'success': 0, 'failed': 0, 'errors': []}
    
    try:
        # 解析CSV
        reader = csv.DictReader(io.StringIO(file_content))
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # 构建模型实例
                data = {}
                for csv_col, model_field in field_mapping.items():
                    if csv_col in row:
                        data[model_field] = row[csv_col]
                
                instance = model_class(**data)
                db.session.add(instance)
                result['success'] += 1
                
            except Exception as e:
                result['failed'] += 1
                result['errors'].append(f'第{row_num}行: {str(e)}')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        result['errors'].append(f'文件解析错误: {str(e)}')
    
    return result


def export_to_csv(model_class, field_list, filename='export.csv'):
    """
    导出数据为CSV
    
    Args:
        model_class: 数据模型类
        field_list: 要导出的字段列表
        filename: 文件名
        
    Returns:
        Response: Flask响应对象
    """
    # 查询所有数据
    records = model_class.query.all()
    
    # 生成CSV内容
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(field_list)
    
    # 写入数据
    for record in records:
        row = [getattr(record, field, '') for field in field_list]
        writer.writerow(row)
    
    # 创建响应
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response


def import_admission_data(file_content):
    """
    导入历年录取数据（专用方法）
    
    Args:
        file_content: CSV文件内容
        
    Returns:
        dict: 导入结果
    """
    from web.models.admission_data import AdmissionData
    
    field_mapping = {
        '院校ID': 'college_id',
        '专业ID': 'major_id',
        '年份': 'year',
        '省份': 'province',
        '分数线': 'score_line',
        '位次': 'rank'
    }
    
    return import_from_csv(file_content, AdmissionData, field_mapping)


def import_college_major(file_content):
    """
    导入院校专业数据（专用方法）
    
    Args:
        file_content: CSV文件内容
        
    Returns:
        dict: 导入结果
    """
    from web.models.college_major import CollegeMajor
    
    field_mapping = {
        '院校ID': 'college_id',
        '专业ID': 'major_id',
        '地区': 'region',
        '层次': 'level',
        '类别': 'category',
        '课程设置': 'course_setting'
    }
    
    return import_from_csv(file_content, CollegeMajor, field_mapping)
