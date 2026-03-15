import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CreativeState {
  selectedIds: string[]
  filters: {
    status?: string
    adGroupId?: string
    type?: string
    dateRange?: [string, string]
  }
}

const initialState: CreativeState = {
  selectedIds: [],
  filters: {},
}

const creativeSlice = createSlice({
  name: 'creative',
  initialState,
  reducers: {
    setSelectedCreatives: (state, action: PayloadAction<string[]>) => {
      state.selectedIds = action.payload
    },
    setCreativeFilters: (state, action: PayloadAction<CreativeState['filters']>) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    clearCreativeFilters: (state) => {
      state.filters = {}
    },
  },
})

export const { setSelectedCreatives, setCreativeFilters, clearCreativeFilters } = creativeSlice.actions
export default creativeSlice.reducer
