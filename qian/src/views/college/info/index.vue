<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>院校基本信息维护</span>
          <el-button type="primary" @click="handleSubmit">保存更改</el-button>
        </div>
      </template>
      <el-form :model="form" label-width="120px">
        <el-form-item label="院校名称">
          <el-input v-model="form.name" disabled />
        </el-form-item>
        <el-form-item label="院校代码">
          <el-input v-model="form.code" disabled />
        </el-form-item>
        <el-form-item label="主管部门">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="办学层次">
           <el-select v-model="form.level">
               <el-option label="本科" value="本科" />
               <el-option label="高职(专科)" value="专科" />
           </el-select>
        </el-form-item>
        <el-form-item label="院校性质">
           <el-radio-group v-model="form.nature">
               <el-radio label="公办">公办</el-radio>
               <el-radio label="民办">民办</el-radio>
           </el-radio-group>
        </el-form-item>
        <el-form-item label="院校简介">
            <el-input v-model="form.description" type="textarea" :rows="6" />
        </el-form-item>
        <el-form-item label="校园风光">
           <el-upload
                action="#"
                list-type="picture-card"
                :auto-upload="false"
                :on-change="handleFileChange"
            >
                <el-icon><Plus /></el-icon>
            </el-upload>
            <div>（仅模拟上传，不实际保存文件）</div>
        </el-form-item>
        <el-form-item label="联系电话">
            <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="学校官网">
            <el-input v-model="form.website" />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup name="CollegeInfo">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
    name: '北京大学',
    code: '10001',
    department: '教育部',
    level: '本科',
    nature: '公办',
    description: '北京大学创办于1898年，初名京师大学堂，是中国第一所国立综合性大学...',
    phone: '010-62751407',
    website: 'https://www.pku.edu.cn'
})

function handleFileChange(file) {
    ElMessage.success(`已选择图片: ${file.name}`)
}

function handleSubmit() {
    ElMessage.success('院校信息已更新')
}
</script>
