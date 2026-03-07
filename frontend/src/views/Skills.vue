<template>
  <div class="skills-container">
    <n-card title="🔧 Echo Skills" class="skills-card">
      <n-space vertical size="large">
        <!-- 代码扫描 -->
        <n-card title="代码扫描" size="small">
          <template #header-extra>
            <n-space>
              <n-button type="primary" @click="scanCode" :loading="scanning">
                开始扫描
              </n-button>
              <n-button @click="scanResults.length > 0 && clearScanResults()">
                清空
              </n-button>
            </n-space>
          </template>
          
          <n-spin :show="scanning">
            <n-empty v-if="!scanning && scanResults.length === 0" description="还没有扫描记录" />
            
            <div v-else class="scan-results">
              <n-alert
                v-if="scanResults.length > 0"
                type="info"
                title="扫描结果"
                :description="`${scanResults.length} 个问题发现`"
              />
              
              <n-list v-if="scanResults.length > 0">
                <n-list-item v-for="result in scanResults" :key="result.id">
                  <template #prefix>
                    <n-tag :type="result.severity === 'high' ? 'error' : result.severity === 'medium' ? 'warning' : 'default'" size="small">
                      {{ result.severity }}
                    </n-tag>
                  </template>
                  <n-ellipsis :line-clamp="2">{{ result.message }}</n-ellipsis>
                  <template #suffix>
                    <n-button text type="error" size="small" @click="removeResult(result.id)">
                      删除
                    </n-button>
                  </template>
                </n-list-item>
              </n-list>
            </div>
          </n-spin>
        </n-card>
        
        <!-- 自动修复 -->
        <n-card title="自动修复" size="small">
          <template #header-extra>
            <n-button type="primary" @click="autoFix" :loading="fixing" :disabled="scanResults.length === 0">
              开始修复
            </n-button>
          </template>
          
          <n-empty v-if="fixResults.length === 0" description="还没有修复记录" />
          
          <div v-else class="fix-results">
            <n-alert
              type="success"
              title="修复结果"
              :description="`${fixResults.length} 个文件已修复`"
            />
            
            <n-list>
              <n-list-item v-for="result in fixResults" :key="result.id">
                <template #prefix>
                  <n-icon color="#18a058">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                  </n-icon>
                </template>
                <n-ellipsis :line-clamp="2">{{ result.file_path }}</n-ellipsis>
                <template #suffix>
                  <n-tag type="success" size="small">
                    {{ result.fixes_applied }} 个修复
                  </n-tag>
                </template>
              </n-list-item>
            </n-list>
          </div>
        </n-card>
        
        <!-- 智能生成 -->
        <n-space>
          <n-button type="info" @click="generateChangelog">
            生成 CHANGELOG
          </n-button>
          <n-button type="info" @click="generateLicense">
            生成 LICENSE
          </n-button>
        </n-space>
      </n-space>
    </n-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMessage } from '@/composables/useNaiveUI'
import axios from 'axios'

const message = useMessage()
const scanning = ref(false)
const fixing = ref(false)
const scanResults = ref([])
const fixResults = ref([])

const scanCode = async () => {
  scanning.value = true
  try {
    const response = await axios.post('/api/skills/scan', {
      workspace_path: '/root/.openclaw/workspace',
    })
    
    scanResults.value = (response.data.issues || []).map((issue, index) => ({
      id: Date.now() + index,
      severity: issue.severity,
      message: issue.message,
      file_path: issue.file_path,
    }))
    
    message.success(`扫描完成，发现 ${scanResults.value.length} 个问题`)
  } catch (error) {
    message.error(`扫描失败：${error.message}`)
  } finally {
    scanning.value = false
  }
}

const autoFix = async () => {
  if (scanResults.value.length === 0) {
    message.warning('请先进行代码扫描')
    return
  }
  
  fixing.value = true
  try {
    const response = await axios.post('/api/skills/fix', {
      workspace_path: '/root/.openclaw/workspace',
      issues: scanResults.value,
    })
    
    fixResults.value = (response.data || []).map((result, index) => ({
      id: Date.now() + index,
      file_path: result.file_path,
      fixes_applied: result.fixes_applied || 0,
    }))
    
    message.success(`修复完成，共修复 ${fixResults.value.length} 个文件`)
    
    // 清空扫描结果
    scanResults.value = []
  } catch (error) {
    message.error(`修复失败：${error.message}`)
  } finally {
    fixing.value = false
  }
}

const generateChangelog = async () => {
  try {
    const response = await axios.post('/api/skills/generate/changelog', {
      workspace_path: '/root/.openclaw/workspace',
      changes: [
        '实现双网关架构',
        '添加 Echo Skills',
        '创建前端界面',
      ],
    })
    
    message.success('CHANGELOG 生成成功')
  } catch (error) {
    message.error(`生成失败：${error.message}`)
  }
}

const generateLicense = async () => {
  try {
    const response = await axios.post('/api/skills/generate/license', {
      workspace_path: '/root/.openclaw/workspace',
    })
    
    message.success('LICENSE 生成成功')
  } catch (error) {
    message.error(`生成失败：${error.message}`)
  }
}

const clearScanResults = () => {
  scanResults.value = []
  message.info('扫描结果已清空')
}

const removeResult = (id) => {
  scanResults.value = scanResults.value.filter(r => r.id !== id)
}
</script>

<style scoped>
.skills-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.skills-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scan-results,
.fix-results {
  max-height: 400px;
  overflow-y: auto;
}
</style>
