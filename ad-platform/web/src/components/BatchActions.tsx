/**
 * 批量操作组件
 */
import React, { useState } from 'react'
import { Button, Dropdown, Modal, Space, message } from 'antd'
import type { MenuProps } from 'antd'
import { MoreOutlined, PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons'

interface BatchActionsProps {
  selectedIds: number[]
  onBatchUpdateStatus: (ids: number[], status: 'enable' | 'disable') => Promise<void>
  onClearSelection: () => void
}

const BatchActions: React.FC<BatchActionsProps> = ({
  selectedIds,
  onBatchUpdateStatus,
  onClearSelection
}) => {
  const [loading, setLoading] = useState(false)

  const handleBatchUpdateStatus = async (status: 'enable' | 'disable') => {
    if (selectedIds.length === 0) {
      message.warning('请先选择要操作的项目')
      return
    }

    setLoading(true)
    try {
      await onBatchUpdateStatus(selectedIds, status)
      message.success(`已${status === 'enable' ? '启用' : '暂停'} ${selectedIds.length} 个项目`)
      onClearSelection()
    } catch (error) {
      message.error('操作失败')
    } finally {
      setLoading(false)
    }
  }

  const menuItems: MenuProps['items'] = [
    {
      key: 'enable',
      label: '批量启用',
      icon: <PlayCircleOutlined />,
      onClick: () => handleBatchUpdateStatus('enable')
    },
    {
      key: 'disable',
      label: '批量暂停',
      icon: <PauseCircleOutlined />,
      onClick: () => handleBatchUpdateStatus('disable')
    }
  ]

  if (selectedIds.length === 0) {
    return null
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 1000
    }}>
      <Space>
        <span style={{
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '8px 16px',
          borderRadius: '4px'
        }}>
          已选择 {selectedIds.length} 项
        </span>
        <Dropdown menu={{ items: menuItems }} placement="top">
          <Button type="primary" loading={loading} icon={<MoreOutlined />}>
            批量操作
          </Button>
        </Dropdown>
        <Button onClick={onClearSelection}>
          取消选择
        </Button>
      </Space>
    </div>
  )
}

export default BatchActions
