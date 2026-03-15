import { Empty, Button } from 'antd'
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons'

interface EmptyStateProps {
  description?: string
  showCreateButton?: boolean
  onCreate?: () => void
  createButtonText?: string
  showRefreshButton?: boolean
  onRefresh?: () => void
}

const EmptyState = ({
  description = '暂无数据',
  showCreateButton = false,
  onCreate,
  createButtonText = '创建',
  showRefreshButton = false,
  onRefresh,
}: EmptyStateProps) => {
  return (
    <div style={{ padding: '40px 0', textAlign: 'center' }}>
      <Empty description={description}>
        <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
          {showRefreshButton && onRefresh && (
            <Button icon={<ReloadOutlined />} onClick={onRefresh}>
              刷新
            </Button>
          )}
          {showCreateButton && onCreate && (
            <Button type="primary" icon={<PlusOutlined />} onClick={onCreate}>
              {createButtonText}
            </Button>
          )}
        </div>
      </Empty>
    </div>
  )
}

export default EmptyState
