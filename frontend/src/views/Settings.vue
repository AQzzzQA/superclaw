<template>
  <div class="settings-container">
    <n-card title="⚙️ 设置" class="settings-card">
      <n-form :model="settings" label-placement="left">
        <n-form-item label="OpenClaw Gateway URL">
          <n-input v-model:value="settings.openclawUrl" placeholder="http://localhost:18789" />
        </n-form-item>
        
        <n-form-item label="LemClaw Gateway URL">
          <n-input v-model:value="settings.lemclawUrl" placeholder="http://localhost:8089" />
        </n-form-item>
        
        <n-form-item label="Gateway Token">
          <n-input v-model:value="settings.gatewayToken" type="password" show-password-on="click" />
        </n-form-item>
        
        <n-form-item label="工作空间路径">
          <n-input v-model:value="settings.workspacePath" placeholder="/root/.openclaw/workspace" />
        </n-form-item>
        
        <n-form-item>
          <n-space>
            <n-button type="primary" @click="saveSettings">保存设置</n-button>
            <n-button @click="resetSettings">重置默认</n-button>
          </n-space>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMessage } from '@/composables/useNaiveUI'

const message = useMessage()

const settings = ref({
  openclawUrl: localStorage.getItem('openclawUrl') || 'http://localhost:18789',
  lemlclawUrl: localStorage.getItem('lemclawUrl') || 'http://localhost:8089',
  gatewayToken: localStorage.getItem('gatewayToken') || '',
  workspacePath: localStorage.getItem('workspacePath') || '/root/.openclaw/workspace',
})

const saveSettings = () => {
  localStorage.setItem('openclawUrl', settings.value.openclawUrl)
  localStorage.setItem('lemclawUrl', settings.value.lemclawUrl)
  localStorage.setItem('gatewayToken', settings.value.gatewayToken)
  localStorage.setItem('workspacePath', settings.value.workspacePath)
  
  message.success('设置已保存')
}

const resetSettings = () => {
  settings.value = {
    openclawUrl: 'http://localhost:18789',
    lemlclawUrl: 'http://localhost:8089',
    gatewayToken: '',
    workspacePath: '/root/.openclaw/workspace',
  }
  
  message.info('设置已重置')
}
</script>

<style scoped>
.settings-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.settings-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
