<template>
  <div class="app-container">
    <el-card>
        <template #header>
            <div class="card-header">
                <span>业务操作日志审计</span>
                <el-button type="primary" icon="Download" @click="handleExport">导出日志</el-button>
            </div>
        </template>
        
        <el-form :inline="true" :model="queryParams" class="demo-form-inline">
          <el-form-item label="操作人员">
            <el-input v-model="queryParams.user" placeholder="输入用户名" />
          </el-form-item>
           <el-form-item label="操作类型">
            <el-select v-model="queryParams.type" placeholder="全部" clearable>
                 <el-option label="登录" value="login" />
                 <el-option label="修改密码" value="password" />
                 <el-option label="提交志愿" value="submit" />
                 <el-option label="审核计划" value="audit" />
            </el-select>
          </el-form-item>
           <el-form-item label="日期范围">
             <el-date-picker
                v-model="queryParams.date"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
            />
          </el-form-item>
           <el-form-item>
             <el-button type="primary" @click="getList">查询</el-button>
           </el-form-item>
        </el-form>

        <el-table :data="logList" border style="width: 100%">
             <el-table-column prop="id" label="日志ID" width="100" />
             <el-table-column prop="user" label="操作人员" width="150" />
             <el-table-column prop="ip" label="操作IP" width="150" />
             <el-table-column prop="type" label="操作类型" width="120">
                 <template #default="scope">
                     <el-tag>{{ scope.row.type }}</el-tag>
                 </template>
             </el-table-column>
             <el-table-column prop="detail" label="操作详情" show-overflow-tooltip />
             <el-table-column prop="status" label="状态" width="100">
                 <template #default="scope">
                     <el-tag :type="scope.row.status === '成功' ? 'success' : 'danger'">{{ scope.row.status }}</el-tag>
                 </template>
             </el-table-column>
             <el-table-column prop="time" label="操作时间" width="180" />
        </el-table>
        
         <el-pagination
            background
            layout="prev, pager, next"
            :total="100"
            style="margin-top:20px; text-align:right"
          />
    </el-card>
  </div>
</template>

<script setup name="MonitorAudit">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const queryParams = reactive({
    user: '',
    type: '',
    date: []
})

const logList = ref([
    { id: 1001, user: 'admin', ip: '127.0.0.1', type: '审核计划', detail: '通过了北京大学的数学专业招生计划', status: '成功', time: '2025-05-12 10:05:23' },
    { id: 1002, user: 'student_zhang', ip: '192.168.1.10', type: '提交志愿', detail: '提交了第一次模拟志愿表', status: '成功', time: '2025-05-12 09:55:10' },
    { id: 1003, user: 'student_li', ip: '192.168.1.12', type: '登录', detail: '尝试登录系统', status: '失败', time: '2025-05-12 09:50:00' },
     { id: 1004, user: 'college_pku', ip: '192.168.0.5', type: '发布咨询', detail: '发布了新的招生简章', status: '成功', time: '2025-05-12 09:00:00' },
])

function getList() {
    ElMessage.success('Mock: 查询完成')
}

function handleExport() {
    ElMessage.success('Mock: 正在导出 Excel...')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
