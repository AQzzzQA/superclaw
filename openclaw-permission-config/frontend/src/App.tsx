import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, ConfigProvider, theme } from 'antd';
import './App.css';

// 导入页面组件
import Dashboard from './pages/Dashboard';
import UserManagement from './pages/UserManagement';
import PermissionConfig from './pages/PermissionConfig';
import TemplateManagement from './pages/TemplateManagement';
import ConfigExport from './pages/ConfigExport';
import SystemStatus from './pages/SystemStatus';

// 导入布局组件
import { MainLayout } from './components/Layout';
import { LoginProvider } from './contexts/LoginContext';

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <LoginProvider>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
          },
        }}
      >
        <Router>
          <MainLayout>
            <Content style={{ 
              padding: '24px', 
              minHeight: 'calc(100vh - 134px)' 
            }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/users" element={<UserManagement />} />
                <Route path="/permissions" element={<PermissionConfig />} />
                <Route path="/templates" element={<TemplateManagement />} />
                <Route path="/config" element={<ConfigExport />} />
                <Route path="/status" element={<SystemStatus />} />
              </Routes>
            </Content>
            <Footer style={{ textAlign: 'center', backgroundColor: '#f0f2f5' }}>
              OpenClaw 权限配置可视化工具 ©2026 - 安全、智能、易用
            </Footer>
          </MainLayout>
        </Router>
      </ConfigProvider>
    </LoginProvider>
  );
}

export default App;