<template>
  <div class="app-container">
    <el-card class="chat-container">
        <template #header>
            <div class="chat-header">
                <span><el-icon><Headset /></el-icon> 平台智能客服</span>
                <el-button type="text" @click="clearHistory">清空记录</el-button>
            </div>
        </template>
        
        <div class="message-list" ref="messageBox">
            <div v-for="msg in chatHistory" :key="msg.id" class="message-item" :class="{ 'me': msg.isMe }">
                <div class="avatar" v-if="!msg.isMe">
                    <el-icon><Service /></el-icon>
                </div>
                <div class="message-content">
                    <div v-html="msg.text"></div>
                </div>
                <div class="avatar" v-if="msg.isMe">我</div>
            </div>
        </div>

        <div class="input-area">
             <el-input 
                v-model="inputText" 
                type="textarea" 
                :rows="3" 
                placeholder="请描述您遇到的系统问题..."
                @keyup.enter="handleSend"
             />
             <div class="action-bar">
                 <span class="tip">常见问题：<a @click="quickAsk('如何修改密码？')">修改密码</a> <a @click="quickAsk('志愿表无法提交')">提交失败</a></span>
                 <el-button type="primary" @click="handleSend">发 送</el-button>
             </div>
        </div>
    </el-card>
  </div>
</template>

<script setup name="StudentService">
import { ref, reactive, nextTick, onMounted } from 'vue'

const inputText = ref('')
const messageBox = ref(null)

const chatHistory = ref([
    { id: 1, isMe: false, text: '您好！我是平台智能客服，请问有什么可以帮您？<br>人工服务时间：9:00 - 18:00' }
])

function handleSend() {
    if(!inputText.value.trim()) return
    
    const question = inputText.value
    chatHistory.value.push({
        id: Date.now(),
        isMe: true,
        text: question
    })
    
    inputText.value = ''
    scrollToBottom()
    
    // Mock Auto Reply
    setTimeout(() => {
        let reply = "很抱歉，我暂时无法理解这个问题。请尝试更详细的描述，或点击<a href='#'>转人工服务</a>。"
        if(question.includes("密码")) {
            reply = "您可以点击右上角头像，选择【个人中心】->【修改密码】进行重置。"
        } else if(question.includes("提交")) {
            reply = "志愿表提交失败可能是网络原因，请检查网络连接后重试。如问题依旧，请尝试刷新页面。"
        }
        
        chatHistory.value.push({
            id: Date.now() + 1,
            isMe: false,
            text: reply
        })
        scrollToBottom()
    }, 1000)
}

function quickAsk(text) {
    inputText.value = text
    handleSend()
}

function clearHistory() {
    chatHistory.value = [
        { id: 1, isMe: false, text: '系统提示：会话记录已清空。' }
    ]
}

function scrollToBottom() {
    nextTick(() => {
        if(messageBox.value) {
            messageBox.value.scrollTop = messageBox.value.scrollHeight
        }
    })
}
</script>

<style scoped>
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    height: 700px;
    display: flex;
    flex-direction: column;
}
.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
}
.message-list {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background: #f9f9f9;
    border-bottom: 1px solid #eee;
    height: 480px; /* fixed height for scroll */
}
.message-item {
    display: flex;
    margin-bottom: 20px;
}
.message-item.me {
    flex-direction: row-reverse;
}
.avatar {
    width: 40px;
    height: 40px;
    background: #e6e6e6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 10px;
    font-size: 20px;
}
.me .avatar {
    background: #409EFF;
    color: #fff;
    font-size: 14px;
}
.message-content {
    background: #fff;
    padding: 10px 15px;
    border-radius: 8px;
    max-width: 70%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    line-height: 1.5;
}
.me .message-content {
    background: #95ec69;
}
.input-area {
    padding: 20px;
}
.action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}
.tip {
    font-size: 12px;
    color: #999;
}
.tip a {
    color: #409EFF;
    cursor: pointer;
    margin-right: 10px;
}
</style>
