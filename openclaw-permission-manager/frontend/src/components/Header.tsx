import React, { useState, useEffect } from 'react';
import { Layout, Menu, Button, Dropdown, Avatar, Space, Typography } from 'antd';
import { UserOutlined, LogoutOutlined, SettingOutlined, TeamOutlined, SafetyCertificateOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

interface HeaderProps {
  currentPath?: string;
}

const Header: React.FC<HeaderProps> = ({ currentPath = '/' }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const userData = authService.getCurrentUser();
    setUser(userData);
  }, []);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const menuItems = [
    {
      key: '/',
      label: '仪表板',
      icon: <UserOutlined />,
    },
    {
      key: '/users',
      label: '用户管理',
      icon: <TeamOutlined />,
    },
    {
      key: '/templates',
      label: '权限模板',
      icon: <SafetyCertificateOutlined />,
    },
    {
      key: '/configs',
      label: '配置管理',
      icon: <SettingOutlined />,
    },
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: '个人信息',
      icon: <UserOutlined />,
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      label: '退出登录',
      icon: <LogoutOutlined />,
      onClick: handleLogout,
    },
  ];

  return (
    <AntHeader style={{ 
      background: '#fff', 
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <h1 style={{ 
          margin: 0, 
          fontSize: '20px', 
          color: '#1890ff',
          marginRight: '48px'
        }}>
          OpenClaw 权限管理系统
        </h1>
        
        <Menu
          mode="horizontal"
          selectedKeys={[currentPath]}
          items={menuItems}
          style={{ border: 'none' }}
          onClick={({ key }) => navigate(key)}
        />
      </div>

      <Space>
        {user && (
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Space style={{ cursor: 'pointer' }}>
              <Avatar 
                src={user.avatar_url} 
                icon={<UserOutlined />} 
                style={{ backgroundColor: '#1890ff' }}
              />
              <div>
                <Text strong>{user.nickname}</Text>
                <br />
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  {user.role}
                </Text>
              </div>
            </Space>
          </Dropdown>
        )}
      </Space>
    </AntHeader>
  );
};

export default Header;