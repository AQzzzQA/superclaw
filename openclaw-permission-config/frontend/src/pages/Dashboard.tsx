import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Button, Table, Tag, Alert } from 'antd';
import { 
  TeamOutlined, 
  SettingOutlined, 
  SafetyOutlined, 
  FileTextOutlined,
  UserAddOutlined,
  TemplateOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    total_users: 0,
    admin_users: 0,
    templates_count: 4,
    system_status: 'healthy',
    last_update: '2026-03-13 15:00'
  });

  // 模拟统计数据
  useEffect(() => {
    setLoading(true);
    // 这里可以调用真实的API获取统计数据
    setTimeout(() => {
      setStats({
        total_users: 8,
        admin_users: 1,
        templates_count: 4,
        system_status: 'healthy',
        last_update: '2026-03-13 15:00'
      });
      setLoading(false);
    }, 1000);
  }, []);

  const quickActions = [
    {
      title: '用户管理',
      description: '管理QQ用户权限和角色',
      icon: <UserAddOutlined />,
      color: '#1890ff',
      action: () => navigate('/users')
    },
    {
      title: '权限配置',
      description: '配置权限级别和访问控制',
      icon: <SettingOutlined />,
      color: '#52c41a',
      action: () => navigate('/permissions')
    },
    {
      title: '模板管理',
      description: '创建和管理权限模板',
      icon: <TemplateOutlined />,
      color: '#faad14',
      action: () => navigate('/templates')
    },
    {
      title: '配置导出',
      description: '导出和应用配置文件',
      icon: <FileTextOutlined />,
      color: '#722ed1',
      action: () => navigate('/config')
    }
  ];

  const recentActivities = [
    {
      id: 1,
      user: '用户_123456789',
      action: '权限更新',
      target: '普通用户 → 高级用户',
      time: '2小时前',
      type: 'success'
    },
    {
      id: 2,
      user: '系统管理员',
      action: '模板创建',
      target: '编辑者模板',
      time: '1天前',
      type: 'info'
    },
    {
      id: 3,
      user: '用户_987654321',
      action: '配置查看',
      target: '查看权限配置',
      time: '2天前',
      type: 'normal'
    }
  ];

  const columns = [
    {
      title: '用户',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: '操作',
      dataIndex: 'action',
      key: 'action',
    },
    {
      title: '目标',
      dataIndex: 'target',
      key: 'target',
    },
    {
      title: '时间',
      dataIndex: 'time',
      key: 'time',
    },
    {
      title: '状态',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const statusMap = {
          success: <Tag color="success">成功</Tag>,
          info: <Tag color="blue">信息</Tag>,
          normal: <Tag color="default">正常</Tag>,
          error: <Tag color="error">错误</Tag>
        };
        return statusMap[type as keyof typeof statusMap] || <Tag>正常</Tag>;
      }
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1>OpenClaw 权限配置管理</h1>
        <p style={{ color: '#666', marginTop: 8 }}>
          欢迎使用OpenClaw权限配置可视化工具，您可以在这里管理QQ用户权限和配置文件。
        </p>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="用户总数"
              value={stats.total_users}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="管理员用户"
              value={stats.admin_users}
              prefix={<SafetyOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="权限模板"
              value={stats.templates_count}
              prefix={<SettingOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="系统状态"
              value={stats.system_status === 'healthy' ? '正常' : '异常'}
              prefix={<FileTextOutlined />}
              valueStyle={{ 
                color: stats.system_status === 'healthy' ? '#52c41a' : '#ff4d4f' 
              }}
            />
          </Card>
        </Col>
      </Row>

      {/* 快捷操作 */}
      <Card title="快捷操作" style={{ marginBottom: 24 }}>
        <Row gutter={[16, 16]}>
          {quickActions.map((action, index) => (
            <Col span={6} key={index}>
              <Button
                type="dashed"
                style={{ 
                  width: '100%', 
                  height: 100,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  background: action.color + '10',
                  borderColor: action.color,
                  color: action.color
                }}
                onClick={action.action}
              >
                {action.icon}
                <div style={{ marginTop: 8, fontWeight: 500 }}>
                  {action.title}
                </div>
                <div style={{ fontSize: 12, color: '#666', marginTop: 4 }}>
                  {action.description}
                </div>
              </Button>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 系统提醒 */}
      {stats.system_status === 'healthy' ? (
        <Alert
          message="系统运行正常"
          description="所有服务运行正常，没有发现异常。"
          type="success"
          showIcon
          style={{ marginBottom: 24 }}
        />
      ) : (
        <Alert
          message="系统警告"
          description="发现系统异常，请检查相关配置。"
          type="warning"
          showIcon
          style={{ marginBottom: 24 }}
        />
      )}

      {/* 最近活动 */}
      <Card title="最近活动">
        <Table
          dataSource={recentActivities}
          columns={columns}
          rowKey="id"
          pagination={false}
          size="small"
        />
      </Card>
    </div>
  );
};

export default Dashboard;