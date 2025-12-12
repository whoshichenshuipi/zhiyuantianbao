from web import db
from datetime import datetime
from flask_login import current_user
from flask import url_for
import json


class ModelMixin(db.Model):
    __abstract__ = True
    def get_id(self):
        for column in self.__table__.primary_key.columns:
            if column.primary_key:
                return getattr(self, column.name)

    def __repr__(self):
        attr_strings = []
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                if isinstance(value, str):
                    attr_strings.append(f"{attr}='{value}'")
                else:
                    attr_strings.append(f"{attr}={value}")

        return f"{self.__class__.__name__}({', '.join(attr_strings)})"

    def to_dict(self):
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])

    def to_json(self):
        def convert_to_camel_case(snake_str):
            words = snake_str.split('_')
            return words[0] + ''.join(word.title() for word in words[1:])
        json_data = {}
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                camel_case_attr = convert_to_camel_case(attr)
                if isinstance(value, datetime):
                    json_data[camel_case_attr] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    if camel_case_attr == 'menuCheckStrictly' or camel_case_attr == 'deptCheckStrictly':
                        json_data[camel_case_attr] = False if value is None else bool(value)
                    elif camel_case_attr == 'noticeContent':
                        json_data[camel_case_attr] = value.decode('utf-8')
                    elif camel_case_attr == 'isFrame' or camel_case_attr == 'isCache':
                        json_data[camel_case_attr] = str(value)
                    elif self.__tablename__ == 'sys_user' and camel_case_attr == 'avatar':
                        json_data[camel_case_attr] = '' if value is None or value == '' else url_for('static', filename=value, _external=True)
                    else:
                        json_data[camel_case_attr] = value
        if self.__tablename__ == 'sys_user':
            if self.dept is not None:
                json_data['dept']  = self.dept.to_json()
                json_data['deptId'] = self.dept.dept_id

            if len(self.roles.all()) > 0:
                json_data['roles'] = [role.to_json() for role in self.roles.all()]

            if len(self.posts.all()) > 0:
                json_data['posts'] = [post.to_json() for post in self.posts.all()]
        if self.__tablename__ == 'sys_dept':
            json_data['children'] = [org.to_json() for org in self.children]
        if self.__tablename__ == 'gen_table':
            json_data['columns'] = [column.to_json() for column in self.columns]
            params = json_data['options'] if 'options' in json_data else None
            if params is None or params == '':
                params = '{}'
            params_dict = json.loads(params)
            json_data['treeCode'] = params_dict['treeCode'] if 'treeCode' in params_dict else None
            json_data['treeParentCode'] = params_dict['treeParentCode'] if 'treeParentCode' in params_dict else None
            json_data['treeName'] = params_dict['treeName'] if 'treeName' in params_dict else None
            json_data['parentMenuId'] = params_dict['parentMenuId'] if 'parentMenuId' in params_dict else None
            json_data['parentMenuName'] = params_dict['parentMenuName'] if 'parentMenuName' in params_dict else None
            if 'tplCategory' in json_data:
                json_data['crud'] = True if json_data['tplCategory'] == 'crud' else False
                json_data['sub'] = True if json_data['tplCategory'] == 'sub' else False
                json_data['tree'] = True if json_data['tplCategory'] == 'tree' else False
            if self.sub_table is not None:
                json_data['subTable'] = self.sub_table.to_json()
            if self.pk_column is not None:
                json_data['pkColumn'] = self.pk_column.to_json()
        if self.__tablename__ == 'gen_table_column':
            json_data['capJavaField'] = json_data['javaField'].capitalize() if 'javaField' in json_data else ''
            json_data['increment'] = True if 'isIncrement' in json_data and json_data['isIncrement'] == '1' else False
            json_data['insert'] = True if json_data['isInsert'] == '1' else False
            json_data['edit'] = True if 'isEdit' in json_data and json_data['isEdit'] == '1' else False
            json_data['list'] = True if 'isList' in json_data and json_data['isList'] == '1' else False
            json_data['pk'] = True if json_data['isPk'] == '1' else False
            json_data['query'] = True if 'isQuery' in json_data and json_data['isQuery'] == '1' else False
            json_data['required'] = True if json_data['isRequired'] == '1' else False
            json_data['superColumn'] = True if 'javaField' in json_data and json_data['javaField'] in {"createBy", "createTime", "updateBy", "updateTime", "remark","parentName", "parentId", "orderNum", "ancestors"} else False
            json_data['usableColumn'] = True if 'javaField' in json_data and json_data['javaField'] in {"parentId", "orderNum", "remark"} else False
        return json_data


class BaseModel(ModelMixin):
    @classmethod
    def before_update(cls, mapper, connection, target):
            if hasattr(target, 'update_by'):
                # 这里可以添加你想要执行的代码
                print(f"------------------- {target} is update their update_by to {target.update_by}")
                if current_user is not None:
                    target.update_by = current_user.user_name
                
    @classmethod
    def before_insert(cls, mapper, connection, target):
        if hasattr(target, 'create_by'):
            print(f"------------------- {target} is insert their create_by to {target.create_by}")
            if current_user is not None:
                target.create_by = current_user.user_name

    __abstract__ = True
    create_by = db.Column(db.String(64), default='', comment="创建者")
    create_time = db.Column(db.DATETIME, index=True,  default=datetime.now, comment="创建时间")
    update_by = db.Column(db.String(64), default='', comment="更新者")
    update_time = db.Column(db.DATETIME, index=True, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    remark = db.Column(db.String(500), default=None, comment="备注")