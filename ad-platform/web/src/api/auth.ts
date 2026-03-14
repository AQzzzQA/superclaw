/**
 * 认证相关 API
 */
import api from './index'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  tenant_id: number
  username: string
  password: string
  email?: string
}

export const authApi = {
  // 登录
  login: (data: LoginRequest) =>
    api.post<LoginResponse>('/auth/login', data),

  // 注册
  register: (data: RegisterRequest) =>
    api.post('/auth/register', data),

  // 获取当前用户信息
  getMe: () => api.get('/auth/me'),
}
