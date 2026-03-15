import { Card, Breadcrumb, Button, Space } from 'antd'
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons'
import type { ReactNode } from 'react'

interface PageHeaderProps {
  title: string
  description?: string
  breadcrumb?: { label: string; href?: string }[]
  extra?: ReactNode
  showAddButton?: boolean
  onAddClick?: () => void
  showRefreshButton?: boolean
  onRefreshClick?: () => void
  children?: ReactNode
}

const PageHeader = ({
  title,
  description,
  breadcrumb,
  extra,
  showAddButton = false,
  onAddClick,
  showRefreshButton = true,
  onRefreshClick,
  children,
}: PageHeaderProps) => {
  return (
    <div style={{ marginBottom: 16 }}>
      {breadcrumb && (
        <Breadcrumb style={{ marginBottom: 8 }}>
          {breadcrumb.map((item, index) => (
            <Breadcrumb.Item key={index}>
              {item.href ? <a href={item.href}>{item.label}</a> : item.label}
            </Breadcrumb.Item>
          ))}
        </Breadcrumb>
      )}
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h2 style={{ margin: 0, marginBottom: description ? 8 : 0 }}>{title}</h2>
            {description && <p style={{ margin: 0, color: '#666' }}>{description}</p>}
          </div>
          <Space>
            {extra}
            {showRefreshButton && (
              <Button icon={<ReloadOutlined />} onClick={onRefreshClick}>
                刷新
              </Button>
            )}
            {showAddButton && (
              <Button type="primary" icon={<PlusOutlined />} onClick={onAddClick}>
                新建
              </Button>
            )}
          </Space>
        </div>
        {children && <div style={{ marginTop: 16 }}>{children}</div>}
      </Card>
    </div>
  )
}

export default PageHeader
