import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Accounts from './pages/Accounts'
import Campaigns from './pages/Campaigns'
import Creatives from './pages/Creatives'
import Reports from './pages/Reports'
import Conversions from './pages/Conversions'
import Targeting from './pages/Targeting'
import Monitoring from './pages/Monitoring'
import Bidding from './pages/Bidding'
import Settings from './pages/Settings'
import Profile from './pages/Profile'

const { Content } = Layout

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sidebar />
      <Layout>
        <Header />
        <Content style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/accounts" element={<Accounts />} />
            <Route path="/campaigns" element={<Campaigns />} />
            <Route path="/creatives" element={<Creatives />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/conversions" element={<Conversions />} />
            <Route path="/targeting" element={<Targeting />} />
            <Route path="/monitoring" element={<Monitoring />} />
            <Route path="/bidding" element={<Bidding />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  )
}

export default App
