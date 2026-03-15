import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'

// 页面导入
import Login from './pages/auth/Login'
import Dashboard from './pages/dashboard/Dashboard'
import AccountList from './pages/account/AccountList'
import AccountAuthorize from './pages/account/AccountAuthorize'
import CampaignList from './pages/campaign/CampaignList'
import CampaignCreate from './pages/campaign/CampaignCreate'
import CampaignEdit from './pages/campaign/CampaignEdit'
import AdGroupList from './pages/adgroup/AdGroupList'
import AdGroupCreate from './pages/adgroup/AdGroupCreate'
import AdGroupEdit from './pages/adgroup/AdGroupEdit'
import CreativeList from './pages/creative/CreativeList'
import CreativeUpload from './pages/creative/CreativeUpload'
import DataMonitor from './pages/monitor/DataMonitor'
import ReportDaily from './pages/report/ReportDaily'
import ReportWeekly from './pages/report/ReportWeekly'
import ReportCustom from './pages/report/ReportCustom'
import CampaignAnalysis from './pages/analysis/CampaignAnalysis'
import CreativeAnalysis from './pages/analysis/CreativeAnalysis'
import AudienceAnalysis from './pages/analysis/AudienceAnalysis'
import UserSettings from './pages/settings/UserSettings'
import SystemSettings from './pages/settings/SystemSettings'
import PermissionManagement from './pages/settings/PermissionManagement'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 公开路由 */}
        <Route path="/login" element={<Login />} />

        {/* 主布局路由 */}
        <Route element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />

          {/* 账户管理 */}
          <Route path="/accounts" element={<AccountList />} />
          <Route path="/accounts/authorize" element={<AccountAuthorize />} />

          {/* 广告计划管理 */}
          <Route path="/campaigns" element={<CampaignList />} />
          <Route path="/campaigns/create" element={<CampaignCreate />} />
          <Route path="/campaigns/:id/edit" element={<CampaignEdit />} />

          {/* 广告组管理 */}
          <Route path="/ad-groups" element={<AdGroupList />} />
          <Route path="/ad-groups/create" element={<AdGroupCreate />} />
          <Route path="/ad-groups/:id/edit" element={<AdGroupEdit />} />

          {/* 广告创意管理 */}
          <Route path="/creatives" element={<CreativeList />} />
          <Route path="/creatives/upload" element={<CreativeUpload />} />

          {/* 数据监控 */}
          <Route path="/monitor" element={<DataMonitor />} />

          {/* 效果报表 */}
          <Route path="/reports/daily" element={<ReportDaily />} />
          <Route path="/reports/weekly" element={<ReportWeekly />} />
          <Route path="/reports/custom" element={<ReportCustom />} />

          {/* 数据分析 */}
          <Route path="/analysis/campaign" element={<CampaignAnalysis />} />
          <Route path="/analysis/creative" element={<CreativeAnalysis />} />
          <Route path="/analysis/audience" element={<AudienceAnalysis />} />

          {/* 设置 */}
          <Route path="/settings/user" element={<UserSettings />} />
          <Route path="/settings/system" element={<SystemSettings />} />
          <Route path="/settings/permissions" element={<PermissionManagement />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
