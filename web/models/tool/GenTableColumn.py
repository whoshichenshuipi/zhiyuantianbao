from web import db
from ..common.BaseModel import ModelMixin
from datetime import datetime


class GenTableColumn(ModelMixin):
    __tablename__ = 'gen_table_column'
    __table_args__ = ({'comment': '代码生成业务表字段'})
    column_id = db.Column(db.BigInteger, nullable=False, autoincrement=True, primary_key=True, comment='编号')
    table_id = db.Column(db.BigInteger, db.ForeignKey('gen_table.table_id'), comment='归属表编号')
    column_name = db.Column(db.String(200), comment='列名称')
    column_comment = db.Column(db.String(500), comment='列描述')
    column_type = db.Column(db.String(100), comment='列类型')
    java_type = db.Column(db.String(500), comment='JAVA类型')
    java_field = db.Column(db.String(200), comment='JAVA字段名')
    is_pk = db.Column(db.CHAR(1), comment='是否主键（1是）')
    is_increment = db.Column(db.CHAR(1), comment='是否自增（1是）')
    is_required = db.Column(db.CHAR(1), comment='是否必填（1是）')
    is_insert = db.Column(db.CHAR(1), comment='是否为插入字段（1是）')
    is_edit = db.Column(db.CHAR(1), comment='是否编辑字段（1是）')
    is_list = db.Column(db.CHAR(1), comment='是否列表字段（1是）')
    is_query = db.Column(db.CHAR(1), comment='是否查询字段（1是）')
    query_type = db.Column(db.String(200), default='EQ', comment='查询方式（等于、不等于、大于、小于、范围）')
    html_type = db.Column(db.String(200), comment='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')
    dict_type = db.Column(db.String(200), default='', comment='字典类型')
    sort = db.Column(db.Integer, comment='排序')
    create_by = db.Column(db.String(64), default='', comment='创建者')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_by = db.Column(db.String(64), default='', comment='更新者')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')