'use client';

import { useState } from 'react';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  AppstoreOutlined,
  BulbOutlined,
  TeamOutlined,
  BarChartOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';

const { Sider } = Layout;

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link href="/dashboard">仪表盘</Link>,
    },
    {
      key: 'campaign',
      icon: <AppstoreOutlined />,
      label: '广告管理',
      children: [
        {
          key: '/campaigns',
          label: <Link href="/campaigns">广告计划</Link>,
        },
        {
          key: '/adgroups',
          label: <Link href="/adgroups">广告组</Link>,
        },
        {
          key: '/creatives',
          label: <Link href="/creatives">创意</Link>,
        },
      ],
    },
    {
      key: '/audiences',
      icon: <TeamOutlined />,
      label: <Link href="/audiences">受众</Link>,
    },
    {
      key: '/reports',
      icon: <BarChartOutlined />,
      label: <Link href="/reports">报表</Link>,
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: <Link href="/settings">设置</Link>,
    },
  ];

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
      }}
    >
      <div
        style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'flex-start',
          padding: collapsed ? 0 : '0 24px',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <BulbOutlined style={{ fontSize: 24, color: '#fff' }} />
        {!collapsed && (
          <span style={{ marginLeft: 12, color: '#fff', fontWeight: 'bold' }}>
            DSP平台
          </span>
        )}
      </div>
      <div style={{ padding: '12px', textAlign: 'center' }}>
        <div
          onClick={() => setCollapsed(!collapsed)}
          style={{
            cursor: 'pointer',
            color: 'rgba(255,255,255,0.65)',
            transition: 'color 0.3s',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = '#fff')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(255,255,255,0.65)')}
        >
          {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        </div>
      </div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[pathname]}
        items={menuItems}
      />
    </Sider>
  );
};

export default Sidebar;
