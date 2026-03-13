import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Space } from 'antd';
import { UserOutlined, TeamOutlined, SettingOutlined, SafetyCertificateOutlined } from '@ant-design/icons';
import { userService } from '../services/userService';
import { authService } from '../services/authService';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    adminUsers: 0,
    normalUsers: 0,
    readonlyUsers: 0,
  });
  const [recentUsers, setRecentUsers] = useState<any[]>([]);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    // Get current user
    const currentUser = localStorage.getItem('user');
    if (currentUser) {
      setUser(JSON.parse(currentUser));
    }

    // Load dashboard data
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load users
      const usersResponse = await userService.getAllUsers();
      const users = usersResponse.data;
      
      setStats({
        totalUsers: users.length,
        adminUsers: users.filter(u => u.role === 'admin').length,
        normalUsers: users.filter(u => u.role === 'user').length,
        readonlyUsers: users.filter(u => u.role === 'readonly').length,
      });

      // Get recent users
      setRecentUsers(users.slice(0, 5));
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const columns = [
    {
      title: 'QQ号码',
      dataIndex: 'qq_number',
      key: 'qq_number',
    },
    {
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname',
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role: string) => {
        const roleColors = {
          admin: 'red',
          user: 'blue',
          readonly: 'green',
        };
        return <Tag color={roleColors[role as keyof typeof roleColors]}>{role}</Tag>;
      },
    },
    {
      title: '权限数量',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: string[]) => permissions.length,
    },
    {
      title: '注册时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>仪表板</h1>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总用户数"
              value={stats.totalUsers}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="管理员"
              value={stats.adminUsers}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="普通用户"
              value={stats.normalUsers}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="只读用户"
              value={stats.readonlyUsers}
              prefix={<SafetyCertificateOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="最近注册用户" style={{ marginBottom: 24 }}>
        <Table
          dataSource={recentUsers}
          columns={columns}
          rowKey="id"
          pagination={false}
        />
      </Card>

      <Card title="系统信息">
        <Space direction="vertical" size="large">
          <div>
            <strong>当前用户:</strong> {user?.nickname} ({user?.qq_number})
          </div>
          <div>
            <strong>用户角色:</strong> 
            <Tag color={user?.role === 'admin' ? 'red' : user?.role === 'readonly' ? 'green' : 'blue'}>
              {user?.role}
            </Tag>
          </div>
          <div>
            <strong>权限数量:</strong> {user?.permissions?.length || 0}
          </div>
          <div>
            <strong>系统版本:</strong> 1.0.0
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default Dashboard;