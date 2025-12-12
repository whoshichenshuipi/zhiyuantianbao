from web import db
from .common.BaseModel import BaseModel

class AdmissionProbability(BaseModel):
    __tablename__ = 't_admission_probability'
    prob_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='概率ID')
    plan_id = db.Column(db.BigInteger, comment='志愿方案ID')
    probability = db.Column(db.Float, comment='录取概率')
    risk_level = db.Column(db.String(20), comment='风险等级')
    analysis_data = db.Column(db.Text, comment='分析数据')
    # 继承通用字段 from BaseModel
