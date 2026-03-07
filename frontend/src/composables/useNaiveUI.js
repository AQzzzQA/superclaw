import { createDiscreteApi } from 'naive-ui'

const discreteApi = createDiscreteApi(['message', 'dialog', 'notification', 'loadingBar'])

export function useNaiveUI() {
  return {
    message: discreteApi.message,
    dialog: discreteApi.dialog,
    notification: discreteApi.notification,
    loadingBar: discreteApi.loadingBar,
    registerNaiveUI(app) {
      app.provide('message', discreteApi.message)
      app.provide('dialog', discreteApi.dialog)
      app.provide('notification', discreteApi.notification)
      app.provide('loadingBar', discreteApi.loadingBar)
    },
  }
}

export function useMessage() {
  return discreteApi.message
}

export function useDialog() {
  return discreteApi.dialog
}

export function useNotification() {
  return discreteApi.notification
}

export function useLoadingBar() {
  return discreteApi.loadingBar
}
