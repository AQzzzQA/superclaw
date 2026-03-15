import { useState } from 'react'
import { Button, Space, Modal, message, Tag } from 'antd'
import { EyeOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useGetCreativesQuery, useDeleteCreativeMutation } from '../../store/services/creativeApi'
import PageHeader from '../../components/common/PageHeader'
import DataTable from '../../components/common/DataTable'
import StatusBadge from '../../components/common/StatusBadge'
import { formatNumber, formatPercent, formatCurrency, formatDateTime } from '../../utils/format'
import type { Creative } from '../../types'

const CreativeList = () => {
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)

  const { data, isLoading, refetch } = useGetCreativesQuery({ page, pageSize })
  const [deleteCreative] = useDeleteCreativeMutation()

  const columns = [
    {
      title: '创意信息',
      key: 'creative',
      render: (record: Creative) => (
        <Space direction="vertical" size={0}>
          <span style={{ fontWeight: 500 }}>{record.name}</span>
          <div style={{ display: 'flex', gap: 8 }}>
            <Tag color="blue">{record.type === 'image' ? '图片' : record.type === 'video' ? '视频' : '轮播'}</Tag>
            <Tag>{record.title}</Tag>
          </div>
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
      title: '尺寸',
      key: 'size',
      render: (record: Creative) => record.width && record.height ? `${record.width}x${record.height}` : '-',
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
      title: '转化数',
      dataIndex: 'conversions',
      key: 'conversions',
      render: formatNumber,
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

  const handleDelete = (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该创意吗？',
      onOk: async () => {
        try {
          await deleteCreative(id).unwrap()
          message.success('删除成功')
          refetch()
        } catch (error) {
          message.error('删除失败')
        }
      },
    })
  }

  const handlePreview = (record: Creative) => {
    Modal.info({
      title: record.name,
      content: (
        <div>
          {record.imageUrl && (
            <img
              src={record.imageUrl}
              alt={record.name}
              style={{ maxWidth: '100%', maxHeight: 400 }}
            />
          )}
          {record.videoUrl && (
            <video
              src={record.videoUrl}
              controls
              style={{ maxWidth: '100%', maxHeight: 400 }}
            />
          )}
          <p style={{ marginTop: 16 }}>
            <strong>标题：</strong>{record.title}<br/>
            <strong>描述：</strong>{record.description}<br/>
            <strong>落地页：</strong><a href={record.landingPageUrl} target="_blank" rel="noopener noreferrer">{record.landingPageUrl}</a>
          </p>
        </div>
      ),
      width: 600,
    })
  }

  return (
    <div>
      <PageHeader
        title="广告创意列表"
        description="管理所有广告创意"
        showAddButton
        onAddClick={() => navigate('/creatives/upload')}
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
              icon={<EyeOutlined />}
              onClick={() => handlePreview(record)}
            >
              预览
            </Button>
            <Button
              size="small"
              icon={<EditOutlined />}
              onClick={() => navigate(`/creatives/${record.id}/edit`)}
            >
              编辑
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

export default CreativeList
