// ==================== 账户相关 ====================
export interface Account {
  id: string
  name: string
  platform: 'douyin' | 'kuaishou' | 'bilibili' | 'weibo' | 'xiaohongshu'
  status: 'active' | 'inactive' | 'expired'
  balance: number
  dailyBudget: number
  authorized: boolean
  createdAt: string
  updatedAt: string
}

// ==================== 广告计划相关 ====================
export interface Campaign {
  id: string
  name: string
  accountId: string
  campaignType: 'search' | 'display' | 'video' | 'feed'
  status: 'active' | 'paused' | 'ended' | 'pending'
  budgetType: 'daily' | 'total'
  budget: number
  startTime: string
  endTime: string
  objectives: string
  impressions: number
  clicks: number
  ctr: number
  cost: number
  cpa: number
  roas: number
  createdAt: string
  updatedAt: string
}

export interface CampaignFormData {
  name: string
  accountId: string
  campaignType: Campaign['campaignType']
  budgetType: Campaign['budgetType']
  budget: number
  startTime: string
  endTime: string
  objectives: string
}

// ==================== 广告组相关 ====================
export interface AdGroup {
  id: string
  campaignId: string
  name: string
  status: 'active' | 'paused' | 'ended'
  bidType: 'cpc' | 'cpm' | 'ocpc' | 'ocpm'
  bid: number
  budget: number
  targeting: Targeting
  impressions: number
  clicks: number
  conversions: number
  ctr: number
  cpc: number
  cost: number
  roas: number
  createdAt: string
  updatedAt: string
}

export interface Targeting {
  age?: {
    min?: number
    max?: number
  }
  gender?: 'male' | 'female' | 'all'
  location?: string[]
  interests?: string[]
  behaviors?: string[]
  deviceType?: string[]
  os?: string[]
  networkType?: string[]
  customAudiences?: string[]
}

export interface AdGroupFormData {
  campaignId: string
  name: string
  bidType: AdGroup['bidType']
  bid: number
  budget: number
  targeting: Targeting
}

// ==================== 广告创意相关 ====================
export interface Creative {
  id: string
  name: string
  adGroupId: string
  type: 'image' | 'video' | 'carousel'
  status: 'active' | 'inactive' | 'rejected' | 'pending'
  title: string
  description: string
  imageUrl?: string
  videoUrl?: string
  thumbnailUrl?: string
  callToAction?: string
  landingPageUrl: string
  width?: number
  height?: number
  duration?: number
  format?: string
  size?: number
  impressions: number
  clicks: number
  ctr: number
  cost: number
  conversions: number
  roas: number
  createdAt: string
  updatedAt: string
}

export interface CreativeFormData {
  adGroupId: string
  name: string
  type: Creative['type']
  title: string
  description: string
  callToAction?: string
  landingPageUrl: string
  imageUrl?: string
  videoUrl?: string
}

// ==================== 实时数据相关 ====================
export interface RealTimeData {
  timestamp: string
  accountId: string
  campaigns: {
    id: string
    name: string
    impressions: number
    clicks: number
    cost: number
    conversions: number
  }[]
  total: {
    impressions: number
    clicks: number
    cost: number
    conversions: number
  }
}

// ==================== 报表相关 ====================
export interface ReportData {
  date: string
  impressions: number
  clicks: number
  ctr: number
  cpc: number
  cpm: number
  cost: number
  conversions: number
  cpa: number
  roas: number
  revenue: number
}

export interface ReportFilters {
  dateRange: [string, string]
  accounts?: string[]
  campaigns?: string[]
  adGroups?: string[]
  dimensions?: string[]
}

// ==================== 用户相关 ====================
export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'manager' | 'operator' | 'viewer'
  permissions: string[]
  createdAt: string
  lastLogin: string
}

export interface LoginFormData {
  username: string
  password: string
}

// ==================== API响应 ====================
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}
