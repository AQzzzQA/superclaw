import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import authReducer from './slices/authSlice'
import campaignReducer from './slices/campaignSlice'
import adGroupReducer from './slices/adGroupSlice'
import creativeReducer from './slices/creativeSlice'
import monitorReducer from './slices/monitorSlice'
import { api } from './services/api'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    campaign: campaignReducer,
    adGroup: adGroupReducer,
    creative: creativeReducer,
    monitor: monitorReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
})

setupListeners(store.dispatch)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
