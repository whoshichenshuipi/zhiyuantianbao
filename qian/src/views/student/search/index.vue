<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" label-width="68px">
      <el-form-item label="院校名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入院校名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="所属地区" prop="location">
        <el-select v-model="queryParams.location" placeholder="请选择地区" clearable style="width: 240px">
          <el-option label="北京" value="北京" />
          <el-option label="上海" value="上海" />
          <el-option label="江苏" value="江苏" />
          <el-option label="湖北" value="湖北" />
        </el-select>
      </el-form-item>
       <el-form-item label="院校层次" prop="level">
        <el-select v-model="queryParams.level" placeholder="请选择层次" clearable style="width: 240px">
          <el-option label="双一流" value="双一流" />
          <el-option label="985" value="985" />
          <el-option label="211" value="211" />
          <el-option label="普通本科" value="普通本科" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="collegeList" border>
      <el-table-column label="排名" align="center" prop="rank" width="80" />
      <el-table-column label="院校名称" align="center" prop="name" :show-overflow-tooltip="true">
        <template #default="scope">
           <span style="font-weight: bold; color: #409EFF; cursor: pointer" @click="handleView(scope.row)">{{ scope.row.name }}</span>
           <el-tag size="small" type="danger" v-if="scope.row.tags.includes('985')" style="margin-left:5px">985</el-tag>
           <el-tag size="small" type="primary" v-if="scope.row.tags.includes('211')" style="margin-left:5px">211</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="所在地" align="center" prop="location" width="100" />
      <el-table-column label="院校类型" align="center" prop="type" width="100" />
      <el-table-column label="招生计划" align="center" prop="planCount" width="100" />
      <el-table-column label="最低投档分(去年)" align="center" prop="minScore" width="150" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            link
            type="primary"
            icon="View"
            @click="handleView(scope.row)"
          >详情</el-button>
          <el-button
            link
            type="success"
            icon="Plus"
            @click="handleAddPlan(scope.row)"
          >加入备选</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 详情弹窗 -->
    <el-dialog :title="detailTitle" v-model="open" width="700px" append-to-body>
        <div v-if="currentCollege" style="padding: 0 20px;">
            <div style="display:flex; align-items:center; margin-bottom: 20px;">
                 <div style="width: 80px; height: 80px; background: #f0f0f0; border-radius: 50%; display:flex; align-items:center; justify-content:center; margin-right: 20px;">
                    LOGO
                 </div>
                 <div>
                     <h2 style="margin:0">{{ currentCollege.name }}</h2>
                     <p style="color: #666; margin: 5px 0">{{ currentCollege.location }} | {{ currentCollege.type }} | 隶属: 教育部</p>
                     <div>
                        <el-tag v-for="tag in currentCollege.tags" :key="tag" style="margin-right:5px">{{ tag }}</el-tag>
                     </div>
                 </div>
            </div>
            
            <el-tabs type="border-card">
                <el-tab-pane label="学校简介">
                    <p style="line-height:1.8">
                        {{ currentCollege.name }} 是一所历史悠久、声誉卓著的高等学府。学校坐落于{{ currentCollege.location }}，
                        拥有完善的教学设施和强大的师资力量。
                        （此处为Mock数据，实际将显示学校详细介绍）
                    </p>
                </el-tab-pane>
                <el-tab-pane label="开设专业">
                    <el-table :data="mockMajors" style="width: 100%">
                        <el-table-column prop="name" label="专业名称" />
                        <el-table-column prop="category" label="门类" width="100" />
                        <el-table-column prop="year" label="修业年限" width="100" />
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="历年分数">
                    <div style="height: 200px; display:flex; align-items:center; justify-content:center; color:#999;">
                        ECharts 图表区域 (历年最高/平均/最低分走势)
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="open = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="CollegeSearch">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const total = ref(0)
const open = ref(false)
const detailTitle = ref("院校详情")
const currentCollege = ref(null)

const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  name: undefined,
  location: undefined,
  level: undefined
})

// Mock Data
const collegeList = ref([
    { id: 1, name: '北京大学', rank: 1, location: '北京', type: '综合类', tags: ['985', '211', '双一流'], planCount: 3500, minScore: 680 },
    { id: 2, name: '清华大学', rank: 2, location: '北京', type: '理工类', tags: ['985', '211', '双一流'], planCount: 3400, minScore: 681 },
    { id: 3, name: '复旦大学', rank: 3, location: '上海', type: '综合类', tags: ['985', '211', '双一流'], planCount: 3600, minScore: 675 },
    { id: 4, name: '上海交通大学', rank: 4, location: '上海', type: '理工类', tags: ['985', '211', '双一流'], planCount: 3700, minScore: 676 },
    { id: 5, name: '浙江大学', rank: 5, location: '浙江', type: '综合类', tags: ['985', '211', '双一流'], planCount: 6000, minScore: 668 },
    { id: 6, name: '南京大学', rank: 6, location: '江苏', type: '综合类', tags: ['985', '211', '双一流'], planCount: 3300, minScore: 665 },
    { id: 7, name: '武汉大学', rank: 9, location: '湖北', type: '综合类', tags: ['985', '211', '双一流'], planCount: 7000, minScore: 650 },
    { id: 8, name: '华中科技大学', rank: 10, location: '湖北', type: '理工类', tags: ['985', '211', '双一流'], planCount: 7200, minScore: 648 },
])

const mockMajors = [
    { name: '计算机科学与技术', category: '工学', year: '4年' },
    { name: '软件工程', category: '工学', year: '4年' },
    { name: '金融学', category: '经济学', year: '4年' },
    { name: '临床医学', category: '医学', year: '5年' }
]

total.value = 8

function getList() {
  loading.value = true;
  // Simulate API delay
  setTimeout(() => {
    loading.value = false;
  }, 300);
}

function handleQuery() {
  queryParams.pageNum = 1;
  getList();
}

function resetQuery() {
  // reset fields
  handleQuery();
}

function handleView(row) {
    currentCollege.value = row
    detailTitle.value = row.name + " - 详情"
    open.value = true
}

function handleAddPlan(row) {
    ElMessage.success("已将 " + row.name + " 加入志愿备选库")
}

getList()
</script>
