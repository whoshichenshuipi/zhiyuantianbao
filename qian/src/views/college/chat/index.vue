<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
          <el-card class="student-list-card">
              <template #header>
                  <span>待回复咨询 ({{ studentList.length }})</span>
              </template>
              <div v-for="stu in studentList" :key="stu.id" class="student-item" @click="handleSelect(stu)" :class="{ active: currentStudent.id === stu.id }">
                  <el-avatar :size="40">{{ stu.name.charAt(0) }}</el-avatar>
                  <div class="info">
                      <div class="top">
                          <span class="name">{{ stu.name }}</span>
                          <span class="time">{{ stu.time }}</span>
                      </div>
                      <p class="msg">{{ stu.lastMsg }}</p>
                  </div>
                  <el-badge is-dot v-if="stu.unread" />
              </div>
          </el-card>
      </el-col>
      <el-col :span="18">
          <el-card class="chat-box" v-if="currentStudent.id">
              <template #header>
                  <div class="chat-header">
                      <span>正在回复: <strong>{{ currentStudent.name }}</strong> ({{ currentStudent.score }}分 / {{ currentStudent.region }})</span>
                      <div>
                          <el-button size="small" @click="handleCheckProfile">查看学生档案</el-button>
                          <el-button size="small" type="success" @click="handleQuickReply">快捷回复</el-button>
                      </div>
                  </div>
              </template>
              <div class="message-list" ref="messageBox">
                  <div v-for="msg in chatHistory" :key="msg.id" class="message-item" :class="{ 'me': msg.isMe }">
                      <div class="avatar" v-if="!msg.isMe">{{ currentStudent.name.charAt(0) }}</div>
                      <div class="message-content">{{ msg.text }}</div>
                      <div class="avatar" v-if="msg.isMe">教</div>
                  </div>
              </div>
              <div class="input-area">
                  <el-input 
                    v-model="inputText" 
                    type="textarea" 
                    :rows="3" 
                    placeholder="请输入回复内容..."
                    @keyup.enter="handleSend"
                   />
                  <div style="text-align: right; margin-top: 10px;">
                      <el-button type="primary" size="small" @click="handleSend">回复</el-button>
                  </div>
              </div>
          </el-card>
          <el-empty v-else description="请从左侧选择待回复的学生" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="CollegeChat">
import { ref, reactive, nextTick } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'

const inputText = ref('')
const messageBox = ref(null)

const studentList = ref([
    { id: 1, name: '张三', region: '北京', score: 620, time: '10:05', lastMsg: '老师您好，请问贵校去年理科线是多少？', unread: true },
    { id: 2, name: '李四', region: '河北', score: 650, time: '09:30', lastMsg: '我想咨询一下计算机专业的就业情况', unread: false },
    { id: 3, name: '王五', region: '山东', score: 580, time: '昨天', lastMsg: '谢谢老师！', unread: false },
])

const currentStudent = ref({})
const chatHistory = ref([])

function handleSelect(stu) {
    currentStudent.value = stu
    stu.unread = false
    // Mock history
    chatHistory.value = [
        { id: 1, isMe: false, text: stu.lastMsg }
    ]
}

function handleSend() {
    if(!inputText.value.trim()) return
    
    chatHistory.value.push({
        id: Date.now(),
        isMe: true,
        text: inputText.value
    })
    
    inputText.value = ''
    
    nextTick(() => {
        if(messageBox.value) {
            messageBox.value.scrollTop = messageBox.value.scrollHeight
        }
    })
    
    ElMessage.success('回复发送成功')
}

function handleCheckProfile() {
    ElNotification({
        title: '学生档案',
        message: `${currentStudent.value.name}，${currentStudent.value.region}考生，高考分数${currentStudent.value.score}分。意向专业：计算机、金融。`,
        duration: 5000
    })
}

function handleQuickReply() {
    inputText.value = "同学你好，关于这个问题，你可以参考我校发布的最新招生章程。"
}
</script>

<style scoped>
.student-list-card {
    height: 600px;
    overflow-y: auto;
}
.student-item {
    padding: 15px 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
}
.student-item:hover {
    background-color: #f5f7fa;
}
.student-item.active {
    background-color: #e6f7ff;
}
.info {
    flex: 1;
    overflow: hidden;
}
.top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}
.name {
    font-weight: bold;
    font-size: 14px;
}
.time {
    font-size: 12px;
    color: #999;
}
.msg {
    font-size: 12px;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 0;
}

.chat-box {
    height: 600px;
    display: flex;
    flex-direction: column;
}
.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.message-list {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background: #f9f9f9;
}
.message-item {
    display: flex;
    margin-bottom: 15px;
}
.message-item.me {
    flex-direction: row-reverse;
}
.avatar {
    width: 36px;
    height: 36px;
    background: #409EFF;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    margin: 0 10px;
}
.message-content {
    background: #fff;
    padding: 10px;
    border-radius: 4px;
    max-width: 70%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.me .message-content {
    background: #e1f3d8;
}
.input-area {
    padding: 20px;
    border-top: 1px solid #eee;
}
</style>
