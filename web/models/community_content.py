from web import db
from .common.BaseModel import BaseModel

class CommunityContent(BaseModel):
    __tablename__ = 't_community_content'
    content_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='内容ID')
    user_id = db.Column(db.BigInteger, comment='用户ID')
    title = db.Column(db.String(200), comment='标题')
    body = db.Column(db.Text, comment='正文')
    type = db.Column(db.String(20), comment='类型（提问/回复）')
    parent_id = db.Column(db.BigInteger, comment='父内容ID')
    # 继承通用字段 from BaseModel
