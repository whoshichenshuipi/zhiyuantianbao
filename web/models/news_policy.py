from web import db
from .common.BaseModel import BaseModel

class NewsPolicy(BaseModel):
    __tablename__ = 't_news_policy'
    news_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='资讯ID')
    title = db.Column(db.String(200), comment='标题')
    content = db.Column(db.Text, comment='内容')
    category = db.Column(db.String(50), comment='分类')
    status = db.Column(db.String(20), comment='状态')
    publish_time = db.Column(db.DateTime, comment='发布时间')
    # 继承通用字段 from BaseModel
