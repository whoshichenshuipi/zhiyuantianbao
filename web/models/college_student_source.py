from web import db
from .common.BaseModel import BaseModel

class CollegeStudentSource(BaseModel):
    __tablename__ = 't_college_student_source'
    source_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='数据源ID')
    college_id = db.Column(db.BigInteger, comment='高校ID')
    candidate_count = db.Column(db.Integer, comment='考生人数')
    score_distribution = db.Column(db.Text, comment='分数分布（JSON）')
    region_distribution = db.Column(db.Text, comment='地区分布（JSON）')
    # 继承通用字段 from BaseModel
