<template>
  <div class="status-container">
    <n-card title="📊 系统状态" class="status-card">
      <n-spin :show="loading">
        <n-space vertical size="large">
          <!-- Gateway 状态 -->
          <n-card title="网关状态" size="small">
            <n-space vertical>
              <n-space>
                <n-statistic label="OpenClaw Gateway" :value="gatewayStatus.openclaw_gateway.healthy ? 1 : 0">
                  <template #suffix>
                    <n-tag :type="gatewayStatus.openclaw_gateway.healthy ? 'success' : 'error'">
                      {{ gatewayStatus.openclaw_gateway.healthy ? '正常' : '离线' }}
                    </n-tag>
                  </template>
                </n-statistic>
              </n-space>
              <n-space>
                <n-statistic label="LemClaw Gateway" :value="gatewayStatus.lemclaw_gateway.healthy ? 1 : 0">
                  <template #suffix>
                    <n-tag :type="gatewayStatus.lemclaw_gateway.healthy ? 'success' : 'error'">
                      {{ gatewayStatus.lemclaw_gateway.healthy ? '正常' : '离线' }}
                    </n-tag>
                  </template>
                </n-statistic>
              </n-space>
            </n-space>
          </n-card>
          
          <!-- 系统信息 -->
          <n-card title="系统信息" size="small">
            <n-descriptions bordered :column="1">
              <n-descriptions-item label="系统时间">
                {{ formatTime(systemInfo.timestamp) }}
              </n-descriptions-item>
              <n-descriptions-item label="运行时间">
                {{ formatUptime(systemInfo.uptime) }}
              </n-descriptions-item>
              <n-descriptions-item label="版本">
                {{ systemInfo.version }}
              </n-descriptions-item>
            </n-descriptions>
          </n-card>
          
          <!-- 性能指标 -->
          <n-card title="性能指标" size="small">
            <n-space vertical>
              <n-progress type="line" percentage="systemInfo.cpu_usage" label="CPU 使用率" />
              <n-progress type="line" percentage="systemInfo.memory_usage" label="内存使用率" />
              <n-progress type="line" percentage="systemInfo.disk_usage" label="磁盘使用率" />
            </n-space>
          </n-card>
        </n-space>
      </n-spin>
    </n-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMessage } from '@/composables/useNaiveUI'
import axios from 'axios'
import dayjs from 'dayjs'

const message = useMessage()
const loading = ref(false)
const gatewayStatus = ref({
  openclaw_gateway: { healthy: false, url: '' },
  lemlaw_gateway: { healthy: false, url: '' },
  timestamp: 0,
})
const systemInfo = ref({
  timestamp: Date.now(),
  uptime: 0,
  version: 'v1.0.0',
  cpu_usage: 45,
  memory_usage: 62,
  disk_usage: 38,
})

const fetchStatus = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/status')
    gatewayStatus.value = response.data
    systemInfo.value.timestamp = Date.now()
  } catch (error) {
    message.error(`获取状态失败：${error.message}`)
  } finally {
    loading.value = false
  }
}

const formatTime = (timestamp) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

const formatUptime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小时 ${minutes}分钟`
}

// 每 5 秒刷新状态
onMounted(() => {
  fetchStatus()
  setInterval(fetchStatus, 5000)
})
</script>

<style scoped>
.status-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.status-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
