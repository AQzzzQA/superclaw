import React from 'react'
import { Layout, Menu, Avatar, Dropdown } from 'antd'
import {
  DashboardOutlined,
  AccountBookOutlined,
  FileTextOutlined,
  PictureOutlined,
  BarChartOutlined,
  SwapOutlined,
  SettingOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import { Modal } from 'antd'

const { Sider } = Layout

const Sidebar: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { key: '/', label: '仪表盘', icon: <DashboardOutlined />, onClick: () => navigate('/') },
    { key: '/accounts', label: '账户管理', icon: <AccountBookOutlined />, onClick: () => navigate('/accounts') },
    { key: '/campaigns', label: '广告计划', icon: <FileTextOutlined />, onClick: () => navigate('/campaigns') },
    { key: '/creatives', label: '创意管理', icon: <PictureOutlined />, onClick: () => navigate('/creatives') },
    { key: '/reports', label: '数据报表', icon: <BarChartOutlined />, onClick: () => navigate('/reports') },
    { key: '/conversions', label: '转化追踪', icon: <SwapOutlined />, onClick: () => navigate('/conversions') },
    { type: 'divider' as const },
    { key: '/targeting', label: '定向投放', icon: <SwapOutlined />, onClick: () => navigate('/targeting') },
    { key: '/monitoring', label: '实时监控', icon: <SwapOutlined />, onClick: () => navigate('/monitoring') },
    { key: '/bidding', label: '出价策略', icon: <SwapOutlined />, onClick: () => navigate('/bidding') },
    { type: 'divider' as const },
    { key: '/settings', label: '系统设置', icon: <SettingOutlined />, onClick: () => navigate('/settings') },
    { key: '/profile', label: '个人中心', icon: <UserOutlined />, onClick: () => navigate('/profile') },
    { type: 'divider' as const },
    {
      key: 'logout',
      label: '退出登录',
      icon: <LogoutOutlined />,
      onClick: () => Modal.confirm({ title: '确认退出', onOk: () => navigate('/login') }),
      danger: true,
    },
  ]

  return (
    <Sider width={240} style={{ background: '#1677FF' }}>
      <div style={{ padding: '16px', color: 'white', fontSize: 20, fontWeight: 'bold' }}>
        广告平台
      </div>
      <Menu theme="dark" mode="inline" selectedKeys={[location.pathname]} items={menuItems} />
    </Sider>
  )
}

export default Sidebar
