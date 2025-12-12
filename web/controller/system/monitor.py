from web.routes import main_routes
from web.models import SysLogininfor
from flask import request, jsonify
from flask_login import login_required
from web.decorator import permission
import psutil
import os
import platform


@main_routes.route('/monitor/online/list', methods=['GET'])
@login_required
@permission('monitor:online:list')
def monitor_online():
    #todo 登录未缓存
    filters = []
    if request.args.get('userName'):
        filters.append(SysLogininfor.user_name.like('%' + request.args.get('userName') + '%'))
    if request.args.get('ipaddr'):
        filters.append(SysLogininfor.ipaddr.like('%' + request.args.get('ipaddr') + '%'))
    order_by = []
    page = request.args.get('pageNum', 1, type=int)
    rows = request.args.get('pageSize', 10, type=int)
    pagination = SysLogininfor.query.filter(*filters).order_by(*order_by).paginate(
        page=page, per_page=rows, error_out=False)
    sysLogininfors = pagination.items

    return jsonify({'total': pagination.total, 'rows': [sysLogininfor.to_json() for sysLogininfor in sysLogininfors], 'code': 200})


@main_routes.route('/monitor/server', methods=['GET'])
@login_required
@permission('monitor:server:list')
def monitor_server():
    physical_cpu_count = psutil.cpu_count(logical=False)
    cpu_times_percent = psutil.cpu_times_percent()
    memory_info = psutil.virtual_memory()
    total_memory_gb = round(memory_info.total / (1024.0 ** 3), 2)
    used_memory_gb = round(memory_info.used / (1024.0 ** 3), 2)
    available_memory_gb = round(memory_info.available / (1024.0 ** 3), 2)
    memory_usage_percentage = round((used_memory_gb / total_memory_gb) * 100, 2)
    # 获取当前Python进程的PID
    pid = os.getpid()
    p = psutil.Process(pid)
    # 获取内存信息并转换为GB单位
    mem_info = p.memory_info()
    total_memory_gb_py = round(mem_info.rss / (1024.0 ** 3), 2)
    used_memory_gb_py = round(mem_info.rss / (1024.0 ** 3), 2)
    available_memory_gb_py = 0
    memory_usage_percentage_py = round((used_memory_gb_py / total_memory_gb_py) * 100, 2)
    disk_usage = psutil.disk_usage('/')
    total_gb = round(disk_usage.total / (1024.0 ** 3), 2)
    used_gb = round(disk_usage.used / (1024.0 ** 3), 2)
    free_gb = round(disk_usage.free / (1024.0 ** 3), 2)
    percent = disk_usage.percent
    data = {
            "cpu": {
                "cpuNum": physical_cpu_count,
                "total": 0.0,
                "sys": cpu_times_percent.system,
                "used": cpu_times_percent.user,
                "wait": 0.0,
                "free": cpu_times_percent.idle
            },
            "mem": {
                "total": total_memory_gb,
                "used": used_memory_gb,
                "free": available_memory_gb,
                "usage": memory_usage_percentage
            },
            "jvm": {
                "total": total_memory_gb_py,
                "max": 0.0,
                "free": available_memory_gb_py,
                "version": "",
                "home": "",
                "runTime": "",
                "startTime": "",
                "inputArgs": "",
                "used": used_memory_gb_py,
                "usage": memory_usage_percentage_py,
                "name": ""
            },
            "sys": {
                "computerName": platform.system(),
                "computerIp": "",
                "userDir": os.path.dirname(os.path.abspath(__file__)),
                "osName": platform.platform(),
                "osArch": platform.machine()
            },
            "sysFiles": [
                {
                    "dirName": "",
                    "sysTypeName": "",
                    "typeName": "",
                    "total": f"{total_gb} GB",
                    "free": f"{free_gb} GB",
                    "used": f"{used_gb} GB",
                    "usage": percent
                }
            ]
    }

    return jsonify({'code': 200, 'data': data})