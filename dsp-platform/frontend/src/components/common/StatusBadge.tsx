import { Badge } from 'antd'
import type { ReactNode } from 'react'

type StatusType = 'active' | 'paused' | 'ended' | 'pending' | 'inactive' | 'rejected' | 'expired'

interface StatusBadgeProps {
  status: StatusType | string
  text?: string
}

const statusConfig: Record<StatusType, { status: 'success' | 'warning' | 'error' | 'default'; text: string }> = {
  active: { status: 'success', text: '进行中' },
  paused: { status: 'warning', text: '已暂停' },
  ended: { status: 'default', text: '已结束' },
  pending: { status: 'processing', text: '待审核' },
  inactive: { status: 'default', text: '未激活' },
  rejected: { status: 'error', text: '已拒绝' },
  expired: { status: 'error', text: '已过期' },
}

const StatusBadge = ({ status, text }: StatusBadgeProps) => {
  const config = statusConfig[status as StatusType]
  const displayText = text || config?.text || status

  return (
    <Badge
      status={config?.status || 'default'}
      text={displayText}
    />
  )
}

export default StatusBadge
