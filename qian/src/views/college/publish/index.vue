<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane label="招生章程发布" name="brochure">
        <el-card>
            <el-form label-width="100px">
                <el-form-item label="章程标题">
                    <el-input v-model="brochure.title" placeholder="例如：2025年本科招生章程" />
                </el-form-item>
                <el-form-item label="发布年份">
                    <el-date-picker v-model="brochure.year" type="year" placeholder="选择年份" />
                </el-form-item>
                <el-form-item label="正文内容">
                   <div style="border: 1px solid #ccc; min-height: 300px;">
                      <!-- Placeholder for Quill Editor -->
                      <QuillEditor theme="snow" v-model:content="brochure.content" contentType="html" toolbar="full" />
                   </div>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handlePublishBrochure">发布章程</el-button>
                    <el-button @click="handleSaveDraft">保存草稿</el-button>
                </el-form-item>
            </el-form>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="分省分专业计划" name="plan">
         <el-card>
             <div style="margin-bottom: 20px;">
                 <el-select v-model="planFilter.province" placeholder="选择省份" style="width: 150px; margin-right: 10px;">
                    <el-option label="北京" value="北京" />
                    <el-option label="上海" value="上海" />
                    <el-option label="四川" value="四川" />
                 </el-select>
                 <el-button type="primary" icon="Plus" @click="handleAddPlan">新增计划</el-button>
                 <el-button type="success" icon="Upload" @click="handleImport">批量导入</el-button>
             </div>

             <el-table :data="planList" border>
                 <el-table-column prop="province" label="省份" width="100" />
                 <el-table-column prop="majorName" label="专业名称" />
                 <el-table-column prop="majorCode" label="专业代码" width="120" />
                 <el-table-column prop="subject" label="选考要求" width="150" />
                 <el-table-column prop="count" label="计划数" width="100">
                     <template #default="scope">
                         <el-input-number v-model="scope.row.count" size="small" :min="0" :max="999" />
                     </template>
                 </el-table-column>
                 <el-table-column prop="tuition" label="学费(元)" width="120" />
                 <el-table-column label="操作" width="120" align="center">
                     <template #default="scope">
                         <el-button type="danger" link icon="Delete" @click="handleDelete(scope.$index)">删除</el-button>
                     </template>
                 </el-table-column>
             </el-table>
             <div style="margin-top: 20px; text-align: center;">
                 <el-button type="primary" size="large" @click="handleSubmitPlans">提交计划审核</el-button>
             </div>
         </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog title="新增招生计划" v-model="dialogVisible" width="500px">
        <el-form :model="newPlan" label-width="100px">
            <el-form-item label="省份">
                 <el-select v-model="newPlan.province" style="width: 100%">
                    <el-option label="北京" value="北京" />
                    <el-option label="上海" value="上海" />
                    <el-option label="四川" value="四川" />
                 </el-select>
            </el-form-item>
            <el-form-item label="专业名称">
                <el-input v-model="newPlan.majorName" />
            </el-form-item>
             <el-form-item label="专业代码">
                <el-input v-model="newPlan.majorCode" />
            </el-form-item>
             <el-form-item label="计划数">
                <el-input-number v-model="newPlan.count" :min="1" />
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmAddPlan">确定</el-button>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="CollegePublish">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';

const activeName = ref('brochure')
const brochure = reactive({
    title: '',
    year: '',
    content: '<h2>2025年招生章程</h2><p>第一章 总则...</p>'
})

const planFilter = reactive({ province: '' })
const planList = ref([
    { province: '北京', majorName: '计算机科学与技术', majorCode: '080901', subject: '物理+化学', count: 15, tuition: 5000 },
    { province: '北京', majorName: '金融学', majorCode: '020301K', subject: '不限', count: 10, tuition: 5000 },
    { province: '四川', majorName: '临床医学', majorCode: '100201K', subject: '物理+化学+生物', count: 8, tuition: 6000 }
])

const dialogVisible = ref(false)
const newPlan = reactive({ province: '', majorName: '', majorCode: '', count: 1 })

function handlePublishBrochure() {
    ElMessage.success('招生章程已发布！')
}

function handleSaveDraft() {
    ElMessage.success('草稿已保存')
}

function handleAddPlan() {
    dialogVisible.value = true
}

function confirmAddPlan() {
    planList.value.push({ ...newPlan, subject: '待定', tuition: 5000 })
    dialogVisible.value = false
    ElMessage.success('添加成功')
}

function handleDelete(index) {
    planList.value.splice(index, 1)
}

function handleImport() {
    ElMessage.info('仅演示：已从Excel导入50条数据')
}

function handleSubmitPlans() {
    ElMessage.success('计划已提交至省招办审核！')
}
</script>
