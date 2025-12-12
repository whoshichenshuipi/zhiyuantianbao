<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>智能问答库维护</span>
          <el-button type="primary" icon="Plus" @click="handleAdd">新增问答</el-button>
        </div>
      </template>

      <el-table :data="faqList" border style="width: 100%">
        <el-table-column prop="question" label="问题关键词" width="250" />
        <el-table-column prop="answer" label="自动回复内容" show-overflow-tooltip />
        <el-table-column prop="hits" label="匹配次数" width="100" align="center" />
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" v-model="open" width="500px">
        <el-form :model="form" label-width="80px">
            <el-form-item label="问题">
                <el-input v-model="form.question" placeholder="例如：分数线、学费、转专业" />
            </el-form-item>
             <el-form-item label="回复">
                <el-input v-model="form.answer" type="textarea" :rows="4" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="open = false">取 消</el-button>
                <el-button type="primary" @click="submitForm">确 定</el-button>
            </div>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="CollegeFaq">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const title = ref('')
const open = ref(false)
const form = reactive({ id: null, question: '', answer: '' })

const faqList = ref([
    { id: 1, question: '分数线', answer: '我校历年录取分数线请参考官网数据，通常理科需650分以上。', hits: 1250 },
    { id: 2, question: '转专业', answer: '学生入校一年后，虽然成绩优秀者可申请转专业，比例约为10%。', hits: 340 },
    { id: 3, question: '宿舍条件', answer: '本科生4人一间，上床下桌，空调、独卫齐全。', hits: 890 }
])

function handleAdd() {
    title.value = '新增问答'
    open.value = true
    form.id = null
    form.question = ''
    form.answer = ''
}

function handleEdit(row) {
    title.value = '编辑问答'
    open.value = true
    Object.assign(form, row)
}

function handleDelete(index) {
     ElMessageBox.confirm('确认删除该条问答吗?', '提示', { type: 'warning' })
     .then(() => {
         faqList.value.splice(index, 1)
         ElMessage.success('删除成功')
     }).catch(()=>{})
}

function submitForm() {
    if(!form.question || !form.answer) {
        ElMessage.warning('请填写完整')
        return
    }
    
    if(form.id) {
        // Edit logic mockup
        const index = faqList.value.findIndex(item => item.id === form.id)
        if(index > -1) Object.assign(faqList.value[index], form)
    } else {
        // Add logic mockup
        faqList.value.push({ ...form, id: Date.now(), hits: 0 })
    }
    open.value = false
    ElMessage.success('保存成功')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
