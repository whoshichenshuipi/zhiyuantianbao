-- 高考志愿填报系统业务表迁移脚本
-- 执行前请确保已创建数据库 zhiyuan

-- 1. 考生/家长个人信息表
CREATE TABLE IF NOT EXISTS `t_examiner_info` (
    `examiner_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '考生信息ID',
    `user_id` BIGINT COMMENT '关联用户ID',
    `interest` VARCHAR(200) COMMENT '兴趣爱好',
    `region_pref` VARCHAR(100) COMMENT '地区偏好',
    `subject_strength` VARCHAR(200) COMMENT '学科优势',
    `score` INT COMMENT '高考分数',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志（0存在 2删除）',
    PRIMARY KEY (`examiner_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考生/家长个人信息表';

-- 2. 院校专业库
CREATE TABLE IF NOT EXISTS `t_college_major` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `college_id` BIGINT COMMENT '院校ID',
    `major_id` BIGINT COMMENT '专业ID',
    `region` VARCHAR(100) COMMENT '地区',
    `level` VARCHAR(50) COMMENT '层次',
    `category` VARCHAR(50) COMMENT '类别',
    `course_setting` VARCHAR(200) COMMENT '课程设置',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`id`),
    KEY `idx_college_major` (`college_id`, `major_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='院校专业库';

-- 3. 志愿方案表
CREATE TABLE IF NOT EXISTS `t_volunteer_plan` (
    `plan_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '志愿方案ID',
    `user_id` BIGINT COMMENT '用户ID',
    `college_id` BIGINT COMMENT '院校ID',
    `major_id` BIGINT COMMENT '专业ID',
    `priority` INT COMMENT '志愿优先级',
    `status` VARCHAR(20) DEFAULT 'draft' COMMENT '状态',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`plan_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='志愿方案表';

-- 4. 历年录取数据表
CREATE TABLE IF NOT EXISTS `t_admission_data` (
    `admission_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '录取数据ID',
    `college_id` BIGINT COMMENT '院校ID',
    `major_id` BIGINT COMMENT '专业ID',
    `year` INT COMMENT '年份',
    `province` VARCHAR(100) COMMENT '省份',
    `score_line` INT COMMENT '分数线',
    `rank` INT COMMENT '位次',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`admission_id`),
    KEY `idx_college_major_year` (`college_id`, `major_id`, `year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='历年录取数据表';

-- 5. 录取概率评估表
CREATE TABLE IF NOT EXISTS `t_admission_probability` (
    `prob_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '概率ID',
    `plan_id` BIGINT COMMENT '志愿方案ID',
    `probability` FLOAT COMMENT '录取概率',
    `risk_level` VARCHAR(20) COMMENT '风险等级',
    `analysis_data` TEXT COMMENT '分析数据',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`prob_id`),
    KEY `idx_plan_id` (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='录取概率评估表';

-- 6. 社区讨论内容表
CREATE TABLE IF NOT EXISTS `t_community_content` (
    `content_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '内容ID',
    `user_id` BIGINT COMMENT '用户ID',
    `title` VARCHAR(200) COMMENT '标题',
    `body` TEXT COMMENT '正文',
    `type` VARCHAR(20) COMMENT '类型',
    `parent_id` BIGINT COMMENT '父内容ID',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`content_id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社区讨论内容表';

-- 7. 资讯与政策表
CREATE TABLE IF NOT EXISTS `t_news_policy` (
    `news_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '资讯ID',
    `title` VARCHAR(200) COMMENT '标题',
    `content` TEXT COMMENT '内容',
    `category` VARCHAR(50) COMMENT '分类',
    `status` VARCHAR(20) COMMENT '状态',
    `publish_time` DATETIME COMMENT '发布时间',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资讯与政策表';

-- 8. 问题反馈与投诉表
CREATE TABLE IF NOT EXISTS `t_feedback_complaint` (
    `fb_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '反馈ID',
    `user_id` BIGINT COMMENT '用户ID',
    `type` VARCHAR(20) COMMENT '类型',
    `content` TEXT COMMENT '内容',
    `attachment_path` VARCHAR(200) COMMENT '附件路径',
    `status` VARCHAR(20) COMMENT '状态',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`fb_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='问题反馈与投诉表';

-- 9. 客服交互记录表
CREATE TABLE IF NOT EXISTS `t_customer_service` (
    `cs_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '客服记录ID',
    `user_id` BIGINT COMMENT '用户ID',
    `college_id` BIGINT COMMENT '高校ID',
    `type` VARCHAR(20) COMMENT '类型',
    `message` TEXT COMMENT '消息内容',
    `timestamp` DATETIME COMMENT '时间戳',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`cs_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客服交互记录表';

-- 10. 高校信息表
CREATE TABLE IF NOT EXISTS `t_college_info` (
    `college_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '高校ID',
    `name` VARCHAR(200) COMMENT '高校名称',
    `intro` TEXT COMMENT '简介',
    `photo` VARCHAR(200) COMMENT '图片路径',
    `specialties` TEXT COMMENT '专业特色',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`college_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='高校信息表';

-- 11. 生源看板数据表
CREATE TABLE IF NOT EXISTS `t_college_student_source` (
    `source_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '数据源ID',
    `college_id` BIGINT COMMENT '高校ID',
    `candidate_count` INT COMMENT '考生人数',
    `score_distribution` TEXT COMMENT '分数分布JSON',
    `region_distribution` TEXT COMMENT '地区分布JSON',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` CHAR(1) DEFAULT '0' COMMENT '删除标志',
    PRIMARY KEY (`source_id`),
    KEY `idx_college_id` (`college_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生源看板数据表';

-- 新增角色记录
INSERT INTO `sys_role` (`role_id`, `role_name`, `role_key`, `role_sort`, `data_scope`, `menu_check_strictly`, `dept_check_strictly`, `status`, `del_flag`, `create_by`, `create_time`) VALUES
(100, '考生/家长', 'student', 3, '1', 1, 1, '0', '0', 'admin', NOW()),
(101, '招生高校', 'college', 4, '1', 1, 1, '0', '0', 'admin', NOW());

-- 完成
SELECT '迁移脚本执行完成！共创建11张业务表，新增2个角色。' AS message;
