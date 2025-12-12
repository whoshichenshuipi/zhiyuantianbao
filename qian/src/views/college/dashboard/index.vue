<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header>
               <div class="card-header">
                   <span>计划完成率</span>
                   <el-tag type="success">实时</el-tag>
               </div>
           </template>
           <div class="data-item">
               <span class="num">98%</span>
               <span class="desc">已录取 / 计划数</span>
           </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header>
               <div class="card-header">
                   <span>今日咨询量</span>
                   <el-tag type="warning">热度</el-tag>
               </div>
           </template>
           <div class="data-item">
               <span class="num">1,250</span>
               <span class="desc">人次</span>
           </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header>
               <div class="card-header">
                   <span>意向收藏数</span>
                   <el-tag>总计</el-tag>
               </div>
           </template>
           <div class="data-item">
               <span class="num">8,900</span>
               <span class="desc">加入志愿备选</span>
           </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header>
               <div class="card-header">
                   <span>平均分(预估)</span>
                   <el-tag type="danger">分析</el-tag>
               </div>
           </template>
           <div class="data-item">
               <span class="num">655</span>
               <span class="desc">理科平均分</span>
           </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12">
            <el-card>
                <template #header><span>生源省份分布</span></template>
                <div id="mapChart" style="height: 400px;"></div>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card>
                <template #header><span>各专业咨询热度TOP5</span></template>
                <div id="barChart" style="height: 400px;"></div>
            </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<script setup name="CollegeDashboard">
import * as echarts from 'echarts'
import { onMounted } from 'vue'

onMounted(() => {
    initMapChart()
    initBarChart()
})

function initMapChart() {
    const chartDom = document.getElementById('mapChart')
    const myChart = echarts.init(chartDom)
    const option = {
        tooltip: { trigger: 'item' },
        series: [
            {
                name: '生源数',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: { show: false, position: 'center' },
                emphasis: {
                    label: { show: true, fontSize: 20, fontWeight: 'bold' }
                },
                labelLine: { show: false },
                data: [
                    { value: 1048, name: '北京' },
                    { value: 735, name: '上海' },
                    { value: 580, name: '江苏' },
                    { value: 484, name: '浙江' },
                    { value: 300, name: '其他' }
                ]
            }
        ]
    }
    myChart.setOption(option)
}

function initBarChart() {
    const chartDom = document.getElementById('barChart')
    const myChart = echarts.init(chartDom)
    const option = {
         tooltip: { trigger: 'axis' },
        xAxis: {
            type: 'category',
            data: ['计算机', '金融学', '临床医学', '法学', '汉语言']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: [1200, 900, 850, 600, 400],
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                },
                 itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#83bff6' },
                        { offset: 0.5, color: '#188df0' },
                        { offset: 1, color: '#188df0' }
                    ])
                }
            }
        ]
    }
    myChart.setOption(option)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.data-item {
    text-align: center;
    padding: 10px 0;
}
.num {
    display: block;
    font-size: 28px;
    font-weight: bold;
    color: #409EFF;
}
.desc {
    color: #909399;
    font-size: 14px;
}
</style>
