export const mockRouters = {
    msg: '操作成功',
    code: 200,
    data: [
        // 考生/家长端菜单
        {
            name: 'Student',
            path: '/student',
            hidden: false,
            redirect: 'noRedirect',
            component: 'Layout',
            alwaysShow: true,
            meta: { title: '考生服务', icon: 'user', noCache: false, roles: ['student'] },
            children: [
                {
                    name: 'Profile',
                    path: 'profile',
                    hidden: false,
                    component: 'student/profile/index',
                    meta: { title: '个人信息', icon: 'form', noCache: false }
                },
                {
                    name: 'Search',
                    path: 'search',
                    hidden: false,
                    component: 'student/search/index',
                    meta: { title: '院校查询', icon: 'search', noCache: false }
                },
                {
                    name: 'Recommend',
                    path: 'recommend',
                    hidden: false,
                    component: 'student/recommend/index',
                    meta: { title: '智能推荐', icon: 'star', noCache: false }
                },
                {
                    name: 'Plan',
                    path: 'plan',
                    hidden: false,
                    component: 'student/plan/index',
                    meta: { title: '志愿方案', icon: 'list', noCache: false }
                },
                {
                    name: 'Probability',
                    path: 'probability',
                    hidden: false,
                    component: 'student/probability/index',
                    meta: { title: '录取概率', icon: 'chart', noCache: false }
                },
                {
                    name: 'Community',
                    path: 'community',
                    hidden: false,
                    component: 'student/community/index',
                    meta: { title: '社区讨论', icon: 'message', noCache: false }
                },
                {
                    name: 'Consult',
                    path: 'consult',
                    hidden: false,
                    component: 'student/consult/index',
                    meta: { title: '咨询互动', icon: 'wechat', noCache: false }
                }
            ]
        },
        // 招生高校端菜单
        {
            name: 'College',
            path: '/college',
            hidden: false,
            redirect: 'noRedirect',
            component: 'Layout',
            alwaysShow: true,
            meta: { title: '高校服务', icon: 'school', noCache: false, roles: ['college'] },
            children: [
                {
                    name: 'CollegeInfo',
                    path: 'info',
                    hidden: false,
                    component: 'college/info/index',
                    meta: { title: '院校维护', icon: 'edit', noCache: false }
                },
                {
                    name: 'Publish',
                    path: 'publish',
                    hidden: false,
                    component: 'college/publish/index',
                    meta: { title: '招生发布', icon: 'guide', noCache: false }
                },
                {
                    name: 'HistoryData',
                    path: 'history-data',
                    hidden: false,
                    component: 'college/history-data/index',
                    meta: { title: '录取数据', icon: 'table', noCache: false }
                },
                {
                    name: 'Dashboard',
                    path: 'dashboard',
                    hidden: false,
                    component: 'college/dashboard/index',
                    meta: { title: '生源看板', icon: 'dashboard', noCache: false }
                }
            ]
        },
        // 系统管理扩展 (模拟)
        {
            name: 'System',
            path: '/system',
            hidden: false,
            redirect: 'noRedirect',
            component: 'Layout',
            alwaysShow: true,
            meta: { title: '系统管理', icon: 'system', noCache: false, roles: ['admin'] },
            children: [
                {
                    name: 'User',
                    path: 'user',
                    hidden: false,
                    component: 'system/user/index',
                    meta: { title: '用户管理', icon: 'user', noCache: false }
                },
                {
                    name: 'Role',
                    path: 'role',
                    hidden: false,
                    component: 'system/role/index',
                    meta: { title: '角色管理', icon: 'peoples', noCache: false }
                },
                {
                    name: 'Menu',
                    path: 'menu',
                    hidden: false,
                    component: 'system/menu/index',
                    meta: { title: '菜单管理', icon: 'tree-table', noCache: false }
                }
            ]
        }
    ]
}
