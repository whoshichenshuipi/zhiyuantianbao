<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header><span>注册考生总数</span></template>
           <div class="num">125,800</div>
           <div class="desc">今日新增 +230</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
           <template #header><span>入驻高校数</span></template>
           <div class="num">2,450</div>
           <div class="desc">今日审核 +5</div>
        </el-card>
      </el-col>
       <el-col :span="6">
        <el-card shadow="hover">
           <template #header><span>待审核计划</span></template>
           <div class="num" style="color:red">15</div>
           <div class="desc">急需处理</div>
        </el-card>
      </el-col>
       <el-col :span="6">
        <el-card shadow="hover">
           <template #header><span>系统访问量(PV)</span></template>
           <div class="num">1,200,890</div>
           <div class="desc">实时监控</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top:20px;">
        <el-col :span="16">
            <el-card>
                <template #header><span>近7日流量趋势</span></template>
                <div id="chart" style="height: 350px;"></div>
            </el-card>
        </el-col>
         <el-col :span="8">
            <el-card>
                <template #header><span>系统公告</span></template>
                <el-timeline>
                    <el-timeline-item timestamp="2025-05-12" placement="top">
                        <el-card>
                            <h4>系统升级通知</h4>
                            <p>将于今晚 24:00 进行停机维护。</p>
                        </el-card>
                    </el-timeline-item>
                    <el-timeline-item timestamp="2025-05-10" placement="top">
                        <el-card>
                            <h4>考生数据导入完成</h4>
                            <p>已完成全省考生基础数据同步。</p>
                        </el-card>
                    </el-timeline-item>
                </el-timeline>
            </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<script setup name="AdminDashboard">
import * as echarts from 'echarts'
import { onMounted } from 'vue'

onMounted(() => {
    initChart()
})

function initChart() {
    const chartDom = document.getElementById('chart')
    const myChart = echarts.init(chartDom)
     const option = {
        tooltip: { trigger: 'axis' },
        xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                type: 'line',
                smooth: true,
                areaStyle: {}
            }
        ]
    }
    myChart.setOption(option)
}
</script>

<style scoped>
.num {
    font-size: 32px;
    font-weight: bold;
    color: #303133;
    margin: 10px 0;
}
.desc {
    color: #909399;
    font-size: 14px;
}
</style>
