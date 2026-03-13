import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import UserManagement from './pages/UserManagement';
import PermissionTemplates from './pages/PermissionTemplates';
import ConfigManagement from './pages/ConfigManagement';
import LoginPage from './pages/LoginPage';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header />
      <Layout>
        <Content style={{ padding: '24px', margin: '0', minHeight: '280px' }}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<UserManagement />} />
            <Route path="/templates" element={<PermissionTemplates />} />
            <Route path="/configs" element={<ConfigManagement />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;