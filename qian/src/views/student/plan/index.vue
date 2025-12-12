<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的志愿方案 (模拟填报)</span>
          <div>
              <el-button type="primary" @click="handleSubmit">生成正式志愿表</el-button>
              <el-button type="warning" plain @click="handleExport">导出预览</el-button>
          </div>
        </div>
      </template>

      <el-alert
        title="温馨提示：请按照 A-H 顺序排列您的志愿，平行志愿录取遵循'分数优先、遵循志愿'原则。"
        type="info"
        show-icon
        style="margin-bottom: 20px"
      />

      <el-table :data="planList" border style="width: 100%">
        <el-table-column label="志愿顺序" width="100" align="center">
            <template #default="scope">
                <el-tag effect="dark" type="danger" v-if="scope.$index < 3">志愿 {{ String.fromCharCode(65 + scope.$index) }}</el-tag>
                <el-tag effect="plain" v-else>志愿 {{ String.fromCharCode(65 + scope.$index) }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="name" label="院校名称" width="220" />
        <el-table-column prop="code" label="院校代码" width="100" />
        <el-table-column prop="major" label="专业名称" />
        <el-table-column prop="majorCode" label="专业代码" width="100" />
        <el-table-column label="调整排序" width="180" align="center">
          <template #default="scope">
            <el-button size="small" icon="Top" circle @click="moveUp(scope.$index)" :disabled="scope.$index === 0" />
            <el-button size="small" icon="Bottom" circle @click="moveDown(scope.$index)" :disabled="scope.$index === planList.length - 1" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template #default="scope">
            <el-button size="small" type="danger" icon="Delete" circle @click="handleDelete(scope.$index, scope.row)" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup name="VolunteerPlan">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const planList = ref([
    { name: '清华大学', code: '10003', major: '计算机科学与技术', majorCode: '080901' },
    { name: '北京大学', code: '10001', major: '数学与应用数学', majorCode: '070101' },
    { name: '复旦大学', code: '10246', major: '金融学', majorCode: '020301K' },
    { name: '上海交通大学', code: '10248', major: '电子信息工程', majorCode: '080701' },
    { name: '浙江大学', code: '10335', major: '数字媒体技术', majorCode: '080906' }
])

function moveUp(index) {
    if (index > 0) {
        const item = planList.value.splice(index, 1)[0]
        planList.value.splice(index - 1, 0, item)
    }
}

function moveDown(index) {
    if (index < planList.value.length - 1) {
        const item = planList.value.splice(index, 1)[0]
        planList.value.splice(index + 1, 0, item)
    }
}

function handleDelete(index, row) {
    ElMessageBox.confirm('确认要移除该志愿吗?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        planList.value.splice(index, 1)
        ElMessage.success('移除成功')
    }).catch(() => {})
}

function handleSubmit() {
    ElMessageBox.alert('模拟提交成功！在正式系统中，您还需要输入动态口令进行最终确认。', '系统提示', {
        confirmButtonText: '我知道了'
    })
}

function handleExport() {
    ElMessage.success('正在导出志愿表 PDF...')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
