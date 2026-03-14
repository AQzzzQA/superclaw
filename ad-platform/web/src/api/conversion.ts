/**
 * 转化回传 API
 */
import api from './index'

export interface ConversionItem {
  click_id: string
  conversion_time: string
  conversion_type: string
}

export const conversionApi = {
  // 上传转化
  upload: (data: {
    advertiser_id: string
    conversions: ConversionItem[]
  }) => api.post('/conversion/upload', data),

  // 查询转化
  query: (data: {
    advertiser_id: string
    start_date: string
    end_date: string
  }, params?: { page?: number; page_size?: number }) =>
    api.post('/conversion/query', data, { params }),
}
