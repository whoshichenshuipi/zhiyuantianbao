<template>
  <div class="app-container">
    <div style="margin-bottom: 20px;">
        <el-button type="primary" icon="Edit" @click="handlePost">发起提问 / 分享</el-button>
        <el-input 
            v-model="searchKeyword" 
            placeholder="搜索话题..." 
            style="width: 200px; margin-left: 10px;"
            prefix-icon="Search"
        />
    </div>

    <el-tabs v-model="activeTab">
        <el-tab-pane label="最新动态" name="latest">
            <div v-for="item in postList" :key="item.id" class="post-item">
                <div class="post-header">
                    <el-avatar :size="40" :src="item.avatar">{{ item.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                        <span class="author">{{ item.author }}</span>
                         <el-tag size="small" v-if="item.role === 'college'" type="warning">高校直招</el-tag>
                        <span class="time">{{ item.time }}</span>
                    </div>
                </div>
                <h3 class="post-title" @click="handleDetail(item)">{{ item.title }}</h3>
                <p class="post-content">{{ item.content }}</p>
                <div class="post-actions">
                    <span><el-icon><View /></el-icon> {{ item.views }}</span>
                    <span><el-icon><ChatDotSquare /></el-icon> {{ item.replies }}</span>
                    <span><el-icon><Star /></el-icon> {{ item.likes }}</span>
                </div>
                <el-divider />
            </div>
        </el-tab-pane>
        <el-tab-pane label="热门讨论" name="hot">
            <el-empty description="暂无热门话题" />
        </el-tab-pane>
        <el-tab-pane label="我的发布" name="mine">
            <el-empty description="您还没有发布过内容" />
        </el-tab-pane>
    </el-tabs>

    <el-dialog title="发起提问" v-model="dialogVisible" width="500px">
        <el-form label-width="80px">
            <el-form-item label="标题">
                <el-input v-model="newPost.title" placeholder="请输入标题" />
            </el-form-item>
             <el-form-item label="内容">
                <el-input v-model="newPost.content" type="textarea" :rows="4" placeholder="详细描述您的问题..." />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitPost">发布</el-button>
            </span>
        </template>
    </el-dialog>
  </div>
</template>

<script setup name="Community">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('latest')
const searchKeyword = ref('')
const dialogVisible = ref(false)
const newPost = reactive({
    title: '',
    content: ''
})

const postList = ref([
    {
        id: 1,
        author: '张三同学',
        role: 'student',
        avatar: '',
        time: '10分钟前',
        title: '620分理科，想冲南开大学有希望吗？',
        content: '如题，全省排名12500左右，比较喜欢经济学，看了往年分数线感觉有点悬...',
        views: 125,
        replies: 8,
        likes: 3
    },
     {
        id: 2,
        author: '四川大学招生办',
        role: 'college',
        avatar: '',
        time: '30分钟前',
        title: '【官方答疑】四川大学2025年招生政策解读',
        content: '欢迎各位考生报考四川大学！今年我校新增主要亮点如下...',
        views: 568,
        replies: 42,
        likes: 120
    },
      {
        id: 3,
        author: '李四家长',
        role: 'parent',
        avatar: '',
        time: '1小时前',
        title: '求助：孩子想学土木，现在就业形势还好吗？',
        content: '家里人都反对，但是孩子特别坚持，有没有懂行的分析一下？',
        views: 230,
        replies: 15,
        likes: 5
    }
])

function handlePost() {
    newPost.title = ''
    newPost.content = ''
    dialogVisible.value = true
}

function submitPost() {
    if(!newPost.title) {
        ElMessage.warning('请输入标题')
        return
    }
    dialogVisible.value = false
    ElMessage.success('发布成功！审核通过后将显示在列表中。')
    // Mock adding to list
    postList.value.unshift({
        id: Date.now(),
        author: '我 (Mock)',
        role: 'student',
        avatar: '',
        time: '刚刚',
        title: newPost.title,
        content: newPost.content,
        views: 0,
        replies: 0,
        likes: 0
    })
}

function handleDetail(item) {
    ElMessage.info(`查看详情: ${item.title}`)
}
</script>

<style scoped>
.post-item {
    padding: 10px 0;
}
.post-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.post-info {
    margin-left: 10px;
    display: flex;
    flex-direction: column;
}
.author {
    font-weight: bold;
    font-size: 14px;
}
.time {
    color: #999;
    font-size: 12px;
}
.post-title {
    margin: 5px 0;
    font-size: 16px;
    cursor: pointer;
}
.post-title:hover {
    color: #409EFF;
}
.post-content {
    color: #666;
    font-size: 14px;
    margin-bottom: 10px;
    line-height: 1.5;
}
.post-actions {
    display: flex;
    gap: 20px;
    color: #999;
    font-size: 13px;
}
.post-actions span {
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
}
</style>
