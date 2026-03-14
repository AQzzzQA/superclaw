/**
 * 账户管理 API
 */
import api from './index'

export interface Account {
  id: number
  advertiser_id: string
  advertiser_name: string
  status: number
  expires_at: string
  created_at: string
}

export interface CreateAccountRequest {
  advertiser_id: string
  advertiser_name: string
  access_token: string
  refresh_token: string
  expires_at: string
}

export interface UpdateAccountRequest {
  access_token?: string
  refresh_token?: string
  expires_at?: string
  status?: number
}

export const accountApi = {
  // 创建账户
  create: (data: CreateAccountRequest) =>
    api.post('/account/create', data),

  // 获取账户列表
  list: () => api.get<{ code: number; message: string; data: Account[] }>('/account/list'),

  // 获取账户详情
  get: (accountId: number) =>
    api.get(`/account/${accountId}`),

  // 更新账户
  update: (accountId: number, data: UpdateAccountRequest) =>
    api.post(`/account/${accountId}/update`, data),

  // 删除账户
  delete: (accountId: number) =>
    api.post(`/account/${accountId}/delete`),
}
