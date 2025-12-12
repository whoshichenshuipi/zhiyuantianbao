from web import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from ..common.BaseModel import BaseModel


@login_manager.user_loader
def load_user(user_id):
    return SysUser.query.filter(SysUser.user_id == user_id).first()

#用户和角色关联表  用户N-1角色
sys_user_role_table = db.Table('sys_user_role', db.Model.metadata
                           , db.Column('user_id', db.BigInteger, db.ForeignKey('sys_user.user_id'), comment='用户ID')
                           , db.Column('role_id', db.BigInteger, db.ForeignKey('sys_role.role_id')), comment='角色ID')

#用户与岗位关联表  用户1-N岗位
sys_user_post_table = db.Table('sys_user_post', db.Model.metadata
                           , db.Column('user_id',db.BigInteger, db.ForeignKey('sys_user.user_id'), comment='用户ID')
                           , db.Column('post_id',db.BigInteger, db.ForeignKey('sys_post.post_id')), comment='岗位ID')

class SysUser(BaseModel, UserMixin):
    __tablename__ = 'sys_user'
    __table_args__ = ({'comment': '用户信息表'})
    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    dept_id = db.Column(db.BigInteger, db.ForeignKey('sys_dept.dept_id'), comment='部门ID')
    user_name = db.Column(db.String(30), unique=True, index=True, comment='用户账号')
    nick_name = db.Column(db.String(30), comment='用户昵称')
    user_type = db.Column(db.String(2), default='00', comment='用户类型（00系统用户）')
    email = db.Column(db.String(50), default='', comment='用户邮箱')
    phonenumber = db.Column(db.String(11), default='', comment='手机号码')
    sex = db.Column(db.CHAR(1), default='0', comment='用户性别（0男 1女 2未知）')
    avatar = db.Column(db.String(100), comment='头像地址')
    password = db.Column(db.String(100), default='', comment='密码')
    status = db.Column(db.CHAR(1), default='0', comment='帐号状态（0正常 1停用）')
    del_flag = db.Column(db.CHAR(1), default='0', comment='删除标志（0代表存在 2代表删除）')
    login_ip = db.Column(db.String(128), default='', comment='最后登录IP')
    login_date = db.Column(db.DATETIME, default=datetime.now, comment='最后登录时间')

    dept = db.relationship('SysDept', backref=db.backref('users', lazy='dynamic'))

    roles = db.relationship('SysRole',
                            secondary=sys_user_role_table,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    posts = db.relationship('SysPost',
                            secondary=sys_user_post_table,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')