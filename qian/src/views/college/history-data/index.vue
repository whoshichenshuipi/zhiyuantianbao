<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams" class="demo-form-inline">
      <el-form-item label="年份">
         <el-date-picker v-model="queryParams.year" type="year" placeholder="选择年份" value-format="YYYY" style="width: 150px" />
      </el-form-item>
      <el-form-item label="省份">
        <el-select v-model="queryParams.province" placeholder="省份" clearable style="width: 150px">
           <el-option label="北京" value="北京" />
           <el-option label="上海" value="上海" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">查询</el-button>
        <el-button type="success" icon="Top" @click="handleImport">导入Excel</el-button>
        <el-button type="primary" plain icon="Plus" @click="handleAdd">新增一条</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="dataList" border style="width: 100%">
      <el-table-column prop="year" label="年份" width="100" />
      <el-table-column prop="province" label="省份" width="100" />
      <el-table-column prop="batch" label="批次" width="120" />
      <el-table-column prop="major" label="专业名称" />
      <el-table-column prop="scoreLine" label="投档线" width="100" />
      <el-table-column prop="minRank" label="最低位次" width="100" />
      <el-table-column label="操作" width="150" align="center">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(scope.$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="title" v-model="open" width="500px">
        <el-form :model="form" label-width="80px">
            <el-form-item label="年份">
                <el-input v-model="form.year" />
            </el-form-item>
             <el-form-item label="省份">
                <el-input v-model="form.province" />
            </el-form-item>
             <el-form-item label="专业">
                <el-input v-model="form.major" />
            </el-form-item>
             <el-form-item label="投档线">
                <el-input v-model="form.scoreLine" />
            </el-form-item>
            <el-form-item label="最低位次">
                <el-input v-model="form.minRank" />
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

<script setup name="HistoryData">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const queryParams = reactive({
    year: '2023',
    province: ''
})
const title = ref('')
const open = ref(false)
const form = reactive({})

const dataList = ref([
    { year: '2023', province: '北京', batch: '本科提前批', major: '马克思主义理论', scoreLine: 658, minRank: 2300 },
    { year: '2023', province: '北京', batch: '本科普通批', major: '计算机类', scoreLine: 672, minRank: 1200 },
    { year: '2023', province: '上海', batch: '本科普通批', major: '经济管理试验班', scoreLine: 580, minRank: 1500 },
    { year: '2022', province: '北京', batch: '本科普通批', major: '计算机类', scoreLine: 669, minRank: 1250 }
])

function handleQuery() {
    ElMessage.success('查询成功')
}

function handleImport() {
    ElMessage.info('Mock: 导入窗口已打开')
}

function handleAdd() {
    title.value = '新增历史数据'
    open.value = true
    Object.assign(form, { year: '2024', province: '', major: '', scoreLine: '' })
}

function handleEdit(row) {
    title.value = '编辑历史数据'
    open.value = true
    Object.assign(form, row)
}

function handleDelete(index) {
     ElMessageBox.confirm('确认删除该条数据吗?', '提示', { type: 'warning' })
     .then(() => {
         dataList.value.splice(index, 1)
         ElMessage.success('删除成功')
     }).catch(()=>{})
}

function submitForm() {
    open.value = false
    ElMessage.success('操作成功')
}
</script>
