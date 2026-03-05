/**
 * 全局状态管理
 */
import { create } from 'zustand'

interface GlobalState {
  loading: boolean
  sidebarCollapsed: boolean
  theme: 'light' | 'dark'

  setLoading: (loading: boolean) => void
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
}

export const useGlobalStore = create<GlobalState>((set) => ({
  loading: false,
  sidebarCollapsed: false,
  theme: 'light',

  setLoading: (loading) => set({ loading }),

  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

  setTheme: (theme) => set({ theme })
}))
