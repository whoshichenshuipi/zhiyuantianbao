from web import db
from ..common.BaseModel import BaseModel


class SysJob(BaseModel):
    __tablename__ = 'sys_job'
    __table_args__ = ({'comment': '定时任务调度表'})
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='任务ID')
    job_name = db.Column(db.String(64), default='', comment='任务名称')
    job_group = db.Column(db.String(64), default='DEFAULT', comment='任务组名')
    invoke_target = db.Column(db.String(500), nullable=False, comment='调用目标字符串')
    cron_expression = db.Column(db.String(255), default='', comment='cron执行表达式')
    misfire_policy = db.Column(db.String(20), default='3', comment='计划执行错误策略（1立即执行 2执行一次 3放弃执行）')
    concurrent = db.Column(db.CHAR(1), default='1', comment='是否并发执行（0允许 1禁止）')
    status = db.Column(db.CHAR(1), default='0', comment='状态（0正常 1暂停）')