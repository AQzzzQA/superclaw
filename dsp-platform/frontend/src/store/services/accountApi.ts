import { api } from './api'
import type { Account, PaginatedResponse, ApiResponse } from '../../types'

export const accountApi = api.injectEndpoints({
  endpoints: (builder) => ({
    // 获取账户列表
    getAccounts: builder.query<PaginatedResponse<Account>, { page?: number; pageSize?: number }>({
      query: ({ page = 1, pageSize = 20 }) => `/accounts?page=${page}&pageSize=${pageSize}`,
      providesTags: ['Account'],
    }),

    // 获取单个账户
    getAccount: builder.query<Account, string>({
      query: (id) => `/accounts/${id}`,
      providesTags: (result, error, id) => [{ type: 'Account', id }],
    }),

    // 创建账户
    createAccount: builder.mutation<Account, Partial<Account>>({
      query: (body) => ({
        url: '/accounts',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Account'],
    }),

    // 更新账户
    updateAccount: builder.mutation<Account, { id: string; data: Partial<Account> }>({
      query: ({ id, data }) => ({
        url: `/accounts/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Account', id }],
    }),

    // 删除账户
    deleteAccount: builder.mutation<void, string>({
      query: (id) => ({
        url: `/accounts/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Account'],
    }),

    // 授权账户
    authorizeAccount: builder.mutation<ApiResponse<any>, { accountId: string; authCode: string }>({
      query: ({ accountId, authCode }) => ({
        url: `/accounts/${accountId}/authorize`,
        method: 'POST',
        body: { authCode },
      }),
      invalidatesTags: ['Account'],
    }),

    // 同步账户数据
    syncAccount: builder.mutation<ApiResponse<any>, string>({
      query: (id) => ({
        url: `/accounts/${id}/sync`,
        method: 'POST',
      }),
      invalidatesTags: ['Account'],
    }),
  }),
})

export const {
  useGetAccountsQuery,
  useGetAccountQuery,
  useCreateAccountMutation,
  useUpdateAccountMutation,
  useDeleteAccountMutation,
  useAuthorizeAccountMutation,
  useSyncAccountMutation,
} = accountApi
