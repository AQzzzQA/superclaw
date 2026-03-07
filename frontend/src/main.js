import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useNaiveUI } from './composables/useNaiveUI'

const app = createApp(App)

// 注册 Naive UI
const { registerNaiveUI } = useNaiveUI()
registerNaiveUI(app)

// 注册路由
app.use(router)

// 注册状态管理
app.use(createPinia())

// 挂载应用
app.mount('#app')
