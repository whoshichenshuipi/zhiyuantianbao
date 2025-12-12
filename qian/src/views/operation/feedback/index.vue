<template>
  <div class="app-container">
    <el-card>
        <template #header>
            <div class="card-header">
                <span>用户反馈管理</span>
                <el-radio-group v-model="statusFilter" size="small" @change="handleFilter">
                    <el-radio-button label="pending">待处理</el-radio-button>
                    <el-radio-button label="processed">已处理</el-radio-button>
                </el-radio-group>
            </div>
        </template>
        
        <el-table :data="feedbackList" border style="width: 100%">
            <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                    <el-tag :type="getTypeTag(scope.row.type)">{{ getTypeLabel(scope.row.type) }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="title" label="标题" width="200" show-overflow-tooltip />
            <el-table-column prop="content" label="内容摘要" show-overflow-tooltip />
            <el-table-column prop="user" label="提交用户" width="120" />
            <el-table-column prop="time" label="提交时间" width="180" />
            <el-table-column prop="contact" label="联系方式" width="150" />
             <el-table-column label="操作" width="150" align="center">
                 <template #default="scope">
                     <el-button size="small" type="primary" @click="handleProcess(scope.row)" v-if="scope.row.status === 'pending'">处理</el-button>
                     <span v-else>已回复</span>
                 </template>
             </el-table-column>
        </el-table>
    </el-card>

    <el-dialog title="反馈处理" v-model="open" width="500px">
        <p><strong>反馈内容：</strong>{{ currentItem.content }}</p>
        <el-input v-model="replyContent" type="textarea" :rows="4" placeholder="请输入回复内容..." />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="open = false">取 消</el-button>
                <el-button type="primary" @click="submitReply">确 定</el-button>
            </div>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="OperationFeedback">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const statusFilter = ref('pending')
const open = ref(false)
const currentItem = ref({})
const replyContent = ref('')

const feedbackList = ref([
    { id: 1, type: 'bug', title: '无法上传头像', content: '点击上传按钮没有反应，试了多次也不行。', user: '张三', time: '2025-05-12 10:00', contact: '13800000000', status: 'pending' },
    { id: 2, type: 'suggestion', title: '希望能增加暗黑模式', content: '晚上查资料太刺眼了，希望能由暗黑模式。', user: '李四', time: '2025-05-11 20:00', contact: '', status: 'pending' },
    { id: 3, type: 'complaint', title: '某高校宣传不实', content: '发现某高校在直播中夸大宣传。', user: '王五', time: '2025-05-10 15:30', contact: '', status: 'processed' }
])

function getTypeTag(type) {
    const map = { bug: 'danger', suggestion: 'success', complaint: 'warning', other: 'info' }
    return map[type]
}

function getTypeLabel(type) {
    const map = { bug: '系统故障', suggestion: '功能建议', complaint: '违规投诉', other: '其他' }
    return map[type]
}

function handleFilter() {
    ElMessage.info('Mock: 列表已过滤')
}

function handleProcess(row) {
    currentItem.value = row
    replyContent.value = ''
    open.value = true
}

function submitReply() {
    if(!replyContent.value) {
        ElMessage.warning('请输入回复内容')
        return
    }
    currentItem.value.status = 'processed'
    open.value = false
    ElMessage.success('处理成功')
}
</script>
