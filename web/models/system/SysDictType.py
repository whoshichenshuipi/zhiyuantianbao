from web import db
from ..common.BaseModel import BaseModel


class SysDictType(BaseModel):
    __tablename__ = 'sys_dict_type'
    __table_args__ = ({'comment': '字典类型表'})
    dict_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='字典主键')
    dict_name = db.Column(db.String(100), comment='字典名称')
    dict_type = db.Column(db.String(100),index=True, comment='字典类型')
    status = db.Column(db.CHAR(1), comment='状态（0正常 1停用）')

    data_list = db.relationship('SysDictData', backref='type', lazy='dynamic')