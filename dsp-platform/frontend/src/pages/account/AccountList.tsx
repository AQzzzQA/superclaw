import { useState } from 'react'
import { Button, Space, Modal, message } from 'antd'
import { PlusOutlined, SyncOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useGetAccountsQuery, useDeleteAccountMutation, useSyncAccountMutation } from '../../store/services/accountApi'
import PageHeader from '../../components/common/PageHeader'
import DataTable from '../../components/common/DataTable'
import StatusBadge from '../../components/common/StatusBadge'
import { getPlatformName, formatCurrency, formatDateTime } from '../../utils/format'
import type { Account } from '../../types'

const AccountList = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)

  const { data, isLoading, refetch } = useGetAccountsQuery({ page, pageSize })
  const [deleteAccount] = useDeleteAccountMutation()
  const [syncAccount] = useSyncAccountMutation()

  const columns = [
    {
      title: '账户名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: Account) => (
        <Space direction="vertical" size={0}>
          <span style={{ fontWeight: 500 }}>{text}</span>
          <span style={{ color: '#666', fontSize: 12 }}>{getPlatformName(record.platform)}</span>
        </Space>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      title: '余额',
      dataIndex: 'balance',
      key: 'balance',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: '日预算',
      dataIndex: 'dailyBudget',
      key: 'dailyBudget',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: '授权状态',
      dataIndex: 'authorized',
      key: 'authorized',
      render: (authorized: boolean) => (
        authorized ? <span style={{ color: '#52c41a' }}>已授权</span> : <span style={{ color: '#ff4d4f' }}>未授权</span>
      ),
    },
    {
      title: '更新时间',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
      render: (value: string) => formatDateTime(value),
    },
  ]

  const handleDelete = (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该账户吗？',
      onOk: async () => {
        try {
          await deleteAccount(id).unwrap()
          message.success('删除成功')
          refetch()
        } catch (error) {
          message.error('删除失败')
        }
      },
    })
  }

  const handleSync = async (id: string) => {
    try {
      await syncAccount(id).unwrap()
      message.success('同步成功')
      refetch()
    } catch (error) {
      message.error('同步失败')
    }
  }

  return (
    <div>
      <PageHeader
        title="账户列表"
        description="管理所有媒体平台的广告账户"
        showAddButton
        onAddClick={() => navigate('/accounts/authorize')}
        onRefreshClick={refetch}
      />

      <DataTable
        columns={columns}
        dataSource={data?.items || []}
        loading={isLoading}
        rowSelection={{
          selectedRowKeys: [],
          onChange: () => {},
        }}
        rowActions={(record) => (
          <Space>
            <Button
              size="small"
              icon={<SyncOutlined />}
              onClick={() => handleSync(record.id)}
            >
              同步
            </Button>
            <Button
              size="small"
              danger
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record.id)}
            >
              删除
            </Button>
          </Space>
        )}
        pagination={{
          current: page,
          pageSize,
          total: data?.total || 0,
          onChange: (newPage, newPageSize) => {
            setPage(newPage)
            setPageSize(newPageSize)
          },
        }}
      />
    </div>
  )
}

export default AccountList
