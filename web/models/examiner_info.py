from web import db
from .common.BaseModel import BaseModel

class ExaminerInfo(BaseModel):
    __tablename__ = 't_examiner_info'
    examiner_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='考生信息ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('sys_user.user_id'), comment='关联用户ID')
    interest = db.Column(db.String(200), comment='兴趣爱好')
    region_pref = db.Column(db.String(100), comment='地区偏好')
    subject_strength = db.Column(db.String(200), comment='学科优势')
    score = db.Column(db.Integer, comment='高考分数')
    # 通用字段继承自 BaseModel (create_by, create_time, update_by, update_time, del_flag)
