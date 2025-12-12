<template>
  <div class="app-container">
    <el-card>
        <template #header>
            <div class="card-header">
                <span>资讯发布审核</span>
                <el-radio-group v-model="statusFilter" size="small" @change="handleFilter">
                    <el-radio-button label="pending">待审核</el-radio-button>
                    <el-radio-button label="approved">已通过</el-radio-button>
                    <el-radio-button label="rejected">已驳回</el-radio-button>
                </el-radio-group>
            </div>
        </template>
        
        <el-table :data="newsList" border style="width: 100%">
            <el-table-column prop="college" label="发布高校" width="180" />
            <el-table-column prop="title" label="资讯标题" show-overflow-tooltip />
            <el-table-column prop="category" label="分类" width="100">
                <template #default="scope">
                    <el-tag>{{ scope.row.category }}</el-tag>
                </template>
            </el-table-column>
             <el-table-column prop="time" label="提交时间" width="180" />
             <el-table-column label="操作" width="200" align="center">
                 <template #default="scope">
                     <el-button size="small" icon="View" link @click="handlePreview(scope.row)">预览</el-button>
                     <el-button size="small" type="success" @click="handleApprove(scope.row)" v-if="scope.row.status === 'pending'">通过</el-button>
                     <el-button size="small" type="danger" @click="handleReject(scope.row)" v-if="scope.row.status === 'pending'">驳回</el-button>
                     <span v-else style="margin-left: 10px">{{ scope.row.status === 'approved' ? '已通过' : '已驳回' }}</span>
                 </template>
             </el-table-column>
        </el-table>
    </el-card>

    <el-dialog title="资讯预览" v-model="previewOpen" width="800px">
        <div v-if="currentNews">
            <h2 style="text-align:center">{{ currentNews.title }}</h2>
            <div style="text-align:center; color:#999; margin: 10px 0">
                <span>{{ currentNews.college }}</span> | <span>{{ currentNews.time }}</span>
            </div>
            <div class="news-content" style="padding: 20px; background: #f9f9f9; min-height: 200px;">
                {{ currentNews.content }}
            </div>
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="previewOpen = false">关 闭</el-button>
                <el-button type="primary" @click="handleApprove(currentNews)" v-if="currentNews && currentNews.status === 'pending'">快速通过</el-button>
            </div>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="AuditNews">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const statusFilter = ref('pending')
const previewOpen = ref(false)
const currentNews = ref(null)

const newsList = ref([
    { id: 1, college: '北京大学', title: '关于2025年强基计划报名的通知', category: '招生快讯', content: '（内容详情Mock）...', time: '2025-05-12 09:00', status: 'pending' },
    { id: 2, college: '清华大学', title: '校园开放日活动安排', category: '校园新闻', content: '（内容详情Mock）...', time: '2025-05-12 09:30', status: 'pending' },
    { id: 3, college: '复旦大学', title: '致2025届高考生的一封信', category: '政策解读', content: '（内容详情Mock）...', time: '2025-05-11 10:00', status: 'approved' }
])

function handleFilter() {
    ElMessage.info('Mock: 列表已过滤')
}

function handlePreview(row) {
    currentNews.value = row
    previewOpen.value = true
}

function handleApprove(row) {
    ElMessageBox.confirm(`确认批准发布 "${row.title}" 吗？`, '审核确认', {
        confirmButtonText: '通过',
        cancelButtonText: '取消',
        type: 'success'
    }).then(() => {
        row.status = 'approved'
        previewOpen.value = false
        ElMessage.success('审核通过')
    }).catch(() => {})
}

function handleReject(row) {
     ElMessageBox.prompt('请输入驳回原因', '驳回确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    }).then(({ value }) => {
        row.status = 'rejected'
        row.remark = value
        previewOpen.value = false
        ElMessage.warning('已驳回')
    }).catch(() => {})
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
