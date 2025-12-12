<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>问题反馈与建议</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="反馈类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="bug">系统故障</el-radio>
            <el-radio label="suggestion">功能建议</el-radio>
            <el-radio label="complaint">违规投诉</el-radio>
            <el-radio label="other">其他</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="简要描述您的问题" />
        </el-form-item>
        <el-form-item label="详细内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="6" placeholder="请详细描述问题重现步骤或您的建议..." />
        </el-form-item>
        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="form.contact" placeholder="手机号/邮箱 (选填，方便我们联系您)" />
        </el-form-item>
        <el-form-item label="截图上传">
           <el-upload
                action="#"
                list-type="picture-card"
                :auto-upload="false"
                :on-change="handleFileChange"
            >
                <el-icon><Plus /></el-icon>
            </el-upload>
            <div>（仅模拟上传）</div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交反馈</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-alert
        title="温馨提示：如遇紧急问题，请直接联系在线客服或拨打服务热线 400-123-4567。"
        type="info"
        show-icon
        style="margin-top: 20px"
    />
  </div>
</template>

<script setup name="StudentFeedback">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const formRef = ref(null)

const form = reactive({
  type: 'bug',
  title: '',
  content: '',
  contact: ''
})

const rules = {
  type: [{ required: true, message: '请选择反馈类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入详细内容', trigger: 'blur' }]
}

function handleFileChange(file) {
    ElMessage.success(`已选择文件: ${file.name}`)
}

const submitForm = () => {
    formRef.value.validate((valid) => {
        if (valid) {
            ElMessage.success('反馈提交成功！我们将尽快处理。')
            resetForm()
        }
    })
}

const resetForm = () => {
    formRef.value.resetFields()
}
</script>
