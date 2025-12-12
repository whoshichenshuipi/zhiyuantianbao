from web import db
from flask_login import UserMixin
from ..common.BaseModel import BaseModel


class SysMenu(BaseModel, UserMixin):
    __tablename__ = 'sys_menu'
    __table_args__ = ({'comment': '菜单权限表'})
    menu_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='菜单ID')
    menu_name = db.Column(db.String(50), comment='菜单名称')
    parent_id = db.Column(db.BigInteger, db.ForeignKey('sys_menu.menu_id'), default=0, comment='父菜单ID')
    order_num = db.Column(db.Integer, comment='显示顺序')
    path = db.Column(db.String(200), comment='路由地址')
    component = db.Column(db.String(255), comment='组件路径')
    query = db.Column(db.String(255), comment='路由参数')
    route_name = db.Column(db.String(50), comment='路由名称')
    is_frame = db.Column(db.Integer,default=1, comment='是否为外链（0是 1否）')
    is_cache = db.Column(db.Integer,default=0, comment='是否缓存（0缓存 1不缓存）')
    menu_type = db.Column(db.CHAR(1),default='', comment='菜单类型（M目录 C菜单 F按钮）')
    visible = db.Column(db.CHAR(1),default='0', comment='菜单状态（0显示 1隐藏）')
    status = db.Column(db.CHAR(1),default='0', comment='菜单状态（0正常 1停用）')
    perms = db.Column(db.String(100), comment='权限标识')
    icon = db.Column(db.String(100), comment='菜单图标')
    # parent = db.relationship('SysMenu', remote_side=[menu_id], backref='sys_menu', uselist=False)
    children = db.relationship('SysMenu')

    hidden = False

    def to_tree_select_json(self):
        return {
            'id': self.menu_id,
            'label': self.menu_name,
            'children': [res.to_tree_select_json() for res in self.children]
        }

    def to_router_json(self):
        router = {
            'name': self.path.capitalize() if self.path else '',
            'path': '/' + self.path if self.parent_id == 0 and self.menu_type =='M' and self.is_frame == 1 else ('/'  if self.parent_id == 0 and self.menu_type =='C' and self.is_frame == 1 else self.path ),
            #菜单状态（0显示 1隐藏）
            'hidden': self.hidden if self.hidden == True else (True if self.visible == '1' else False),
            'redirect': 'noRedirect',
            'component': self.component if self.component and not (self.parent_id == 0 and self.menu_type =='C' and self.is_frame == 1) else \
                    ('InnerLink' if (self.component is None or len(self.component)==0) and self.parent_id != 0 and self.is_frame == 1 and self.path.startswith('http') else \
                        ('ParentView' if (self.component is None or len(self.component)==0) and self.parent_id != 0 and self.menu_type =='M'  else 'Layout')),
            'alwaysShow': True,
            'meta': {
                'title': self.menu_name,
                'icon': self.icon,
                'noCache': self.is_cache,
                'link':''
            },
            'children': [
                res.to_router_json() for res in self.children if res.menu_type == 'C' or res.menu_type == 'M'
            ]
        }
        if not router['children']:
            del router['children']
            del router['redirect']
            del router['alwaysShow']
        if not router['component']:
            router['component'] = 'Layout'
        return router

    def to_menu_json(self):
        return {
            'id': self.menu_id,
            'iconCls': self.icon,
            'pid': self.get_pid(),
            'state': 'open',
            'checked': False,
            'attributes': {
                'target': self.path,
                'url': self.component
            },
            'text': self.menu_name
        }

    def get_pid(self):
        if self.parent:
            return self.get_pid()
        return ''
