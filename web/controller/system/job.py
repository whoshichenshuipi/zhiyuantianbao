from web.routes import main_routes
from web.models import SysJob, SysJobLog
from flask import request, jsonify, current_app
from flask_login import login_required
from web import db
from web.decorator import permission
import flask_excel as excel
from croniter import croniter
from datetime import datetime
from web import scheduler
import time


def get_target_function_and_args(function_path_str):
    args = []
    parts = []
    if function_path_str.find('(') > 0:
        function_part, args_part = function_path_str.split('(', 1)
        parts = function_part.split('.')
        args_list = args_part.rstrip(')').split(',')
        for arg in args_list:
            if arg.strip() == 'true':
                args.append(True)
            elif arg.strip() == 'false':
                args.append(False)
            else:
                args.append(eval(arg.strip().replace('L', '').replace('D', '')))
    else:
        parts = function_path_str.split('.')
    parts.append(args)
    return parts


def next_execution_time(cron_expression):
    base_time = datetime.now()
    cron = croniter(cron_expression, base_time)
    return cron.get_next(datetime)


def after_task_log(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        run_ms = (time.time() - start_time) * 1000
        from app import app
        with app.app_context():
            sysJobLog = SysJobLog()
            sysJobLog.job_name = args[0]['jobName']
            sysJobLog.job_group = args[0]['jobGroup']
            sysJobLog.invoke_target = args[0]['invokeTarget']
            sysJobLog.job_message = f"{args[0]['jobName']} 总共耗时：{run_ms}毫秒"
            sysJobLog.status = '0' if result['code'] else '1'
            if not result['code']:
                sysJobLog.exception_info = result['msg']
            db.session.add(sysJobLog)
        return result
    return wrapper


@after_task_log
def execute_task(job):
    try:
        target_module, target_function, args = get_target_function_and_args(job['invokeTarget'].strip())
        module = __import__('web.task.'+target_module, fromlist=[target_function])
        function = getattr(module, target_function)
        function(args) if len(args) > 0 else function()
        return {"code": True, "msg": "执行成功"}
    except Exception as e:
        print(f"执行任务 {job['jobId']} 时出错: {e}")
        return {"code": False, "msg": str(e)}


def add_job(job):
    scheduler.add_job(execute_task, 'cron', args=(job,), second=job['cronExpression'].split(' ')[0],
                      minute=job['cronExpression'].split(' ')[1], hour=job['cronExpression'].split(' ')[2],
                      day=job['cronExpression'].split(' ')[3].replace("?", "*"), month=job['cronExpression'].split(' ')[4],
                      day_of_week=job['cronExpression'].split(' ')[5].replace("?", "*"), id=f"{job['jobId']}_{job['jobName']}",
                      misfire_grace_time=30, replace_existing=(False if job['concurrent'] == '0' else True))


def createScheduleJob(job):
    job_id = f"{job['jobId']}_{job['jobName']}"
    specific_job = scheduler.get_job(job_id)
    if specific_job:
        scheduler.remove_job(job_id)
    #misfirePolicy 计划执行错误策略（1立即执行 2执行一次 3放弃执行）
    if job['status'] == '0' and job['misfirePolicy'] == '1':
        add_job(job)
    elif job['misfirePolicy'] == '2':
        execute_task(job)


def deleteScheduleJob(job):
    job_id = f"{job['jobId']}_{job['jobName']}"
    specific_job = scheduler.get_job(job_id)
    if specific_job:
        scheduler.remove_job(job_id)


@main_routes.route('/monitor/job/list', methods=['GET'])
@login_required
@permission('monitor:job:list')
def sysjob_list():
    filters = []
    if request.args.get('jobName'):
        filters.append(SysJob.job_name.like('%' + request.args.get('jobName') + '%'))
    if request.args.get('jobGroup'):
        filters.append(SysJob.job_group == request.args.get('jobGroup'))
    if request.args.get('status'):
        filters.append(SysJob.status == request.args.get('status'))
    order_by = []
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysJob.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    sysJobs = pagination.items
    return jsonify({'total': pagination.total, 'rows': [sysJob.to_json() for sysJob in sysJobs], 'code': 200})


@main_routes.route('/monitor/job', methods=['POST'])
@login_required
@permission('monitor:job:add')
def sysjob_add():
    sysjob = SysJob()
    if 'jobName' in request.json: sysjob.job_name = request.json['jobName']
    if 'jobGroup' in request.json: sysjob.job_group = request.json['jobGroup']
    if 'invokeTarget' in request.json: sysjob.invoke_target = request.json['invokeTarget']
    if 'cronExpression' in request.json: sysjob.cron_expression = request.json['cronExpression']
    if 'misfirePolicy' in request.json: sysjob.misfire_policy = request.json['misfirePolicy']
    if 'concurrent' in request.json: sysjob.concurrent = request.json['concurrent']
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    db.session.commit()
    job_id = sysjob.job_id
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/monitor/job', methods=['PUT'])
@login_required
@permission('monitor:job:edit')
def sysjob_update():
    sysjob = SysJob.query.get(request.json['jobId'])
    if 'jobName' in request.json: sysjob.job_name = request.json['jobName']
    if 'jobGroup' in request.json: sysjob.job_group = request.json['jobGroup']
    if 'invokeTarget' in request.json: sysjob.invoke_target = request.json['invokeTarget']
    if 'cronExpression' in request.json: sysjob.cron_expression = request.json['cronExpression']
    if 'misfirePolicy' in request.json: sysjob.misfire_policy = request.json['misfirePolicy']
    if 'concurrent' in request.json: sysjob.concurrent = request.json['concurrent']
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/monitor/job/run', methods=['PUT'])
@login_required
@permission('monitor:job:changeStatus')
def sysjob_run():
    sysjob = SysJob.query.get(request.json['jobId'])
    res = execute_task(sysjob.to_json())
    if res['code']:
        return jsonify({'code': 200, 'msg': '执行成功'})
    return jsonify({'code': 500, 'msg': f"执行任务 {request.json['jobId']} 时出错:{res['msg']}"})


@main_routes.route('/monitor/job/<string:ids>', methods=['DELETE'])
@login_required
@permission('monitor:job:remove')
def sysjob_delete(ids):
    idList = ids.split(',')
    for id in idList:
        sysjob = SysJob.query.get(id)
        if sysjob:
            db.session.delete(sysjob)
            deleteScheduleJob(sysjob.to_json())

    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/monitor/job/changeStatus', methods=['PUT'])
@login_required
@permission('monitor:job:changeStatus')
def sysjob_status_update():
    sysjob = SysJob.query.get(request.json['jobId'])
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/monitor/job/<string:id>', methods=['GET'])
@login_required
@permission('monitor:job:query')
def sysjob_getById(id):
    sysjob = SysJob.query.get(id)
    if sysjob:
        data = sysjob.to_json()
        try:
            data['nextValidTime'] = next_execution_time(sysjob.cron_expression.replace('?', '*'))
        except Exception as e:
            data['nextValidTime'] = ''
        return jsonify({'code': 200, 'msg': '操作成功', 'data': data})
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@main_routes.route('/monitor/job/export', methods=['POST'])
@login_required
@permission('monitor:job:export')
def sysjob_export():
    rows = []
    rows.append(['任务ID', '任务名称', '任务组名', '调用目标字符串', '状态', '备注', '创建时间'])
    sysjobs = SysJob.query.all()
    for sysjob in sysjobs:
        row = []
        row.append(sysjob.job_id)
        row.append(sysjob.job_name)
        row.append(sysjob.job_group)
        row.append(sysjob.invoke_target)
        if sysjob.status == '0':
            row.append('正常')
        elif sysjob.status == '1':
            row.append('停用')
        row.append(sysjob.remark)
        row.append(sysjob.create_time)

        rows.append(row)

    return excel.make_response_from_array(rows, "xlsx", file_name="sys_job")


@main_routes.route('/monitor/jobLog/list', methods=['GET'])
@login_required
@permission('monitor:jobLog:list')
def sysjobLog_list():
    filters = []
    if request.args.get('jobName'):
        filters.append(SysJobLog.job_name.like('%' + request.args.get('jobName') + '%'))
    if request.args.get('jobGroup'):
        filters.append(SysJobLog.job_group == request.args.get('jobGroup'))
    if request.args.get('status'):
        filters.append(SysJobLog.status == request.args.get('status'))
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysJobLog.create_time > request.args['params[beginTime]'])
        filters.append(SysJobLog.create_time < request.args['params[endTime]'])
    order_by = []
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysJobLog.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    sysJobLogs = pagination.items
    return jsonify({'total': pagination.total, 'rows': [sysJobLog.to_json() for sysJobLog in sysJobLogs], 'code': 200})


@main_routes.route('/monitor/jobLog/<string:ids>', methods=['DELETE'])
@login_required
@permission('monitor:jobLog:remove')
def sysjoblog_delete(ids):
    idList = ids.split(',')
    for id in idList:
        sysjoblog = SysJobLog.query.get(id)
        if sysjoblog:
            db.session.delete(sysjoblog)
    return jsonify({'code': 200, 'msg': '操作成功'})


@main_routes.route('/monitor/jobLog/clean', methods=['DELETE'])
@login_required
@permission('monitor:jobLog:clean')
def sysjoblog_clean():
    return jsonify({'code': 500, 'msg': '不支持清空'})


@main_routes.route('/monitor/jobLog/export', methods=['POST'])
@login_required
@permission('monitor:jobLog:export')
def sysjoblog_export():
    rows = []
    rows.append(['任务日志ID', '任务名称', '任务组名', '调用目标字符串', '状态', '异常信息', '创建时间'])
    sysjoblogs = SysJobLog.query.all()
    for sysjoblog in sysjoblogs:
        row = []
        row.append(sysjoblog.job_log_id)
        row.append(sysjoblog.job_name)
        row.append(sysjoblog.job_group)
        row.append(sysjoblog.invoke_target)
        if sysjoblog.status == '0':
            row.append('正常')
        elif sysjoblog.status == '1':
            row.append('停用')
        row.append(sysjoblog.exception_info)
        row.append(sysjoblog.create_time)

        rows.append(row)

    return excel.make_response_from_array(rows, "xlsx", file_name="sys_job_log")
