from web import db
from .common.BaseModel import BaseModel

class CollegeMajor(BaseModel):
    __tablename__ = 't_college_major'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键')
    college_id = db.Column(db.BigInteger, comment='院校ID')
    major_id = db.Column(db.BigInteger, comment='专业ID')
    region = db.Column(db.String(100), comment='地区')
    level = db.Column(db.String(50), comment='层次')
    category = db.Column(db.String(50), comment='类别')
    course_setting = db.Column(db.String(200), comment='课程设置')
    # 继承通用字段 from BaseModel
