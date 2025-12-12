from web import db
from .common.BaseModel import BaseModel

class FeedbackComplaint(BaseModel):
    __tablename__ = 't_feedback_complaint'
    fb_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='反馈/投诉ID')
    user_id = db.Column(db.BigInteger, comment='用户ID')
    type = db.Column(db.String(20), comment='类型（学生/高校）')
    content = db.Column(db.Text, comment='内容')
    attachment_path = db.Column(db.String(200), comment='附件路径')
    status = db.Column(db.String(20), comment='状态')
    # 继承通用字段 from BaseModel
