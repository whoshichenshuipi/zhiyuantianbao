<template>
  <div class="app-container">
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card>
                <template #header><span>平台用户增长趋势</span></template>
                <div id="lineChart" style="height: 350px;"></div>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card>
                <template #header><span>考生地域分布热力图</span></template>
                <div id="mapChart" style="height: 350px;"></div>
            </el-card>
        </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
         <el-col :span="12">
            <el-card>
                <template #header><span>志愿填报热门专业TOP10</span></template>
                <div id="barChart" style="height: 350px;"></div>
            </el-card>
        </el-col>
         <el-col :span="12">
            <el-card>
                <template #header><span>系统访问终端占比</span></template>
                <div id="pieChart" style="height: 350px;"></div>
            </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<script setup name="StatsAnalysis">
import * as echarts from 'echarts'
import { onMounted } from 'vue'

onMounted(() => {
    initLineChart()
    initMapChart()
    initBarChart()
    initPieChart()
})

function initLineChart() {
    const myChart = echarts.init(document.getElementById('lineChart'))
    myChart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: ['5月1日', '5月2日', '5月3日', '5月4日', '5月5日', '5月6日', '5月7日'] },
        yAxis: { type: 'value' },
        series: [{ data: [150, 230, 224, 218, 135, 147, 260], type: 'line', smooth: true }]
    })
}

function initMapChart() {
    const myChart = echarts.init(document.getElementById('mapChart'))
    myChart.setOption({
        tooltip: { trigger: 'item' },
        visualMap: { min: 0, max: 2000, left: 'left', top: 'bottom', text: ['高', '低'], calculable: true },
         series: [
            {
                name: '考生人数',
                type: 'map',
                mapType: 'china', // Note: Need to register china map separately in real project, here just mock config structure
                label: { show: false },
                data: [
                    { name: '北京', value: 1560 },
                    { name: '四川', value: 1890 },
                    { name: '上海', value: 1200 },
                     { name: '广东', value: 2100 }
                ]
            }
        ]
    })
    // Mocking map since we don't have map json imported
    myChart.setOption({
          title: { text: '因缺少地图JSON数据，此处仅展示模拟饼图替代', left: 'center', top: 'center', textStyle: { color: '#999' } }
    }, true)
}

function initBarChart() {
     const myChart = echarts.init(document.getElementById('barChart'))
    myChart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: { type: 'category', data: ['临床医学', '法学', '汉语言文学', '软件工程', '会计学', '电气工程', '计算机'] },
        series: [{ name: '填报人数', type: 'bar', data: [18203, 23489, 29034, 104970, 131744, 630230, 720102] }]
    })
}

function initPieChart() {
     const myChart = echarts.init(document.getElementById('pieChart'))
    myChart.setOption({
        tooltip: { trigger: 'item' },
        legend: { top: '5%', left: 'center' },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
                 data: [
                    { value: 1048, name: 'PC端 Web' },
                    { value: 735, name: '移动端 H5' },
                    { value: 580, name: '微信小程序' }
                ]
            }
        ]
    })
}
</script>
