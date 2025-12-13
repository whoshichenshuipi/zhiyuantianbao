<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>招生快讯与政策解读</span>
              <el-input 
                v-model="searchKeyword" 
                placeholder="搜索感兴趣的内容..." 
                prefix-icon="Search"
                style="width: 250px" 
              />
            </div>
          </template>
          
          <div class="news-list">
             <div v-for="item in newsList" :key="item.news_id || item.id" class="news-item" @click="handleDetail(item)">
                <div class="news-title">
                    <el-tag size="small" :type="getCategoryType(item.category)">{{ item.category }}</el-tag>
                    <span class="title-text">{{ item.title }}</span>
                </div>
                <div class="news-meta">
                    <span>{{ item.college || '官方' }}</span>
                    <span>{{ item.publish_time || item.time }}</span>
                </div>
             </div>
          </div>
          
          <el-pagination
            background
            layout="prev, pager, next"
            :total="100"
            class="pagination"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
          <el-card>
             <template #header><span>热门资讯排行榜</span></template>
             <div v-for="(item, index) in hotNews" :key="index" class="hot-item" @click="handleDetail(item)">
                 <span class="index" :class="{ top3: index < 3 }">{{ index + 1 }}</span>
                 <span class="text">{{ item.title }}</span>
             </div>
          </el-card>
          
          <el-card style="margin-top: 20px">
              <template #header><span>相关推荐</span></template>
               <div style="font-size: 14px; color: #666; line-height: 1.8;">
                   <p>如何填报平行志愿？</p>
                   <p>2025年强基计划报考指南</p>
                   <p>双一流高校专业解读</p>
               </div>
          </el-card>
      </el-col>
    </el-row>

    <el-dialog :title="currentNews.title" v-model="open" width="800px">
        <div v-if="currentNews" class="news-detail">
            <div class="detail-meta">
                <span>发布高校：{{ currentNews.college }}</span>
                <span>发布时间：{{ currentNews.time }}</span>
                <span class="read-count">阅读量：{{ Math.floor(Math.random() * 1000) + 100 }}</span>
            </div>
            <el-divider />
            <div class="detail-content">
                <p>（这里是 Mock 的资讯详情内容）</p>
                <p>为全面贯彻落实党的教育方针，探索多维度考核评价模式，选拔一批有志向、有兴趣、有天赋的青年学生进行专门培养，为国家重大战略领域输送后备人才，根据教育部关于在部分高校开展基础学科招生改革试点工作的意见等文件精神，我校2025年继续开展基础学科招生改革试点（也称强基计划）招生工作。</p>
                <p><strong>一、招生对象及报名条件</strong></p>
                <p>符合2025年全国普通高等学校招生全国统一考试报名条件，综合素质优秀或基础学科拔尖，并有志于将来从事相关领域科学技术工作的高中毕业生均可申请。</p>
                <img src="https://via.placeholder.com/600x300?text=News+Image+Placeholder" style="max-width: 100%; border-radius: 4px; margin: 10px 0;" />
                <p>申请考生分为以下两类......</p>
            </div>
        </div>
    </el-dialog>
  </div>
</template>

<script setup name="StudentNews">
import { ref, onMounted } from 'vue'
import { listNews, getNews } from '@/api/student/news'

const searchKeyword = ref('')
const open = ref(false)
const currentNews = ref({})
const loading = ref(false)
const total = ref(0)
const queryParams = ref({
  page: 1,
  pageSize: 10
})

const newsList = ref([])

const hotNews = ref([
    { title: '教育部发布2025年普通高校招生工作规定' },
    { title: '全国39所强基计划试点高校简章汇总' },
    { title: '新高考改革省份志愿填报重难点解析' },
    { title: '计算机专业就业前景分析报告' },
    { title: '医学类专业报考指南' }
])

/** 查询资讯列表 */
function getList() {
    loading.value = true
    listNews(queryParams.value).then(response => {
        if (response.code === 0) {
            newsList.value = response.data.rows || []
            total.value = response.data.total || 0
        }
        loading.value = false
    }).catch(() => {
        loading.value = false
        // 如果API调用失败，使用mock数据
        newsList.value = [
            { news_id: 1, title: '北京大学2025年强基计划招生简章', category: '招生快讯', college: '北京大学', publish_time: '2025-05-12' },
            { news_id: 2, title: '清华大学2025年自强计划启动', category: '政策解读', college: '清华大学', publish_time: '2025-05-11' },
            { news_id: 3, title: '复旦大学校园开放日活动预告', category: '校园新闻', college: '复旦大学', publish_time: '2025-05-10' },
        ]
    })
}

function getCategoryType(category) {
    const map = {
        '招生快讯': 'danger',
        '政策解读': 'primary',
        '校园新闻': 'success',
        '学科动态': 'warning'
    }
    return map[category] || 'info'
}

function handleDetail(item) {
    currentNews.value = item
    open.value = true
}

onMounted(() => {
    getList()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.news-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}
.news-item:hover {
    background-color: #fafafa;
}
.news-title {
    display: flex;
    align-items: center;
    gap: 10px;
}
.title-text {
    font-size: 16px;
    color: #333;
}
.news-meta {
    font-size: 13px;
    color: #999;
    display: flex;
    gap: 15px;
}
.pagination {
    margin-top: 20px;
    text-align: center;
}

.hot-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    cursor: pointer;
}
.hot-item:hover .text {
    color: #409EFF;
}
.index {
    display: inline-block;
    width: 20px;
    height: 20px;
    line-height: 20px;
    text-align: center;
    background: #f0f2f5;
    color: #666;
    margin-right: 10px;
    border-radius: 4px;
    font-size: 12px;
}
.index.top3 {
    background: #ff7675;
    color: #fff;
}
.text {
    font-size: 14px;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.detail-meta {
    display: flex;
    gap: 20px;
    color: #999;
    font-size: 13px;
    justify-content: center;
    margin-bottom: 15px;
}
.detail-content {
    line-height: 1.8;
    color: #333;
    font-size: 15px;
}
</style>
