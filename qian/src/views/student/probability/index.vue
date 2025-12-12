<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>录取概率测算</span>
        </div>
      </template>
      
      <el-form :inline="true" :model="form" class="demo-form-inline">
        <el-form-item label="目标院校">
          <el-select v-model="form.college" placeholder="请选择院校" filterable>
            <el-option label="北京大学" value="pku" />
            <el-option label="清华大学" value="thu" />
            <el-option label="复旦大学" value="fudan" />
            <el-option label="浙江大学" value="zju" />
          </el-select>
        </el-form-item>
        <el-form-item label="目标专业">
          <el-select v-model="form.major" placeholder="请选择专业">
            <el-option label="计算机科学与技术" value="cs" />
            <el-option label="金融学" value="finance" />
            <el-option label="临床医学" value="medicine" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCalculate">开始测算</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.show" style="margin-top: 30px; text-align: center;">
          <el-row>
              <el-col :span="12">
                   <div id="gaugeChart" style="height: 350px;"></div>
              </el-col>
              <el-col :span="12" style="text-align: left; padding-top: 50px;">
                  <h3>测算结果分析：</h3>
                  <p><strong>录取概率：</strong> <span style="font-size: 24px; color: #E6A23C">{{ result.prob }}%</span></p>
                  <p><strong>风险评估：</strong> <el-tag :type="result.riskType">{{ result.riskLabel }}</el-tag></p>
                  <p><strong>历年分差：</strong> 平均分差 {{ result.diff }} 分</p>
                  <el-alert title="建议：该院校对您来说属于冲刺型，建议将其放在志愿表的前列，作为冲一冲的选择。" type="warning" :closable="false" />
              </el-col>
          </el-row>
      </div>
    </el-card>

    <el-card style="margin-top: 20px">
        <template #header>
            <span>同分段考生去向 (大数据参考)</span>
        </template>
        <el-table :data="historyData" style="width: 100%">
            <el-table-column prop="year" label="年份" />
            <el-table-column prop="college" label="录取院校" />
            <el-table-column prop="major" label="录取专业" />
            <el-table-column prop="score" label="录取分数" />
        </el-table>
    </el-card>
  </div>
</template>

<script setup name="Probability">
import * as echarts from 'echarts'
import { ref, reactive, nextTick } from 'vue'
import { ElLoading } from 'element-plus'

const form = reactive({
  college: '',
  major: ''
})

const result = reactive({
    show: false,
    prob: 0,
    riskLabel: '',
    riskType: '',
    diff: 0
})

const historyData = [
    { year: '2023', college: '同济大学', major: '土木工程', score: 622 },
    { year: '2023', college: '南开大学', major: '经济学', score: 620 },
    { year: '2022', college: '武汉大学', major: '测绘工程', score: 618 },
    { year: '2022', college: '厦门大学', major: '会计学', score: 619 },
]

function handleCalculate() {
    if(!form.college || !form.major) {
        return;
    }
    constloadingInstance = ElLoading.service({ text: '正在进行大数据分析...', background: 'rgba(0, 0, 0, 0.7)' })
    setTimeout(() => {
        constloadingInstance.close()
        result.show = true
        result.prob = 68
        result.riskLabel = '较为稳妥'
        result.riskType = 'warning'
        result.diff = 5
        
        nextTick(() => {
            initChart()
        })
    }, 1500)
}

function initChart() {
    const chartDom = document.getElementById('gaugeChart')
    const myChart = echarts.init(chartDom)
    const option = {
        series: [
            {
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: 100,
                splitNumber: 10,
                axisLine: {
                    lineStyle: {
                        width: 6,
                        color: [
                            [0.3, '#F56C6C'],
                            [0.7, '#E6A23C'],
                            [1, '#67C23A']
                        ]
                    }
                },
                pointer: {
                    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    length: '12%',
                    width: 20,
                    offsetCenter: [0, '-60%'],
                    itemStyle: {
                    color: 'auto'
                    }
                },
                axisTick: {
                    length: 12,
                    lineStyle: {
                    color: 'auto',
                    width: 2
                    }
                },
                splitLine: {
                    length: 20,
                    lineStyle: {
                    color: 'auto',
                    width: 5
                    }
                },
                axisLabel: {
                    color: '#464646',
                    fontSize: 20,
                    distance: -60,
                    formatter: function (value) {
                        if (value === 90) {
                            return '稳';
                        } else if (value === 50) {
                            return '中';
                        } else if (value === 10) {
                            return '险';
                        }
                        return '';
                    }
                },
                title: {
                    offsetCenter: [0, '-20%'],
                    fontSize: 30
                },
                detail: {
                    fontSize: 50,
                    offsetCenter: [0, '0%'],
                    valueAnimation: true,
                    formatter: function (value) {
                    return Math.round(value) + '%';
                    },
                    color: 'auto'
                },
                data: [
                    {
                    value: result.prob,
                    name: '录取概率'
                    }
                ]
            }
        ]
    };
    myChart.setOption(option)
}
</script>
