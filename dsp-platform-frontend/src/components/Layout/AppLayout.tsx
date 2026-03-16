'use client';

import { Layout } from 'antd';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Sidebar from '@/components/Layout/Sidebar';
import AppHeader from '@/components/Layout/Header';

const { Content } = Layout;

const AppLayout = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const router = useRouter();

  // 路由守卫
  useEffect(() => {
    if (!isAuthenticated && pathname !== '/login') {
      router.push('/login');
    }
  }, [isAuthenticated, pathname, router]);

  // 登录页不需要布局
  if (pathname === '/login') {
    return <>{children}</>;
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sidebar />
      <Layout style={{ marginLeft: 200 }}>
        <AppHeader />
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            minHeight: 280,
            background: '#f0f2f5',
            overflow: 'auto',
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
