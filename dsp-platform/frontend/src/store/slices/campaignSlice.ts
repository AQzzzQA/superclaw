import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { Campaign } from '../../types'

interface CampaignState {
  selectedIds: string[]
  filters: {
    status?: string
    accountId?: string
    dateRange?: [string, string]
  }
}

const initialState: CampaignState = {
  selectedIds: [],
  filters: {},
}

const campaignSlice = createSlice({
  name: 'campaign',
  initialState,
  reducers: {
    setSelectedCampaigns: (state, action: PayloadAction<string[]>) => {
      state.selectedIds = action.payload
    },
    setCampaignFilters: (state, action: PayloadAction<CampaignState['filters']>) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    clearCampaignFilters: (state) => {
      state.filters = {}
    },
  },
})

export const { setSelectedCampaigns, setCampaignFilters, clearCampaignFilters } = campaignSlice.actions
export default campaignSlice.reducer
