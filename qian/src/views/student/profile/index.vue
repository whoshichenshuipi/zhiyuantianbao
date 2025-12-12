<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>个人信息与志愿偏好</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考生号" prop="candidateId">
              <el-input v-model="form.candidateId" placeholder="请输入考生号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="高考分数" prop="score">
              <el-input-number v-model="form.score" :min="0" :max="750" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="全省排名" prop="rank">
              <el-input-number v-model="form.rank" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">志愿偏好设置</el-divider>

        <el-form-item label="兴趣爱好" prop="interests">
          <el-checkbox-group v-model="form.interests">
            <el-checkbox label="计算机/互联网" />
            <el-checkbox label="金融/经济" />
            <el-checkbox label="医学/护理" />
            <el-checkbox label="教育/培训" />
            <el-checkbox label="艺术/设计" />
            <el-checkbox label="机械/制造" />
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="地域偏好" prop="regions">
          <el-select
            v-model="form.regions"
            multiple
            placeholder="请选择意向省份(可多选)"
            style="width: 100%"
          >
            <el-option label="北京市" value="beijing" />
            <el-option label="上海市" value="shanghai" />
            <el-option label="江苏省" value="jiangsu" />
            <el-option label="浙江省" value="zhejiang" />
            <el-option label="广东省" value="guangdong" />
            <el-option label="四川省" value="sichuan" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="专业类型偏好" prop="majorTypes">
           <el-radio-group v-model="form.majorTypes">
              <el-radio label="engineering">理工类</el-radio>
              <el-radio label="liberal_arts">文史类</el-radio>
              <el-radio label="comprehensive">综合类</el-radio>
              <el-radio label="art">艺术类</el-radio>
           </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">保存信息</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup name="StudentProfile">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const formRef = ref(null)

const form = reactive({
  name: '考生张三',
  candidateId: '230101200508081234',
  score: 620,
  rank: 12500,
  interests: ['计算机/互联网'],
  regions: ['beijing', 'shanghai'],
  majorTypes: 'engineering'
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  candidateId: [{ required: true, message: '请输入考生号', trigger: 'blur' }],
  score: [{ required: true, message: '请输入高考分数', trigger: 'blur' }],
  regions: [{ required: true, message: '请选择地域偏好', trigger: 'change' }]
}

const submitForm = () => {
    formRef.value.validate((valid) => {
        if (valid) {
            // Mock submission
            setTimeout(() => {
                ElMessage.success('个人信息保存成功！')
            }, 500)
        }
    })
}

const resetForm = () => {
    formRef.value.resetFields()
}
</script>

<style scoped>
.box-card {
  width: 100%;
}
</style>
