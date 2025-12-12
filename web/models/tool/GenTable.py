from web import db
from ..common.BaseModel import BaseModel


class GenTable(BaseModel):
    __tablename__ = 'gen_table'
    __table_args__ = ({'comment': '代码生成业务表'})
    table_id = db.Column(db.BigInteger, nullable=False, autoincrement=True, primary_key=True, comment='编号')
    table_name = db.Column(db.String(200), default='', comment='表名称')
    table_comment = db.Column(db.String(500), default='', comment='表描述')
    sub_table_name = db.Column(db.String(64), default=None, comment='关联子表的表名')
    sub_table_fk_name = db.Column(db.String(64), default=None, comment='子表关联的外键名')
    class_name = db.Column(db.String(100), default='', comment='实体类名称')
    tpl_category = db.Column(db.String(200), default='crud', comment='使用的模板（crud单表操作 tree树表操作）')
    tpl_web_type = db.Column(db.String(30), default='', comment='前端模板类型（element-ui模版 element-plus模版）')
    package_name = db.Column(db.String(100), comment='生成包路径')
    module_name = db.Column(db.String(30), comment='生成模块名')
    business_name = db.Column(db.String(30), comment='生成业务名')
    function_name = db.Column(db.String(50), comment='生成功能名')
    function_author = db.Column(db.String(50), comment='生成功能作者')
    gen_type = db.Column(db.CHAR(1), default='0', comment='生成代码方式（0zip压缩包 1自定义路径）')
    gen_path = db.Column(db.String(200), default='/', comment='生成路径（不填默认项目路径）')
    options = db.Column(db.String(1000), comment='其它生成选项')

    columns = db.relationship('GenTableColumn', backref='gen_table', lazy='dynamic')

    pk_column = None
    sub_table = None
