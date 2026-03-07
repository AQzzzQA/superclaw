<template>
  <div class="chat-container">
    <n-card title="💬 对话" class="chat-card">
      <div class="messages" ref="messagesContainer">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.role]"
        >
          <div class="message-content">
            <div class="message-header">
              <n-tag :type="message.role === 'user' ? 'primary' : 'info'" size="small">
                {{ message.role === 'user' ? '👤 用户' : '🤖 SuperClaw' }}
              </n-tag>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
            <div class="message-text">{{ message.content }}</div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <n-space vertical>
          <n-input
            v-model:value="inputMessage"
            type="textarea"
            placeholder="输入消息..."
            :autosize="{ minRows: 2, maxRows: 6 }"
            @keydown.enter.prevent="handleEnter"
          />
          <n-space>
            <n-button type="primary" @click="sendMessage" :loading="sending">
              发送
            </n-button>
            <n-button @click="clearMessages" :disabled="messages.length === 0">
              清空
            </n-button>
          </n-space>
        </n-space>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useMessage } from '@/composables/useNaiveUI'
import dayjs from 'dayjs'
import axios from 'axios'

const message = useMessage()
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    content: '你好！我是 SuperClaw，你的智能助手！🦞\n我可以帮助你：\n- 对话交流\n- 代码扫描\n- 自动修复\n- 智能生成\n\n有什么我可以帮你的吗？',
    timestamp: Date.now(),
  }
])
const inputMessage = ref('')
const sending = ref(false)
const messagesContainer = ref(null)

const sendMessage = async () => {
  if (!inputMessage.value.trim()) {
    message.warning('请输入消息')
    return
  }

  // 添加用户消息
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
    timestamp: Date.now(),
  })

  const userMessage = inputMessage.value
  inputMessage.value = ''
  sending.value = true

  try {
    // 发送到后端
    const response = await axios.post('/api/agent', {
      auth_code: 'default',
      message: userMessage,
    })

    // 添加 AI 回复
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: response.data.reply || '抱歉，我没有收到回复。',
      timestamp: Date.now(),
    })

    message.success('消息发送成功')
  } catch (error) {
    message.error(`发送失败：${error.message}`)
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: '抱歉，发送消息时出错。请检查网络连接。',
      timestamp: Date.now(),
    })
  } finally {
    sending.value = false
    scrollToBottom()
  }
}

const handleEnter = (e) => {
  if (e.shiftKey) {
    return // Shift + Enter 允许换行
  }
  sendMessage()
}

const clearMessages = () => {
  message.warning({
    content: '确定要清空所有对话记录吗？',
    action: () => {
      messages.value = []
      message.info('对话记录已清空')
    },
    positiveText: '确定',
    negativeText: '取消',
  })
}

const formatTime = (timestamp) => {
  return dayjs(timestamp).format('HH:mm:ss')
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 初始化滚动
scrollToBottom()
</script>

<style scoped>
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  justify-content: flex-start;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-text {
  padding: 12px;
  border-radius: 8px;
  background: #f5f5f5;
  word-wrap: break-word;
  line-height: 1.5;
}

.message.user .message-text {
  background: #e6f7ff;
}

.input-area {
  padding: 16px 0;
  border-top: 1px solid var(--n-border-color);
}
</style>
