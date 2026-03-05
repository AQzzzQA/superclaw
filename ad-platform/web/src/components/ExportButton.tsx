/**
 * 数据导出组件
 */
import React, { useState } from 'react'
import { Button, Dropdown, message } from 'antd'
import type { MenuProps } from 'antd'
import { DownloadOutlined } from '@ant-design/icons'

interface ExportButtonProps {
  onExport: (format: 'xlsx' | 'csv') => Promise<void>
}

const ExportButton: React.FC<ExportButtonProps> = ({ onExport }) => {
  const [loading, setLoading] = useState(false)

  const handleExport = async (format: 'xlsx' | 'csv') => {
    setLoading(true)
    try {
      await onExport(format)
      message.success(`导出成功（${format.toUpperCase()}）`)
    } catch (error) {
      message.error('导出失败')
    } finally {
      setLoading(false)
    }
  }

  const menuItems: MenuProps['items'] = [
    {
      key: 'xlsx',
      label: '导出 Excel',
      onClick: () => handleExport('xlsx')
    },
    {
      key: 'csv',
      label: '导出 CSV',
      onClick: () => handleExport('csv')
    }
  ]

  return (
    <Dropdown menu={{ items: menuItems }} placement="bottomRight">
      <Button icon={<DownloadOutlined />} loading={loading}>
        导出数据
      </Button>
    </Dropdown>
  )
}

export default ExportButton
