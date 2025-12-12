from web import db
from flask_login import UserMixin
from datetime import datetime
from ..common.BaseModel import ModelMixin


class SysDept(ModelMixin, UserMixin):
    __tablename__ = 'sys_dept'
    __table_args__ = ({'comment': '部门表'})
    dept_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='部门id')
    parent_id = db.Column(db.BigInteger, db.ForeignKey('sys_dept.dept_id'),default=0, comment='父部门id')
    ancestors = db.Column(db.String(50), comment='祖级列表')
    dept_name = db.Column(db.String(30), comment='部门名称')
    order_num = db.Column(db.Integer, comment='显示顺序')
    leader = db.Column(db.String(20), comment='负责人')
    phone = db.Column(db.String(11), comment='联系电话')
    email = db.Column(db.String(50), comment='邮箱')
    status = db.Column(db.CHAR(1),default=0, comment='部门状态（0正常 1停用）')
    del_flag = db.Column(db.CHAR(1),default=0, comment='删除标志（0代表存在 2代表删除）')
    create_by = db.Column(db.String(64), comment='创建者')
    create_time = db.Column(db.DATETIME, default=datetime.now, comment='创建时间')
    update_by = db.Column(db.String(64), comment='更新者')
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    parent = db.relationship('SysDept', remote_side=[dept_id], backref='sys_dept', uselist=False)

    children = db.relationship('SysDept')

    def to_tree_select_json(self):
        return {
            'id': self.dept_id,
            'label': self.dept_name,
            'children': [org.to_tree_select_json() for org in self.children]
        }