/**
 * OAuth2 认证 API
 */
import api from './index'

export interface AuthorizeResponse {
  authorize_url: string
  redirect_uri: string
  state: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  expires_in: number
  advertiser_ids: string[]
  state?: string
}

export const oauthApi = {
  // 获取授权 URL
  getAuthorizeUrl: (params?: { redirect_uri?: string; state?: string }) =>
    api.get<AuthorizeResponse>('/oauth/authorize', { params }),

  // 回调处理
  callback: (params: { auth_code: string; state?: string }) =>
    api.post<TokenResponse>('/oauth/callback', null, { params }),

  // 刷新 Token
  refreshToken: (refresh_token: string) =>
    api.post<TokenResponse>('/oauth/refresh', { refresh_token }),
}
