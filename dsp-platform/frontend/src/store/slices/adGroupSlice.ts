import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface AdGroupState {
  selectedIds: string[]
  filters: {
    status?: string
    campaignId?: string
    dateRange?: [string, string]
  }
}

const initialState: AdGroupState = {
  selectedIds: [],
  filters: {},
}

const adGroupSlice = createSlice({
  name: 'adGroup',
  initialState,
  reducers: {
    setSelectedAdGroups: (state, action: PayloadAction<string[]>) => {
      state.selectedIds = action.payload
    },
    setAdGroupFilters: (state, action: PayloadAction<AdGroupState['filters']>) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    clearAdGroupFilters: (state) => {
      state.filters = {}
    },
  },
})

export const { setSelectedAdGroups, setAdGroupFilters, clearAdGroupFilters } = adGroupSlice.actions
export default adGroupSlice.reducer
