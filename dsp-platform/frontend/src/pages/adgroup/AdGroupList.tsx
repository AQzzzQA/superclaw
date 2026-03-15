import { useState } from 'react'
import { Button, Space, Modal, message } from 'antd'
import { PlayCircleOutlined, PauseCircleOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useGetAdGroupsQuery, useUpdateAdGroupMutation, useDeleteAdGroupMutation } from '../../store/services/adGroupApi'
import PageHeader from '../../components/common/PageHeader'
import DataTable from '../../components/common/DataTable'
import StatusBadge from '../../components/common/StatusBadge'
import { formatCurrency, formatNumber, formatPercent, formatDateTime } from '../../utils/format'
import type { AdGroup } from '../../types'

const AdGroupList = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)

  const { data, isLoading, refetch } = useGetAdGroupsQuery({ page, pageSize })
  const [updateAdGroup] = useUpdateAdGroupMutation()
  const [deleteAdGroup] = useDeleteAdGroupMutation()

  const columns = [
    {
      title: '广告组名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: AdGroup) => (
        <a onClick={() => navigate(`/ad-groups/${record.id}/edit`)}>{text}</a>
      ),
    },
    {
      title: '所属计划',
      dataIndex: 'campaignId',
      key: 'campaignId',
      render: (id: string) => `计划-${id}`,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      title: '出价方式',
      dataIndex: 'bidType',
      key: 'bidType',
      render: (type: string) => {
        const typeMap: Record<string, string> = {
          cpc: 'CPC',
          cpm: 'CPM',
          ocpc: 'oCPC',
          ocpm: 'oCPM',
        }
        return typeMap[type] || type
      },
    },
    {
      title: '出价',
      dataIndex: 'bid',
      key: 'bid',
      render: formatCurrency,
    },
    {
      title: '预算',
      dataIndex: 'budget',
      key: 'budget',
      render: formatCurrency,
    },
    {
      title: '曝光量',
      dataIndex: 'impressions',
      key: 'impressions',
      render: formatNumber,
    },
    {
      title: '点击数',
      dataIndex: 'clicks',
      key: 'clicks',
      render: formatNumber,
    },
    {
      title: 'CTR',
      dataIndex: 'ctr',
      key: 'ctr',
      render: formatPercent,
    },
    {
      title: '消耗',
      dataIndex: 'cost',
      key: 'cost',
      render: formatCurrency,
    },
    {
      title: 'ROAS',
      dataIndex: 'roas',
      key: 'roas',
      render: (value: number) => value.toFixed(2),
    },
    {
      title: '更新时间',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
      render: formatDateTime,
    },
  ]

  const handleStatusChange = async (id: string, status: 'active' | 'paused') => {
    try {
      await updateAdGroup({ id, data: { status } }).unwrap()
      message.success(status === 'active' ? '启动成功' : '暂停成功')
      refetch()
    } catch (error) {
      message.error('操作失败')
    }
  }

  const handleDelete = (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该广告组吗？',
      onOk: async () => {
        try {
          await deleteAdGroup(id).unwrap()
          message.success('删除成功')
          refetch()
        } catch (error) {
          message.error('删除失败')
        }
      },
    })
  }

  return (
    <div>
      <PageHeader
        title="广告组列表"
        description="管理所有广告组"
        showAddButton
        onAddClick={() => navigate('/ad-groups/create')}
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
            {record.status === 'active' ? (
              <Button
                size="small"
                icon={<PauseCircleOutlined />}
                onClick={() => handleStatusChange(record.id, 'paused')}
              >
                暂停
              </Button>
            ) : (
              <Button
                size="small"
                type="primary"
                icon={<PlayCircleOutlined />}
                onClick={() => handleStatusChange(record.id, 'active')}
              >
                启动
              </Button>
            )}
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

export default AdGroupList
