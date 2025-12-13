from web import db
from .common.BaseModel import BaseModel

class VolunteerPlan(BaseModel):
    __tablename__ = 't_volunteer_plan'
    plan_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='志愿方案ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('sys_user.user_id'), comment='用户ID')
    college_id = db.Column(db.BigInteger, comment='院校ID')
    major_id = db.Column(db.BigInteger, comment='专业ID')
    priority = db.Column(db.Integer, comment='志愿优先级')
    status = db.Column(db.String(20), default='draft', comment='状态（draft/submitted/admitted/rejected）')
    # 继承通用字段 from BaseModel
