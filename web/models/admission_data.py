from web import db
from .common.BaseModel import BaseModel

class AdmissionData(BaseModel):
    __tablename__ = 't_admission_data'
    admission_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='录取数据ID')
    college_id = db.Column(db.BigInteger, comment='院校ID')
    major_id = db.Column(db.BigInteger, comment='专业ID')
    year = db.Column(db.Integer, comment='年份')
    province = db.Column(db.String(100), comment='省份')
    score_line = db.Column(db.Integer, comment='分数线')
    rank = db.Column(db.Integer, comment='位次')
    # 继承通用字段 from BaseModel
