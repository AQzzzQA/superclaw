import { useState } from 'react'
import { Button, Space, Modal, message } from 'antd'
import { PlayCircleOutlined, PauseCircleOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useGetCampaignsQuery, useUpdateCampaignMutation, useDeleteCampaignMutation } from '../../store/services/campaignApi'
import PageHeader from '../../components/common/PageHeader'
import DataTable from '../../components/common/DataTable'
import StatusBadge from '../../components/common/StatusBadge'
import { formatCurrency, formatNumber, formatDateTime, formatPercent } from '../../utils/format'
import type { Campaign } from '../../types'

const CampaignList = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)

  const { data, isLoading, refetch } = useGetCampaignsQuery({ page, pageSize })
  const [updateCampaign] = useUpdateCampaignMutation()
  const [deleteCampaign] = useDeleteCampaignMutation()

  const columns = [
    {
      title: '计划名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: Campaign) => (
        <a onClick={() => navigate(`/campaigns/${record.id}/edit`)}>{text}</a>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      title: '类型',
      dataIndex: 'campaignType',
      key: 'campaignType',
      render: (type: string) => {
        const typeMap: Record<string, string> = {
          search: '搜索广告',
          display: '展示广告',
          video: '视频广告',
          feed: '信息流广告',
        }
        return typeMap[type] || type
      },
    },
    {
      title: '预算',
      dataIndex: 'budget',
      key: 'budget',
      render: (value: number, record: Campaign) => `${formatCurrency(value)} / ${record.budgetType === 'daily' ? '日' : '总计'}`,
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
      await updateCampaign({ id, data: { status } }).unwrap()
      message.success(status === 'active' ? '启动成功' : '暂停成功')
      refetch()
    } catch (error) {
      message.error('操作失败')
    }
  }

  const handleDelete = (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该广告计划吗？',
      onOk: async () => {
        try {
          await deleteCampaign(id).unwrap()
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
        title="广告计划列表"
        description="管理所有广告计划"
        showAddButton
        onAddClick={() => navigate('/campaigns/create')}
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

export default CampaignList
