import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { RealTimeData } from '../../types'

interface MonitorState {
  isConnected: boolean
  realtimeData: RealTimeData | null
  lastUpdate: string | null
  autoRefresh: boolean
  refreshInterval: number
}

const initialState: MonitorState = {
  isConnected: false,
  realtimeData: null,
  lastUpdate: null,
  autoRefresh: true,
  refreshInterval: 30000,
}

const monitorSlice = createSlice({
  name: 'monitor',
  initialState,
  reducers: {
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload
    },
    updateRealtimeData: (state, action: PayloadAction<RealTimeData>) => {
      state.realtimeData = action.payload
      state.lastUpdate = new Date().toISOString()
    },
    toggleAutoRefresh: (state) => {
      state.autoRefresh = !state.autoRefresh
    },
    setRefreshInterval: (state, action: PayloadAction<number>) => {
      state.refreshInterval = action.payload
    },
  },
})

export const { setConnected, updateRealtimeData, toggleAutoRefresh, setRefreshInterval } = monitorSlice.actions
export default monitorSlice.reducer
