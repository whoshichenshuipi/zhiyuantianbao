# coding:utf-8
from web import db
from flask_login import UserMixin
from ..common.BaseModel import BaseModel


#角色和菜单关联表  角色1-N菜单
sys_role_menu_table = db.Table('sys_role_menu', db.metadata,
                               db.Column('role_id', db.BigInteger, db.ForeignKey('sys_role.role_id'), comment='角色ID'),
                               db.Column('menu_id', db.BigInteger, db.ForeignKey('sys_menu.menu_id')), comment='菜单ID')


#角色和部门关联表  角色1-N部门
sys_role_dept_table = db.Table('sys_role_dept', db.metadata,
                               db.Column('role_id', db.BigInteger, db.ForeignKey('sys_role.role_id'), comment='角色ID'),
                               db.Column('dept_id', db.BigInteger, db.ForeignKey('sys_dept.dept_id')), comment='部门ID')


class SysRole(BaseModel, UserMixin):
    __tablename__ = 'sys_role'
    __table_args__ = ({'comment': '角色信息表'})
    role_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='角色ID')
    role_name = db.Column(db.String(30), comment='角色名称')
    role_key = db.Column(db.String(100), comment='角色权限字符串')
    role_sort = db.Column(db.Integer, comment='显示顺序')
    data_scope = db.Column(db.CHAR(1), comment='数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）')
    menu_check_strictly = db.Column(db.Integer, nullable=False, default=1, comment='菜单树选择项是否关联显示')
    dept_check_strictly = db.Column(db.Integer, nullable=False, default=1, comment='部门树选择项是否关联显示')
    status = db.Column(db.CHAR(1), comment='角色状态（0正常 1停用）')
    del_flag = db.Column(db.CHAR(1), default=0, comment='删除标志（0代表存在 2代表删除）')

    #包含资源
    resources = db.relationship('SysMenu',
                                secondary=sys_role_menu_table,
                                backref=db.backref('roles', lazy='dynamic')) #资源所属角色
    #包含部门
    depts = db.relationship('SysDept',
                                secondary=sys_role_dept_table,
                                backref=db.backref('roles', lazy='dynamic')) #部门所属角色