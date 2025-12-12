from web import db
from datetime import datetime
from ..common.BaseModel import ModelMixin


class SysOperLog(ModelMixin):
    __tablename__ = 'sys_oper_log'
    __table_args__ = ({'comment': '操作日志记录'})
    oper_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='日志主键')
    title = db.Column(db.String(50), comment='模块标题')
    business_type = db.Column(db.Integer, comment='业务类型（0其它 1新增 2修改 3删除）')
    method = db.Column(db.String(200), comment='方法名称')
    request_method = db.Column(db.String(10), comment='请求方式')
    operator_type = db.Column(db.Integer, comment='操作类别（0其它 1后台用户 2手机端用户）')
    oper_name = db.Column(db.String(50), comment='操作人员')
    dept_name = db.Column(db.String(50), comment='部门名称')
    oper_url = db.Column(db.String(255), comment='请求URL')
    oper_ip = db.Column(db.String(128), comment='主机地址')
    oper_location = db.Column(db.String(255), comment='操作地点')
    oper_param = db.Column(db.String(2000), comment='请求参数')
    json_result = db.Column(db.String(2000), comment='返回参数')
    status = db.Column(db.Integer, comment='操作状态（0正常 1异常）')
    error_msg = db.Column(db.String(2000), comment='错误消息')
    oper_time = db.Column(db.DATETIME, default=datetime.now, comment='操作时间')
    cost_time = db.Column(db.BigInteger, comment='消耗时间')