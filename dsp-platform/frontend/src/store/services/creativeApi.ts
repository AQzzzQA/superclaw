import { api } from './api'
import type { Creative, CreativeFormData, PaginatedResponse, ApiResponse } from '../../types'

export const creativeApi = api.injectEndpoints({
  endpoints: (builder) => ({
    // 获取广告创意列表
    getCreatives: builder.query<PaginatedResponse<Creative>, { page?: number; pageSize?: number; adGroupId?: string; status?: string; type?: string }>({
      query: ({ page = 1, pageSize = 20, adGroupId, status, type }) => {
        const params = new URLSearchParams({ page: page.toString(), pageSize: pageSize.toString() })
        if (adGroupId) params.append('adGroupId', adGroupId)
        if (status) params.append('status', status)
        if (type) params.append('type', type)
        return `/creatives?${params.toString()}`
      },
      providesTags: ['Creative'],
    }),

    // 获取单个广告创意
    getCreative: builder.query<Creative, string>({
      query: (id) => `/creatives/${id}`,
      providesTags: (result, error, id) => [{ type: 'Creative', id }],
    }),

    // 创建广告创意
    createCreative: builder.mutation<Creative, CreativeFormData>({
      query: (body) => ({
        url: '/creatives',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Creative'],
    }),

    // 更新广告创意
    updateCreative: builder.mutation<Creative, { id: string; data: Partial<Creative> }>({
      query: ({ id, data }) => ({
        url: `/creatives/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Creative', id }],
    }),

    // 删除广告创意
    deleteCreative: builder.mutation<void, string>({
      query: (id) => ({
        url: `/creatives/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Creative'],
    }),

    // 上传创意素材
    uploadCreative: builder.mutation<ApiResponse<{ url: string }>, FormData>({
      query: (formData) => ({
        url: '/creatives/upload',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Creative'],
    }),

    // 批量操作
    batchUpdateCreatives: builder.mutation<ApiResponse<any>, { ids: string[]; action: 'start' | 'pause' | 'delete' }>({
      query: ({ ids, action }) => ({
        url: '/creatives/batch',
        method: 'POST',
        body: { ids, action },
      }),
      invalidatesTags: ['Creative'],
    }),
  }),
})

export const {
  useGetCreativesQuery,
  useGetCreativeQuery,
  useCreateCreativeMutation,
  useUpdateCreativeMutation,
  useDeleteCreativeMutation,
  useUploadCreativeMutation,
  useBatchUpdateCreativesMutation,
} = creativeApi
