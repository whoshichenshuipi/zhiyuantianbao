from web import db
from .common.BaseModel import BaseModel

class CollegeInfo(BaseModel):
    __tablename__ = 't_college_info'
    college_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='高校ID')
    name = db.Column(db.String(200), comment='高校名称')
    intro = db.Column(db.Text, comment='简介')
    photo = db.Column(db.String(200), comment='图片路径')
    specialties = db.Column(db.Text, comment='专业特色')
    # 继承通用字段 from BaseModel
