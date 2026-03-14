/**
 * 广告计划 API
 */
import api from './index'

export interface Campaign {
  campaign_id: number
  campaign_name: string
  budget_mode: number
  budget?: number
  objective_type: string
  status: string
  start_time: string
  end_time: string
}

export interface CreateCampaignRequest {
  advertiser_id: string
  campaign_name: string
  budget_mode?: number
  budget?: number
  start_time: string
  end_time: string
  objectives?: string[]
}

export const campaignApi = {
  // 创建计划
  create: (data: CreateCampaignRequest) =>
    api.post('/campaign/create', data),

  // 获取计划列表
  list: (params: {
    advertiser_id: string
    campaign_ids?: string
    page?: number
    page_size?: number
  }) => api.get('/campaign/list', { params }),

  // 更新计划
  update: (data: {
    advertiser_id: string
    campaign_id: number
    campaign_name?: string
    budget?: number
  }) => api.post('/campaign/update', data),

  // 更新计划状态
  updateStatus: (data: {
    advertiser_id: string
    campaign_id: number
    opt_status: string
  }) => api.post('/campaign/update-status', data),

  // 删除计划
  delete: (data: {
    advertiser_id: string
    campaign_id: number
  }) => api.post('/campaign/delete', data),
}

export interface AdGroup {
  adgroup_id: number
  adgroup_name: string
  promote_mode: number
  budget_mode: number
  budget?: number
  status: string
  start_time: string
  end_time: string
}

export const adGroupApi = {
  // 创建广告组
  create: (data: {
    advertiser_id: string
    campaign_id: number
    adgroup_name: string
    promote_mode?: number
    budget_mode?: number
    budget?: number
    start_time: string
    end_time: string
  }) => api.post('/adgroup/create', data),

  // 获取广告组列表
  list: (params: {
    advertiser_id: string
    campaign_id?: number
    adgroup_ids?: string
    page?: number
    page_size?: number
  }) => api.get('/adgroup/list', { params }),

  // 更新广告组
  update: (data: {
    advertiser_id: string
    adgroup_id: number
    adgroup_name?: string
    budget?: number
  }) => api.post('/adgroup/update', data),

  // 更新广告组状态
  updateStatus: (data: {
    advertiser_id: string
    adgroup_id: number
    opt_status: string
  }) => api.post('/adgroup/update-status', data),

  // 删除广告组
  delete: (data: {
    advertiser_id: string
    adgroup_id: number
  }) => api.post('/adgroup/delete', data),
}

export interface Creative {
  creative_id: number
  creative_name: string
  creative_type: number
  creative_material_mode: number
  status: string
}

export const creativeApi = {
  // 创建创意
  create: (data: {
    advertiser_id: string
    adgroup_id: number
    creative_name: string
    creative_type: number
    creative_material_mode?: number
  }) => api.post('/creative/create', data),

  // 获取创意列表
  list: (params: {
    advertiser_id: string
    adgroup_id?: number
    creative_ids?: string
    page?: number
    page_size?: number
  }) => api.get('/creative/list', { params }),

  // 更新创意
  update: (data: {
    advertiser_id: string
    creative_id: number
    creative_name?: string
  }) => api.post('/creative/update', data),

  // 更新创意状态
  updateStatus: (data: {
    advertiser_id: string
    creative_id: number
    opt_status: string
  }) => api.post('/creative/update-status', data),

  // 删除创意
  delete: (data: {
    advertiser_id: string
    creative_id: number
  }) => api.post('/creative/delete', data),
}
