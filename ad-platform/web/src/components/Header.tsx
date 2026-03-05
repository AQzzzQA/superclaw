import React from 'react'
import { Layout, Avatar, Dropdown } from 'antd'
import { SettingOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { Modal } from 'antd'

const { Header } = Layout

const HeaderComponent: React.FC = () => {
  const navigate = useNavigate()

  const userMenuItems = [
    { key: '1', label: '系统设置', icon: <SettingOutlined />, onClick: () => navigate('/settings') },
    { key: '2', label: '个人中心', icon: <UserOutlined />, onClick: () => navigate('/profile') },
    { type: 'divider' as const },
    {
      key: '3',
      label: '退出登录',
      icon: <LogoutOutlined />,
      onClick: () => Modal.confirm({ title: '确认退出', onOk: () => navigate('/login') }),
      danger: true,
    },
  ]

  return (
    <Header style={{ background: 'white', padding: '0 24px', display: 'flex', alignItems: 'center', borderBottom: '1px solid #F0F0F0' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginLeft: 'auto' }}>
        <Avatar style={{ background: '#1677FF' }}>管</Avatar>
        <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
          <span style={{ cursor: 'pointer' }}>管理员</span>
        </Dropdown>
      </div>
    </Header>
  )
}

export default HeaderComponent
