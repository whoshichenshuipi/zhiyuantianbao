from web.routes import main_routes
from flask import jsonify
from flask_login import login_required
from web import cache
from web.decorator import permission


@main_routes.route('/monitor/cache', methods=['GET'])
@login_required
@permission('monitor:cache:list')
def monitor_cache():
    return jsonify({'code': 200, 'data': {}})


@main_routes.route('/monitor/cache/getNames', methods=['GET'])
@login_required
@permission('monitor:cache:list')
def monitor_cache_getNames():
    is_exits = []
    data = []
    for config in cache.cache._cache:
        cache_list = config.split('@')
        if not cache_list[0] in is_exits:
            is_exits.append(cache_list[0])
            data.append({'cacheName': cache_list[0], 'remark': cache_list[1] if len(cache_list) > 1 else '', 'cacheKey': '', 'cacheValue': ''})

    return jsonify({'code': 200, 'data': data })


@main_routes.route('/monitor/cache/getKeys/<getName>', methods=['GET'])
@login_required
@permission('monitor:cache:list')
def monitor_cache_getKeys(getName):
    data = []
    for config in cache.cache._cache:
        cache_list = config.split('@')
        if cache_list[0] == getName and len(cache_list) > 2:
            data.append(cache_list[2])
    return jsonify({'code': 200, 'data': data})


@main_routes.route('/monitor/cache/getValue/<getName>/<getKey>', methods=['GET'])
@login_required
@permission('monitor:cache:list')
def monitor_cache_getValue_sys_dict_getKey(getName, getKey):
    data = {}
    for config in cache.cache._cache:
        cache_list = config.split('@')
        if len(cache_list) > 2 and cache_list[0] == getName and cache_list[2] == getKey:
            data['cacheName'] = cache_list[0]
            data['cacheKey'] = cache_list[2]
            data['cacheValue'] = '' if getName == 'captcha_codes' else str(cache.get(config))
            data['remark'] = ''
            break

    return jsonify({'code': 200, 'data': data})


@main_routes.route('/monitor/cache/clearCacheAll', methods=['DELETE'])
@login_required
@permission('monitor:cache:list')
def monitor_cache_clearCacheAll():
    cache.clear()
    return jsonify({'code': 200, 'msg': '操作成功'})