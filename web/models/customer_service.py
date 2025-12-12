from web import db
from .common.BaseModel import BaseModel

class CustomerService(BaseModel):
    __tablename__ = 't_customer_service'
    cs_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='客服记录ID')
    user_id = db.Column(db.BigInteger, comment='用户ID')
    college_id = db.Column(db.BigInteger, comment='高校ID')
    type = db.Column(db.String(20), comment='类型（智能/人工）')
    message = db.Column(db.Text, comment='消息内容')
    timestamp = db.Column(db.DateTime, comment='时间戳')
    # 继承通用字段 from BaseModel
