from web import db
from ..common.BaseModel import ModelMixin


class SysLogininfor(ModelMixin):
    __tablename__ = 'sys_logininfor'
    __table_args__ = ({'comment': '系统访问记录'})
    info_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='访问ID')
    user_name = db.Column(db.String(50), comment='用户账号')
    ipaddr = db.Column(db.String(128), comment='登录IP地址')
    login_location = db.Column(db.String(255), comment='登录地点')
    browser = db.Column(db.String(50), comment='浏览器类型')
    os = db.Column(db.String(50), comment='操作系统')
    status = db.Column(db.CHAR(1), comment='登录状态（0成功 1失败）')
    msg = db.Column(db.String(255), comment='提示消息')
    login_time = db.Column(db.String(100), comment='访问时间')
