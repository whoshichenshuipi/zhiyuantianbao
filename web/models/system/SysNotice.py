from web import db
from ..common.BaseModel import BaseModel


class SysNotice(BaseModel):
    __tablename__ = 'sys_notice'
    __table_args__ = ({'comment': '通知公告表'})
    notice_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='公告ID')
    notice_title = db.Column(db.String(50), default='', comment='公告标题')
    notice_type = db.Column(db.CHAR(1), default='', comment='公告类型（1通知 2公告)')
    notice_content = db.Column(db.LargeBinary, default='', comment='公告内容')
    status = db.Column(db.CHAR(1), default='N', comment='公告状态（0正常 1关闭）')