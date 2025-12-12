from web import db
from ..common.BaseModel import BaseModel


class SysDictData(BaseModel):
    __tablename__ = 'sys_dict_data'
    __table_args__ = ({'comment': '字典数据表'})
    dict_code = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='字典编码')
    dict_sort = db.Column(db.Integer, comment='字典排序')
    dict_label = db.Column(db.String(100), comment='字典标签')
    dict_value = db.Column(db.String(100), comment='字典键值')
    dict_type = db.Column(db.String(100), db.ForeignKey('sys_dict_type.dict_type', name='sys_dict_data_type_ibfk_2'), comment='字典类型')
    css_class = db.Column(db.String(100), comment='样式属性（其他样式扩展）')
    list_class = db.Column(db.String(100), comment='表格回显样式')
    is_default = db.Column(db.CHAR(1), comment='是否默认（Y是 N否）')
    status = db.Column(db.CHAR(1), comment='状态（0正常 1停用）')