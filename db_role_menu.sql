-- =====================================================
-- 高考志愿填报系统 - 角色菜单权限配置脚本
-- 执行顺序：先执行 db_migration.sql，再执行本脚本
-- =====================================================

-- =====================================================
-- 1. 新增考生/家长端菜单
-- =====================================================
-- 考生端一级目录
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `route_name`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) VALUES
(2000, '考生服务', 0, 5, 'student', NULL, '', '', 1, 0, 'M', '0', '0', '', 'user', 'admin', NOW(), '', NULL, '考生服务目录');

-- 考生端二级菜单
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `route_name`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) VALUES
(2001, '个人信息', 2000, 1, 'profile', 'student/profile/index', '', '', 1, 0, 'C', '0', '0', 'student:profile:list', 'user', 'admin', NOW(), '', NULL, '个人信息菜单'),
(2002, '院校查询', 2000, 2, 'search', 'student/search/index', '', '', 1, 0, 'C', '0', '0', 'student:search:list', 'search', 'admin', NOW(), '', NULL, '院校查询菜单'),
(2003, '智能推荐', 2000, 3, 'recommend', 'student/recommend/index', '', '', 1, 0, 'C', '0', '0', 'student:recommend:list', 'star', 'admin', NOW(), '', NULL, '智能推荐菜单'),
(2004, '志愿方案', 2000, 4, 'plan', 'student/plan/index', '', '', 1, 0, 'C', '0', '0', 'student:plan:list', 'list', 'admin', NOW(), '', NULL, '志愿方案菜单'),
(2005, '录取概率', 2000, 5, 'probability', 'student/probability/index', '', '', 1, 0, 'C', '0', '0', 'student:probability:list', 'chart', 'admin', NOW(), '', NULL, '录取概率菜单'),
(2006, '社区讨论', 2000, 6, 'community', 'student/community/index', '', '', 1, 0, 'C', '0', '0', 'student:community:list', 'peoples', 'admin', NOW(), '', NULL, '社区讨论菜单'),
(2007, '资讯政策', 2000, 7, 'news', 'student/news/index', '', '', 1, 0, 'C', '0', '0', 'student:news:list', 'documentation', 'admin', NOW(), '', NULL, '资讯政策菜单'),
(2008, '问题反馈', 2000, 8, 'feedback', 'student/feedback/index', '', '', 1, 0, 'C', '0', '0', 'student:feedback:list', 'message', 'admin', NOW(), '', NULL, '问题反馈菜单'),
(2009, '联系客服', 2000, 9, 'service', 'student/service/index', '', '', 1, 0, 'C', '0', '0', 'student:service:list', 'phone', 'admin', NOW(), '', NULL, '联系客服菜单'),
(2010, '高校咨询', 2000, 10, 'consult', 'student/consult/index', '', '', 1, 0, 'C', '0', '0', 'student:consult:list', 'education', 'admin', NOW(), '', NULL, '高校咨询菜单');

-- =====================================================
-- 2. 新增招生高校端菜单
-- =====================================================
-- 高校端一级目录
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `route_name`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) VALUES
(2100, '高校服务', 0, 6, 'college', NULL, '', '', 1, 0, 'M', '0', '0', '', 'education', 'admin', NOW(), '', NULL, '高校服务目录');

-- 高校端二级菜单
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `route_name`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) VALUES
(2101, '院校信息', 2100, 1, 'info', 'college/info/index', '', '', 1, 0, 'C', '0', '0', 'college:info:list', 'education', 'admin', NOW(), '', NULL, '院校信息菜单'),
(2102, '招生发布', 2100, 2, 'publish', 'college/publish/index', '', '', 1, 0, 'C', '0', '0', 'college:publish:list', 'form', 'admin', NOW(), '', NULL, '招生发布菜单'),
(2103, '历年数据', 2100, 3, 'history-data', 'college/history-data/index', '', '', 1, 0, 'C', '0', '0', 'college:data:list', 'chart', 'admin', NOW(), '', NULL, '历年数据菜单'),
(2104, '生源看板', 2100, 4, 'dashboard', 'college/dashboard/index', '', '', 1, 0, 'C', '0', '0', 'college:dashboard:list', 'dashboard', 'admin', NOW(), '', NULL, '生源看板菜单'),
(2105, '在线咨询', 2100, 5, 'chat', 'college/chat/index', '', '', 1, 0, 'C', '0', '0', 'college:chat:list', 'message', 'admin', NOW(), '', NULL, '在线咨询菜单'),
(2106, '问答库', 2100, 6, 'faq', 'college/faq/index', '', '', 1, 0, 'C', '0', '0', 'college:faq:list', 'question', 'admin', NOW(), '', NULL, '问答库菜单'),
(2107, '校园资讯', 2100, 7, 'news', 'college/news/index', '', '', 1, 0, 'C', '0', '0', 'college:news:list', 'documentation', 'admin', NOW(), '', NULL, '校园资讯菜单');

-- =====================================================
-- 3. 配置角色菜单关联
-- =====================================================
-- 考生角色(role_id=100)关联菜单
INSERT INTO `sys_role_menu` (`role_id`, `menu_id`) VALUES
(100, 2000), -- 考生服务目录
(100, 2001), -- 个人信息
(100, 2002), -- 院校查询
(100, 2003), -- 智能推荐
(100, 2004), -- 志愿方案
(100, 2005), -- 录取概率
(100, 2006), -- 社区讨论
(100, 2007), -- 资讯政策
(100, 2008), -- 问题反馈
(100, 2009), -- 联系客服
(100, 2010); -- 高校咨询

-- 高校角色(role_id=101)关联菜单
INSERT INTO `sys_role_menu` (`role_id`, `menu_id`) VALUES
(101, 2100), -- 高校服务目录
(101, 2101), -- 院校信息
(101, 2102), -- 招生发布
(101, 2103), -- 历年数据
(101, 2104), -- 生源看板
(101, 2105), -- 在线咨询
(101, 2106), -- 问答库
(101, 2107); -- 校园资讯

-- =====================================================
-- 完成提示
-- =====================================================
SELECT '角色菜单权限配置完成！' AS message;
SELECT '考生角色(student)已关联11个菜单' AS student_role;
SELECT '高校角色(college)已关联8个菜单' AS college_role;
