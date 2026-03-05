/**
 * 数据报表 API
 */
import api from './index'

export interface DailyReportItem {
  stat_date: string
  cost: number
  show: number
  click: number
  ctr: number
  cpm: number
  cpc: number
  convert: number
}

export interface ReportQueryRequest {
  advertiser_id: string
  start_date: string
  end_date: string
  campaign_ids?: string
  adgroup_ids?: string
}

export const reportApi = {
  // 获取日报表
  getDailyReport: (data: ReportQueryRequest, params?: { page?: number; page_size?: number }) =>
    api.post('/report/daily', data, { params }),

  // 获取历史报表
  getHistory: (params: {
    advertiser_id: string
    start_date?: string
    end_date?: string
    page?: number
    page_size?: number
  }) => api.get('/report/history', { params }),
}
