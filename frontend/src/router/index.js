import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'chat',
    component: () => import('@/views/Chat.vue'),
    meta: { title: '对话' }
  },
  {
    path: '/agents',
    name: 'agents',
    component: () => import('@/views/Agents.vue'),
    meta: { title: '智能体' }
  },
  {
    path: '/skills',
    name: 'skills',
    component: () => import('@/views/Skills.vue'),
    meta: { title: 'Echo Skills' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '设置' }
  },
  {
    path: '/status',
    name: 'status',
    component: () => import('@/views/Status.vue'),
    meta: { title: '状态' }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
