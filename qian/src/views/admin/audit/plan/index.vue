<template>
  <div class="app-container">
    <el-card>
        <template #header>
            <div class="card-header">
                <span>招生计划审核</span>
                <el-radio-group v-model="statusFilter" size="small" @change="handleFilter">
                    <el-radio-button label="pending">待审核</el-radio-button>
                    <el-radio-button label="approved">已通过</el-radio-button>
                    <el-radio-button label="rejected">已驳回</el-radio-button>
                </el-radio-group>
            </div>
        </template>
        
        <el-table :data="auditList" border style="width: 100%">
            <el-table-column prop="college" label="提交高校" width="180" />
            <el-table-column prop="province" label="生源省份" width="100" />
            <el-table-column prop="major" label="专业名称" />
            <el-table-column prop="count" label="计划人数" width="100" />
             <el-table-column prop="tuition" label="学费" width="100" />
             <el-table-column prop="time" label="提交时间" width="180" />
             <el-table-column label="操作" width="200" align="center">
                 <template #default="scope">
                     <el-button size="small" type="success" @click="handleApprove(scope.row)" v-if="scope.row.status === 'pending'">通过</el-button>
                     <el-button size="small" type="danger" @click="handleReject(scope.row)" v-if="scope.row.status === 'pending'">驳回</el-button>
                     <span v-else>{{ scope.row.status === 'approved' ? '已通过' : '已驳回' }}</span>
                 </template>
             </el-table-column>
        </el-table>
        
         <pagination
            v-show="total>0"
            :total="total"
            v-model:page="queryParams.pageNum"
            v-model:limit="queryParams.pageSize"
            @pagination="getList"
        />
    </el-card>
  </div>
</template>

<script setup name="AuditPlan">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const statusFilter = ref('pending')
const total = ref(5)
const queryParams = reactive({
    pageNum: 1,
    pageSize: 10
})

const auditList = ref([
    { id: 1, college: '北京大学', province: '四川', major: '数学与应用数学', count: 5, tuition: 5000, time: '2025-05-12 10:00', status: 'pending' },
    { id: 2, college: '清华大学', province: '四川', major: '建筑学', count: 3, tuition: 5000, time: '2025-05-12 10:30', status: 'pending' },
     { id: 3, college: '复旦大学', province: '上海', major: '新闻学', count: 15, tuition: 5500, time: '2025-05-11 15:00', status: 'approved' },
])

function getList() {
    // Mock refresh
}

function handleFilter() {
    // Mock filter
    if(statusFilter.value === 'pending') {
         auditList.value = [
            { id: 1, college: '北京大学', province: '四川', major: '数学与应用数学', count: 5, tuition: 5000, time: '2025-05-12 10:00', status: 'pending' },
            { id: 2, college: '清华大学', province: '四川', major: '建筑学', count: 3, tuition: 5000, time: '2025-05-12 10:30', status: 'pending' }
        ]
    } else if (statusFilter.value === 'approved') {
         auditList.value = [
              { id: 3, college: '复旦大学', province: '上海', major: '新闻学', count: 15, tuition: 5500, time: '2025-05-11 15:00', status: 'approved' }
         ]
    } else {
        auditList.value = []
    }
}

function handleApprove(row) {
    ElMessageBox.confirm(`确认通过 [${row.college} - ${row.major}] 的招生计划吗？`, '审核确认', {
        confirmButtonText: '通过',
        cancelButtonText: '取消',
        type: 'success'
    }).then(() => {
        row.status = 'approved'
        ElMessage.success('已审核通过')
        handleFilter()
    }).catch(() => {})
}

function handleReject(row) {
     ElPromptBox('请输入驳回原因', '驳回确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    }).then(({ value }) => {
        row.status = 'rejected'
        ElMessage.warning('已驳回：' + value)
        handleFilter()
    }).catch(() => {})
}

// Mock prompt helper
function ElPromptBox(message, title, options) {
    return ElMessageBox.prompt(message, title, options)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
