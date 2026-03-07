<template>
  <n-config-provider :theme-overrides="themeOverrides" :theme="isDark ? darkTheme : null">
    <n-layout has-sider>
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :collapsed="collapsed"
        show-trigger
        @collapse="collapsed = true"
        @expand="collapsed = false"
      >
        <div class="logo">
          <h1 v-if="!collapsed">SuperClaw 🦞</h1>
          <h1 v-else>🦞</h1>
        </div>
        
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          :value="currentKey"
          @update:value="handleMenuSelect"
        />
      </n-layout-sider>
      
      <n-layout>
        <n-layout-header bordered class="header">
          <div class="header-content">
            <h2>{{ pageTitle }}</h2>
            <n-space>
              <n-button quaternary circle @click="toggleTheme">
                <template #icon>
                  <n-icon v-if="isDark">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12 3a9 9 0 1 0 9 9 0 0 0-9 9 9 0 0 0 9 0zm0 16a7 7 0 1 1-7-7 7 7 0 0 1 7 7zm0-14a7 7 0 1 1 7-7 7 7 0 0 0-7 7 7 0 0 0 7z"/>
                    </svg>
                  </n-icon>
                  <n-icon v-else>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12 2a10 10 0 1 1 10 10 0 0 0-10 10 10 0 0 0 10zm0 18a8 8 0 1 1-8-8 8 8 0 0 0 8 8zm0-16a8 8 0 1 1 8-8 8 8 0 0 0-8 8 8 0 0 0 8z"/>
                    </svg>
                  </n-icon>
                </template>
              </n-button>
            </n-space>
          </div>
        </n-layout-header>
        
        <n-layout-content content-style="padding: 24px;" class="content">
          <router-view />
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-config-provider>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { NIcon } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
const collapsed = ref(false)
const isDark = ref(false)
const currentKey = ref('chat')

// 菜单选项
const menuOptions = [
  {
    label: '💬 对话',
    key: 'chat',
    icon: () => h(NIcon, null, { default: () => h('svg', { viewBox: '0 0 24 24' }, h('path', { fill: 'currentColor', d: 'M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z' })) })
  },
  {
    label: '🤖 智能体',
    key: 'agents',
    icon: () => h(NIcon, null, { default: () => h('svg', { viewBox: '0 0 24 24' }, h('path', { fill: 'currentColor', d: 'M12 2c-5.52 0-10 4.48-10 10s4.48 10 10 10c1.85 0 3.58-.63 5-1.68V21a1 1 0 0 1 0 1 1s-1-1-1-1v-4.72c2.05-.8 3.5-2.8 3.5-5.14 0-5.52-4.48-10-10-10z' })) })
  },
  {
    label: '🔧 Echo Skills',
    key: 'skills',
    icon: () => h(NIcon, null, { default: () => h('svg', { viewBox: '0 0 24 24' }, h('path', { fill: 'currentColor', d: 'M19.14 12.94c.04-.3.06-.61.06-.94 0-2.33-2.33-2.33-4.29 0-2.04 1.44-3.75 3.38-4.14l-2.86-.83c-.24-.07-.47-.12-.69-.18-1.13-.33-2.12-1.09-2.12-2.12V7.5c0-1.93-1.57-3.5-3.5-3.5H8c-1.93 0-3.5 1.57-3.5 3.5v2.17c0 1.03-.99 1.79-2.12 2.12-.22.06-.45.11-.69.18l-2.86.83c-1.94.39-3.38 2.1-3.38 4.14 0 1.96 1.44 3.64 3.38 4.04.04.33.06.64.06.94 0 2.33 2.33 4.29 2.33 2.04-1.44 3.75-3.38 4.14l2.86.83c.24.07.47.12.69.18 1.13.33 2.12 1.09 2.12 2.12v2.17c0 1.93 1.57 3.5 3.5 3.5h2c1.93 0 3.5-1.57 3.5-3.5v-2.17c0-1.03.99-1.79 2.12-2.12.22-.06.45-.11.69-.18l2.86-.83c1.94-.39 3.38-2.1 3.38-4.14 0-1.96-1.44-3.64-3.38-4.04-.04-.33-.06-.64-.06-.94zM13 17h-2v-2h2v2zm0-4H9v-2h4v2z' })) })
  },
  {
    label: '⚙️ 设置',
    key: 'settings',
    icon: () => h(NIcon, null, { default: () => h('svg', { viewBox: '0 0 24 24' }, h('path', { fill: 'currentColor', d: 'M19.14 12.94c.04-.3.06-.61.06-.94 0-2.33-2.33-2.33-4.29 0-2.04 1.44-3.75 3.38-4.14l-2.86-.83c-.24-.07-.47-.12-.69-.18-1.13-.33-2.12-1.09-2.12-2.12V7.5c0-1.93-1.57-3.5-3.5-3.5H8c-1.93 0-3.5 1.57-3.5 3.5v2.17c0 1.03-.99 1.79-2.12 2.12-.22.06-.45.11-.69.18l-2.86.83c-1.94.39-3.38 2.1-3.38 4.14 0 1.96 1.44 3.64 3.38 4.04.04.33.06.64.06.94 0 2.33 2.33 4.29 2.33 2.04-1.44 3.75-3.38 4.14l2.86.83c.24.07.47.12.69.18 1.13.33 2.12 1.09 2.12 2.12v2.17c0 1.93 1.57 3.5 3.5 3.5h2c1.93 0 3.5-1.57 3.5-3.5v-2.17c0-1.03.99-1.79 2.12-2.12.22-.06.45-.11.69-.18l2.86-.83c1.94-.39 3.38-2.1 3.38-4.14 0-1.96-1.44-3.64-3.38-4.04-.04-.33-.06-.64-.06-.94zM13 17h-2v-2h2v2zm0-4H9v-2h4v2z' })) })
  },
  {
    label: '📊 状态',
    key: 'status',
    icon: () => h(NIcon, null, { default: () => h('svg', { viewBox: '0 0 24 24' }, h('path', { fill: 'currentColor', d: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.55.45-1 1-1s1 .45 1 1c0 1.08 3.05 7.44 7 7.93v-2.01c-2.47-.28-4.5-2.26-4.5-2.24 0-.55-.45-1-1-1s1 .45 1 1c0 .02 2.03 1.96 4.5 2.24v-2.01zm6-7.93c0 .55.45 1 1 1s-.45 1-1 1c0 1.08-3.05 7.44-7 7.93v2.01c2.47-.28 4.5-2.26 4.5-2.24 0 .55-.45 1-1 1s-1-.45-1-1c0-.02-2.03 1.96-4.5 2.24v-2.01z' })) })
  },
]

// 页面标题
const pageTitle = computed(() => {
  const titles = {
    chat: '💬 对话',
    agents: '🤖 智能体',
    skills: '🔧 Echo Skills',
    settings: '⚙️ 设置',
    status: '📊 状态',
  }
  return titles[currentKey.value] || 'SuperClaw'
})

// 主题配置
const themeOverrides = {
  common: {
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6e',
    primaryColorPressed: '#0c7b43',
  },
}

const darkTheme = {
  common: {
    primaryColor: '#63e2b7',
    primaryColorHover: '#7ce2a9',
    primaryColorPressed: '#52c2a1',
  },
}

// 菜单选择处理
const handleMenuSelect = (key) => {
  currentKey.value = key
  router.push({ name: key })
}

// 切换主题
const toggleTheme = () => {
  isDark.value = !isDark.value
}
</script>

<style scoped>
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--n-border-color);
}

.logo h1 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.header-content h2 {
  margin: 0;
  font-size: 18px;
}

.content {
  min-height: calc(100vh - 64px);
}
</style>
