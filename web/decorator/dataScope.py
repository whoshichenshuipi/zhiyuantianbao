from flask_login import current_user
from functools import wraps
from sqlalchemy import text


def dataScope(userAlias):
    def dataScopeFilter(func):
        @wraps(func)
        def inner(*args, **kargs):
            # 查看参数名称列表   获取函数的__code__属性
            if current_user.user_id !=1 and 'filters' in func.__code__.co_varnames[:func.__code__.co_argcount]:
                sqlString = ''
                conditions = []
                #数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5:本人）
                scopeCustomIds = [role.role_id for role in current_user.roles if role.status == '0' and role.data_scope == '2']
                for role in current_user.roles:
                    dataScope = role.data_scope
                    if dataScope in conditions or role.status == '1':
                        continue
                    if dataScope == '1':
                        sqlString = ''
                        conditions.append(dataScope)
                        break
                    elif dataScope == '2':
                        if len(scopeCustomIds)>1:
                            #多个自定数据权限使用in查询，避免多次拼接。
                            sqlString += f' OR {userAlias} IN ( SELECT user_name from sys_user where dept_id IN ( SELECT dept_id FROM sys_role_dept WHERE role_id in ({",".join(scopeCustomIds)})))'
                        else:
                            sqlString += f' OR {userAlias} IN ( SELECT user_name from sys_user where dept_id IN ( SELECT dept_id FROM sys_role_dept WHERE role_id = {role.role_id} ))'
                    elif dataScope == '3':
                        sqlString += f' OR {userAlias} IN (SELECT user_name from sys_user where dept_id = (SELECT dept_id from sys_user where sys_user.user_id = {current_user.user_id}))'
                    elif dataScope == '4':
                        sqlString += f' OR {userAlias} IN (SELECT user_name from sys_user where dept_id IN (SELECT dept_id FROM sys_dept WHERE dept_id = {current_user.dept_id} or find_in_set( {current_user.dept_id} , ancestors )))'
                    elif dataScope == '5':
                        sqlString += f' OR {userAlias} = "{current_user.user_name}"'
                    conditions.append(dataScope)
                #角色都不包含传递过来的权限字符，这个时候sqlString也会为空，所以要限制一下,不查询任何数据
                if len(conditions) == 0:
                    sqlString += f' OR {userAlias} = "0" )'
                if sqlString:
                    query_filters = [text(f' ( {sqlString[4:]} )')]
                    original_filters = kargs.get('filters', [])
                    all_filters = original_filters + query_filters
                    kargs['filters'] = all_filters
            return func(*args, **kargs)
        return inner
    return dataScopeFilter
