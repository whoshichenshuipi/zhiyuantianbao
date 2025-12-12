<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="24" :md="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>智能分析报告</span>
              <el-tag type="success">AI 驱动</el-tag>
            </div>
          </template>
          <div class="text item">
            <p>考生：张三 (620分 / 理科)</p>
            <p>全省排名：12,500</p>
            <div id="riskChart" style="height: 300px;"></div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24" :md="16">
        <el-tabs type="border-card">
          <el-tab-pane label="冲刺院校 (风险高)">
             <el-table :data="recommendList.aggressive" style="width: 100%">
               <el-table-column prop="name" label="院校名称" />
               <el-table-column prop="prob" label="录取概率" width="100">
                  <template #default="scope">
                     <el-tag type="danger">{{ scope.row.prob }}%</el-tag>
                  </template>
               </el-table-column>
               <el-table-column prop="diff" label="分差" width="100">
                   <template #default="scope">
                     <span style="color:red">-{{ scope.row.diff }}</span>
                  </template>
               </el-table-column>
               <el-table-column label="操作" width="100">
                 <template #default="scope">
                   <el-button link type="primary" @click="handleAddToPlan(scope.row)">填报</el-button>
                 </template>
               </el-table-column>
             </el-table>
          </el-tab-pane>
          <el-tab-pane label="稳妥院校 (机会大)">
             <el-table :data="recommendList.moderate" style="width: 100%">
               <el-table-column prop="name" label="院校名称" />
               <el-table-column prop="prob" label="录取概率" width="100">
                  <template #default="scope">
                     <el-tag type="warning">{{ scope.row.prob }}%</el-tag>
                  </template>
               </el-table-column>
                <el-table-column prop="diff" label="分差" width="100">
                   <template #default="scope">
                     <span style="color:orange">{{ scope.row.diff > 0 ? '+' : '' }}{{ scope.row.diff }}</span>
                  </template>
               </el-table-column>
               <el-table-column label="操作" width="100">
                 <template #default="scope">
                   <el-button link type="primary" @click="handleAddToPlan(scope.row)">填报</el-button>
                 </template>
               </el-table-column>
             </el-table>
          </el-tab-pane>
          <el-tab-pane label="保底院校 (极稳)">
             <el-table :data="recommendList.safe" style="width: 100%">
               <el-table-column prop="name" label="院校名称" />
               <el-table-column prop="prob" label="录取概率" width="100">
                  <template #default="scope">
                     <el-tag type="success">{{ scope.row.prob }}%</el-tag>
                  </template>
               </el-table-column>
               <el-table-column prop="diff" label="分差" width="100">
                   <template #default="scope">
                     <span style="color:green">+{{ scope.row.diff }}</span>
                  </template>
               </el-table-column>
               <el-table-column label="操作" width="100">
                 <template #default="scope">
                   <el-button link type="primary" @click="handleAddToPlan(scope.row)">填报</el-button>
                 </template>
               </el-table-column>
             </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="Recommend">
import * as echarts from 'echarts'
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const recommendList = reactive({
    aggressive: [
        { name: '北京理工大学', prob: 30, diff: 5 },
        { name: '南开大学', prob: 35, diff: 3 },
        { name: '同济大学', prob: 25, diff: 8 }
    ],
    moderate: [
        { name: '厦门大学', prob: 65, diff: 2 },
        { name: '天津大学', prob: 70, diff: 5 },
        { name: '四川大学', prob: 75, diff: 8 }
    ],
    safe: [
        { name: '吉林大学', prob: 95, diff: 15 },
        { name: '中南大学', prob: 98, diff: 18 },
        { name: '湖南大学', prob: 96, diff: 16 }
    ]
})

function handleAddToPlan(row) {
    ElMessage.success(`已将 ${row.name} 加入模拟志愿表`)
}

onMounted(() => {
    const chartDom = document.getElementById('riskChart')
    const myChart = echarts.init(chartDom)
    const option = {
        title: {
            text: '录取概率分布',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
             top: 'bottom'
        },
        series: [
            {
                name: '概率分析',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: 20, name: '冲刺 (High Risk)' },
                    { value: 50, name: '稳妥 (Medium)' },
                    { value: 30, name: '保底 (Low Risk)' }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    myChart.setOption(option)
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
