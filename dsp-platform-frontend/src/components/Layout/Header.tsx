'use client';

import { Layout, Dropdown, Avatar, Button } from 'antd';
import { UserOutlined, LogoutOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'next/navigation';

const { Header } = Layout;

const AppHeader = () => {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const items = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      danger: true,
      onClick: () => {
        logout();
        router.push('/login');
      },
    },
  ];

  return (
    <Header
      style={{
        padding: '0 24px',
        background: '#fff',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginLeft: 200, // Sidebar width
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      }}
    >
      <div />
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <span>{user?.username}</span>
        <Dropdown menu={{ items }} placement="bottomRight">
          <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
        </Dropdown>
      </div>
    </Header>
  );
};

export default AppHeader;
