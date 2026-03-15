import { api } from './api'
import type { Campaign, CampaignFormData, PaginatedResponse, ApiResponse } from '../../types'

export const campaignApi = api.injectEndpoints({
  endpoints: (builder) => ({
    // 获取广告计划列表
    getCampaigns: builder.query<PaginatedResponse<Campaign>, { page?: number; pageSize?: number; accountId?: string; status?: string }>({
      query: ({ page = 1, pageSize = 20, accountId, status }) => {
        const params = new URLSearchParams({ page: page.toString(), pageSize: pageSize.toString() })
        if (accountId) params.append('accountId', accountId)
        if (status) params.append('status', status)
        return `/campaigns?${params.toString()}`
      },
      providesTags: ['Campaign'],
    }),

    // 获取单个广告计划
    getCampaign: builder.query<Campaign, string>({
      query: (id) => `/campaigns/${id}`,
      providesTags: (result, error, id) => [{ type: 'Campaign', id }],
    }),

    // 创建广告计划
    createCampaign: builder.mutation<Campaign, CampaignFormData>({
      query: (body) => ({
        url: '/campaigns',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Campaign'],
    }),

    // 更新广告计划
    updateCampaign: builder.mutation<Campaign, { id: string; data: Partial<Campaign> }>({
      query: ({ id, data }) => ({
        url: `/campaigns/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Campaign', id }],
    }),

    // 删除广告计划
    deleteCampaign: builder.mutation<void, string>({
      query: (id) => ({
        url: `/campaigns/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Campaign'],
    }),

    // 批量操作
    batchUpdateCampaigns: builder.mutation<ApiResponse<any>, { ids: string[]; action: 'start' | 'pause' | 'delete' }>({
      query: ({ ids, action }) => ({
        url: '/campaigns/batch',
        method: 'POST',
        body: { ids, action },
      }),
      invalidatesTags: ['Campaign'],
    }),
  }),
})

export const {
  useGetCampaignsQuery,
  useGetCampaignQuery,
  useCreateCampaignMutation,
  useUpdateCampaignMutation,
  useDeleteCampaignMutation,
  useBatchUpdateCampaignsMutation,
} = campaignApi
