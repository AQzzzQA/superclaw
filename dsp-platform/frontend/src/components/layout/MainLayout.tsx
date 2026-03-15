import { useState } from 'react'
import { Layout, Menu, theme } from 'antd'
import {
  DashboardOutlined,
  AccountBookOutlined,
  RocketOutlined,
  AppstoreOutlined,
  PictureOutlined,
  LineChartOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SettingOutlined,
  UserOutlined,
  TeamOutlined,
} from '@ant-design/icons'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'

const { Header, Sider, Content } = Layout

const MainLayout = () => {
  const [collapsed, setCollapsed] = useState(false)
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()
  const location = useLocation()
  const navigate = useNavigate()

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '数据总览',
    },
    {
      key: 'account-group',
      icon: <AccountBookOutlined />,
      label: '账户管理',
      children: [
        {
          key: '/accounts',
          label: '账户列表',
        },
        {
          key: '/accounts/authorize',
          label: '账户授权',
        },
      ],
    },
    {
      key: 'campaign-group',
      icon: <RocketOutlined />,
      label: '广告计划',
      children: [
        {
          key: '/campaigns',
          label: '计划列表',
        },
        {
          key: '/campaigns/create',
          label: '新建计划',
        },
      ],
    },
    {
      key: 'adgroup-group',
      icon: <AppstoreOutlined />,
      label: '广告组',
      children: [
        {
          key: '/ad-groups',
          label: '广告组列表',
        },
        {
          key: '/ad-groups/create',
          label: '新建广告组',
        },
      ],
    },
    {
      key: 'creative-group',
      icon: <PictureOutlined />,
      label: '广告创意',
      children: [
        {
          key: '/creatives',
          label: '创意列表',
        },
        {
          key: '/creatives/upload',
          label: '上传创意',
        },
      ],
    },
    {
      key: 'monitor-group',
      icon: <LineChartOutlined />,
      label: '数据监控',
      children: [
        {
          key: '/monitor',
          label: '实时监控',
        },
      ],
    },
    {
      key: 'report-group',
      icon: <FileTextOutlined />,
      label: '效果报表',
      children: [
        {
          key: '/reports/daily',
          label: '日报表',
        },
        {
          key: '/reports/weekly',
          label: '周报表',
        },
        {
          key: '/reports/custom',
          label: '自定义报表',
        },
      ],
    },
    {
      key: 'analysis-group',
      icon: <BarChartOutlined />,
      label: '数据分析',
      children: [
        {
          key: '/analysis/campaign',
          label: '计划分析',
        },
        {
          key: '/analysis/creative',
          label: '创意分析',
        },
        {
          key: '/analysis/audience',
          label: '人群分析',
        },
      ],
    },
    {
      key: 'settings-group',
      icon: <SettingOutlined />,
      label: '系统设置',
      children: [
        {
          key: '/settings/user',
          label: '用户设置',
        },
        {
          key: '/settings/system',
          label: '系统设置',
        },
        {
          key: '/settings/permissions',
          label: '权限管理',
        },
      ],
    },
  ]

  const getSelectedKeys = () => {
    return [location.pathname]
  }

  const getOpenKeys = () => {
    const path = location.pathname
    if (path.startsWith('/accounts')) return ['account-group']
    if (path.startsWith('/campaigns')) return ['campaign-group']
    if (path.startsWith('/ad-groups')) return ['adgroup-group']
    if (path.startsWith('/creatives')) return ['creative-group']
    if (path.startsWith('/monitor')) return ['monitor-group']
    if (path.startsWith('/reports')) return ['report-group']
    if (path.startsWith('/analysis')) return ['analysis-group']
    if (path.startsWith('/settings')) return ['settings-group']
    return []
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div
          style={{
            height: 32,
            margin: 16,
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: borderRadiusLG,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: collapsed ? '16px' : '18px',
          }}
        >
          {collapsed ? 'DSP' : 'DSP广告平台'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={getSelectedKeys()}
          defaultOpenKeys={getOpenKeys()}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: '0 24px',
            background: colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
            {menuItems.find((item) => item.key === location.pathname)?.label || '数据总览'}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <UserOutlined style={{ fontSize: '20px', cursor: 'pointer' }} />
            <TeamOutlined style={{ fontSize: '20px', cursor: 'pointer' }} />
          </div>
        </Header>
        <Content
          style={{
            margin: '24px 16px 0',
            padding: 24,
            minHeight: 280,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout
