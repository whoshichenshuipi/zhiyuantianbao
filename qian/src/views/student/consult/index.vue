<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="8">
          <el-card>
              <template #header>
                  <span>在线咨询高校列表</span>
              </template>
              <el-input v-model="searchText" placeholder="搜索高校..." prefix-icon="Search" style="margin-bottom: 15px" />
              <div v-for="college in collegeList" :key="college.id" class="college-item" @click="handleSelect(college)" :class="{ active: currentCollege.id === college.id }">
                  <div class="college-info">
                      <h4>{{ college.name }}</h4>
                      <p>{{ college.status }}</p>
                  </div>
                  <el-tag size="small" :type="college.online ? 'success' : 'info'">{{ college.online ? '在线' : '离线' }}</el-tag>
              </div>
          </el-card>
      </el-col>
      <el-col :span="16">
          <el-card class="chat-box" v-if="currentCollege.id">
              <template #header>
                  <div class="chat-header">
                      <span>与 <strong>{{ currentCollege.name }}</strong> 招生办对话中</span>
                      <el-button type="text" icon="Delete" @click="clearHistory">清空记录</el-button>
                  </div>
              </template>
              <div class="message-list" ref="messageBox">
                  <div v-for="msg in chatHistory" :key="msg.id" class="message-item" :class="{ 'me': msg.isMe }">
                      <div class="avatar" v-if="!msg.isMe">{{ currentCollege.name.charAt(0) }}</div>
                      <div class="message-content">{{ msg.text }}</div>
                      <div class="avatar" v-if="msg.isMe">我</div>
                  </div>
              </div>
              <div class="input-area">
                  <el-input 
                    v-model="inputText" 
                    type="textarea" 
                    :rows="3" 
                    placeholder="请输入您的问题... (按Enter发送)"
                    @keyup.enter="handleSend"
                   />
                  <div style="text-align: right; margin-top: 10px;">
                      <el-button type="primary" size="small" @click="handleSend">发送</el-button>
                  </div>
              </div>
          </el-card>
          <el-empty v-else description="请选择左侧高校开始咨询" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="Consult">
import { ref, reactive, nextTick } from 'vue'

const searchText = ref('')
const inputText = ref('')
const messageBox = ref(null)

const collegeList = ref([
    { id: 1, name: '北京大学', status: '招生办李老师', online: true },
    { id: 2, name: '清华大学', status: '招生办王老师', online: true },
    { id: 3, name: '复旦大学', status: '智能客服机器人', online: true },
    { id: 4, name: '浙江大学', status: '暂时离开', online: false },
])

const currentCollege = ref({})
const chatHistory = ref([])

function handleSelect(college) {
    currentCollege.value = college
    chatHistory.value = [
        { id: 1, isMe: false, text: `同学你好！我是${college.name}招生办老师，有什么可以帮你的吗？` }
    ]
}

function handleSend() {
    if(!inputText.value.trim()) return
    
    // User message
    chatHistory.value.push({
        id: Date.now(),
        isMe: true,
        text: inputText.value
    })
    
    const question = inputText.value
    inputText.value = ''
    
    // Auto reply mock
    setTimeout(() => {
        let reply = "收到您的问题，我们将尽快回复。"
        if(question.includes("分数线")) {
            reply = "我校去年的录取分数线可以在官网查询，一般来说理科需要在680分以上。"
        } else if(question.includes("专业")) {
            reply = "我校优势专业包括计算机、数学、经济学等。"
        }
        
        chatHistory.value.push({
            id: Date.now() + 1,
            isMe: false,
            text: reply
        })
        nextTick(() => {
            if(messageBox.value) {
                messageBox.value.scrollTop = messageBox.value.scrollHeight
            }
        })
    }, 1000)
    
     nextTick(() => {
        if(messageBox.value) {
            messageBox.value.scrollTop = messageBox.value.scrollHeight
        }
    })
}

function clearHistory() {
    chatHistory.value = []
}
</script>

<style scoped>
.college-item {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.college-item:hover {
    background-color: #f5f7fa;
}
.college-item.active {
    background-color: #e6f7ff;
}
.college-info h4 {
    margin: 0 0 5px 0;
}
.college-info p {
    margin: 0;
    font-size: 12px;
    color: #999;
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
    background: #ddd;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
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
    background: #95ec69;
}
.input-area {
    padding: 20px;
    border-top: 1px solid #eee;
}
</style>
