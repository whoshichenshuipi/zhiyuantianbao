from web import db
from ..common.BaseModel import BaseModel


class SysConfig(BaseModel):
    __tablename__ = 'sys_config'
    __table_args__ = ({'comment': '参数配置表'})
    config_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='参数主键')
    config_name = db.Column(db.String(100),default='', comment='参数名称')
    config_key = db.Column(db.String(100),default='', comment='参数键名')
    config_value = db.Column(db.String(500),default='', comment='参数键值')
    config_type = db.Column(db.CHAR(1),default='N', comment='系统内置（Y是 N否）')