from web import db
from ..common.BaseModel import ModelMixin
from datetime import datetime


class SysJobLog(ModelMixin):
    __tablename__ = 'sys_job_log'
    __table_args__ = ({'comment': '定时任务调度日志表'})
    job_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='任务日志ID')
    job_name = db.Column(db.String(64), comment='任务名称')
    job_group = db.Column(db.String(64), comment='任务组名')
    invoke_target = db.Column(db.String(500), comment='调用目标字符串')
    job_message = db.Column(db.String(500), comment='日志信息')
    status = db.Column(db.CHAR(1), default='0', comment='状态（0正常 1暂停）')
    exception_info = db.Column(db.String(2000), default='', comment='异常信息')
    create_time = db.Column(db.DATETIME, default=datetime.now, comment='创建时间')
