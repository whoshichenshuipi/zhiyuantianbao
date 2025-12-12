<template>
  <div class="app-container">
    <div style="margin-bottom: 20px;">
        <el-button type="primary" icon="Edit" @click="handlePublish">发布资讯</el-button>
        <el-input 
            v-model="searchKeyword" 
            placeholder="搜索资讯标题..." 
            style="width: 200px; margin-left: 10px;"
            prefix-icon="Search"
        />
    </div>

    <el-table :data="newsList" border style="width: 100%">
        <el-table-column prop="title" label="标题" show-overflow-tooltip />
        <el-table-column prop="category" label="分类" width="100">
            <template #default="scope">
                <el-tag>{{ scope.row.category }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="time" label="发布时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
             <template #default="scope">
                <el-tag :type="scope.row.status === '已发布' ? 'success' : 'info'">{{ scope.row.status }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
    </el-table>

    <el-dialog :title="title" v-model="open" width="700px">
        <el-form :model="form" label-width="80px">
            <el-form-item label="标题">
                <el-input v-model="form.title" placeholder="请输入标题" />
            </el-form-item>
             <el-form-item label="分类">
                <el-select v-model="form.category">
                    <el-option label="招生快讯" value="招生快讯" />
                    <el-option label="校园新闻" value="校园新闻" />
                    <el-option label="政策解读" value="政策解读" />
                </el-select>
            </el-form-item>
             <el-form-item label="内容">
                <el-input v-model="form.content" type="textarea" :rows="10" placeholder="请输入内容..." />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="open = false">取 消</el-button>
                <el-button type="primary" @click="submitForm">发 布</el-button>
            </div>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="CollegeNews">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const searchKeyword = ref('')
const title = ref('')
const open = ref(false)
const form = reactive({ id: null, title: '', category: '', content: '' })

const newsList = ref([
    { id: 1, title: '2025年本科招生简章发布', category: '招生快讯', time: '2025-05-10 10:00', status: '已发布' },
    { id: 2, title: '校园开放日活动预告', category: '校园新闻', time: '2025-05-09 14:30', status: '已发布' },
    { id: 3, title: '强基计划报名指南', category: '政策解读', time: '2025-05-08 09:00', status: '草稿' }
])

function handlePublish() {
    title.value = '发布新资讯'
    open.value = true
    form.id = null
    form.title = ''
    form.category = '招生快讯'
    form.content = ''
}

function handleEdit(row) {
    title.value = '编辑资讯'
    open.value = true
    Object.assign(form, row)
}

function handleDelete(index) {
     ElMessageBox.confirm('确认删除该条资讯吗?', '提示', { type: 'warning' })
     .then(() => {
         newsList.value.splice(index, 1)
         ElMessage.success('删除成功')
     }).catch(()=>{})
}

function submitForm() {
    if(!form.title || !form.content) {
        ElMessage.warning('请填写完整')
        return
    }
    
    if(form.id) {
        const index = newsList.value.findIndex(item => item.id === form.id)
        if(index > -1) {
            Object.assign(newsList.value[index], { ...form, time: '刚刚', status: '已发布' })
        }
    } else {
        newsList.value.unshift({ ...form, id: Date.now(), time: '刚刚', status: '已发布' })
    }
    open.value = false
    ElMessage.success('发布成功')
}
</script>
