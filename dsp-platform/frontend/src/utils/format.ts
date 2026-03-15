import dayjs from 'dayjs'

/**
 * 格式化数字，添加千位分隔符
 */
export const formatNumber = (num: number, decimals = 2): string => {
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
}

/**
 * 格式化百分比
 */
export const formatPercent = (num: number, decimals = 2): string => {
  return `${formatNumber(num, decimals)}%`
}

/**
 * 格式化金额
 */
export const formatCurrency = (num: number): string => {
  return `¥${formatNumber(num, 2)}`
}

/**
 * 格式化日期时间
 */
export const formatDateTime = (date: string | Date): string => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

/**
 * 格式化日期
 */
export const formatDate = (date: string | Date): string => {
  return dayjs(date).format('YYYY-MM-DD')
}

/**
 * 格式化时间
 */
export const formatTime = (date: string | Date): string => {
  return dayjs(date).format('HH:mm:ss')
}

/**
 * 格式化相对时间
 */
export const formatRelativeTime = (date: string | Date): string => {
  const now = dayjs()
  const target = dayjs(date)
  const diff = now.diff(target, 'second')

  if (diff < 60) {
    return '刚刚'
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}分钟前`
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}小时前`
  } else if (diff < 604800) {
    return `${Math.floor(diff / 86400)}天前`
  } else {
    return formatDate(date)
  }
}

/**
 * 格式化文件大小
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${formatNumber(bytes / Math.pow(k, i))} ${sizes[i]}`
}

/**
 * 格式化时长
 */
export const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  } else if (minutes > 0) {
    return `${minutes}:${String(secs).padStart(2, '0')}`
  } else {
    return `${secs}秒`
  }
}

/**
 * 平台名称映射
 */
export const platformNameMap: Record<string, string> = {
  douyin: '抖音',
  kuaishou: '快手',
  bilibili: 'B站',
  weibo: '微博',
  xiaohongshu: '小红书',
}

/**
 * 获取平台显示名称
 */
export const getPlatformName = (platform: string): string => {
  return platformNameMap[platform] || platform
}
