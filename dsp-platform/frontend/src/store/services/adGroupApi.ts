import { api } from './api'
import type { AdGroup, AdGroupFormData, PaginatedResponse, ApiResponse } from '../../types'

export const adGroupApi = api.injectEndpoints({
  endpoints: (builder) => ({
    // 获取广告组列表
    getAdGroups: builder.query<PaginatedResponse<AdGroup>, { page?: number; pageSize?: number; campaignId?: string; status?: string }>({
      query: ({ page = 1, pageSize = 20, campaignId, status }) => {
        const params = new URLSearchParams({ page: page.toString(), pageSize: pageSize.toString() })
        if (campaignId) params.append('campaignId', campaignId)
        if (status) params.append('status', status)
        return `/ad-groups?${params.toString()}`
      },
      providesTags: ['AdGroup'],
    }),

    // 获取单个广告组
    getAdGroup: builder.query<AdGroup, string>({
      query: (id) => `/ad-groups/${id}`,
      providesTags: (result, error, id) => [{ type: 'AdGroup', id }],
    }),

    // 创建广告组
    createAdGroup: builder.mutation<AdGroup, AdGroupFormData>({
      query: (body) => ({
        url: '/ad-groups',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['AdGroup'],
    }),

    // 更新广告组
    updateAdGroup: builder.mutation<AdGroup, { id: string; data: Partial<AdGroup> }>({
      query: ({ id, data }) => ({
        url: `/ad-groups/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'AdGroup', id }],
    }),

    // 删除广告组
    deleteAdGroup: builder.mutation<void, string>({
      query: (id) => ({
        url: `/ad-groups/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['AdGroup'],
    }),

    // 批量操作
    batchUpdateAdGroups: builder.mutation<ApiResponse<any>, { ids: string[]; action: 'start' | 'pause' | 'delete' }>({
      query: ({ ids, action }) => ({
        url: '/ad-groups/batch',
        method: 'POST',
        body: { ids, action },
      }),
      invalidatesTags: ['AdGroup'],
    }),
  }),
})

export const {
  useGetAdGroupsQuery,
  useGetAdGroupQuery,
  useCreateAdGroupMutation,
  useUpdateAdGroupMutation,
  useDeleteAdGroupMutation,
  useBatchUpdateAdGroupsMutation,
} = adGroupApi
