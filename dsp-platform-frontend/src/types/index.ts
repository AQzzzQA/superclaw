// 全局类型定义

// 用户相关
export interface User {
  id: number;
  username: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
  created_at: string;
}

// 广告主相关
export interface Advertiser {
  id: number;
  name: string;
  email: string;
  phone: string;
  company: string;
  balance: number;
  status: 'active' | 'inactive';
  created_at: string;
}

// 广告计划
export interface Campaign {
  id: number;
  advertiser_id: number;
  name: string;
  type: 'display' | 'video' | 'native';
  start_date: string;
  end_date: string;
  budget: number;
  status: 'active' | 'paused' | 'completed' | 'pending';
  created_at: string;
  updated_at: string;
  advertiser?: Advertiser;
}

// 广告组
export interface AdGroup {
  id: number;
  campaign_id: number;
  name: string;
  targeting: Record<string, any>;
  bid_amount: number;
  status: 'active' | 'paused';
  created_at: string;
  campaign?: Campaign;
}

// 创意
export interface Creative {
  id: number;
  campaign_id: number;
  name: string;
  type: 'image' | 'video' | 'html';
  content: string;
  width: number;
  height: number;
  file_url: string;
  status: 'active' | 'paused';
  approval_status: 'pending' | 'approved' | 'rejected';
  created_at: string;
}

// 受众
export interface Audience {
  id: number;
  name: string;
  description: string;
  targeting: Record<string, any>;
  size: number;
  status: 'active' | 'calculating';
  created_at: string;
}

// 报表数据
export interface CampaignReport {
  id: number;
  campaign_id: number;
  campaign?: Campaign;
  report_date: string;
  impressions: number;
  clicks: number;
  ctr: number;
  cost: number;
  cpc: number;
  cpm: number;
  conversions: number;
  conversion_rate: number;
  created_at: string;
}

// 实时报表
export interface RealTimeReport {
  id: number;
  object_id: number;
  object_type: 'campaign' | 'adgroup';
  date: string;
  hour: number;
  impressions: number;
  clicks: number;
  cost: number;
}

// 仪表盘数据
export interface DashboardData {
  today: {
    impressions: number;
    clicks: number;
    cost: number;
    ctr: number;
    cpc: number;
  };
  yesterday: {
    impressions: number;
    clicks: number;
    cost: number;
  };
  active_campaigns: number;
  trend: Array<{
    report_date: string;
    impressions: number;
    clicks: number;
    cost: number;
  }>;
}

// API响应
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

// 分页响应
export interface PaginatedResponse<T> {
  total: number;
  list: T[];
}

// JWT Token
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}
