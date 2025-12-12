from web import db
from flask_login import UserMixin
from ..common.BaseModel import BaseModel


class SysPost(BaseModel, UserMixin):
    __tablename__ = 'sys_post'
    __table_args__ = ({'comment': '岗位信息表'})
    post_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='岗位ID')
    post_code = db.Column(db.String(64), comment='岗位编码')
    post_name = db.Column(db.String(50), comment='岗位名称')
    post_sort = db.Column(db.Integer, comment='显示顺序')
    status = db.Column(db.CHAR(1), comment='状态（0正常 1停用）')