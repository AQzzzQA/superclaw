import React from 'react'
import { Card, Row, Col, Statistic, Typography, Space, Table, Tag, Progress, Button, Avatar, Dropdown, Menu } from 'antd'
import { UserOutlined, ShoppingCartOutlined, DollarOutlined, EyeOutlined, CheckCircleOutlined, SettingOutlined, LogoutOutlined } from '@ant-design/icons'

const { Title, Text } = Typography

interface DashboardStats {
  totalSpent: number
  totalImpressions: number
  totalClicks: number
  totalConversions: number
  ctr: number
  cvr: number
  roi: number
}

interface CampaignData {
  id: number
  name: string
  objective: string
  budget: number
  spent: number
  status: string
  ctr: number
  cvr: number
  roi: number
}

const Dashboard: React.FC = () => {
  const stats: DashboardStats = {
    totalSpent: 125000,
    totalImpressions: 650000,
    totalClicks: 13000,
    totalConversions: 650,
    ctr: 2.0,
    cvr: 5.0,
    roi: 3.2,
  }

  const campaigns: CampaignData[] = [
    {
      id: 1,
      name: '夏季促销活动',
      objective: '产品推广',
      budget: 100000,
      spent: 45000,
      status: 'enable',
      ctr: 2.5,
      cvr: 5.5,
      roi: 3.8,
    },
    {
      id: 2,
      name: '节日营销活动',
      objective: '应用推广',
      budget: 80000,
      spent: 35000,
      status: 'enable',
      ctr: 2.0,
      cvr: 4.8,
      roi: 3.2,
    },
    {
      id: 3,
      name: '新用户获取',
      objective: '网页转化',
      budget: 120000,
      spent: 28000,
      status: 'disable',
      ctr: 1.8,
      cvr: 4.2,
      roi: 2.9,
    },
  ]

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '计划名称', dataIndex: 'name', key: 'name', width: 200 },
    { 
      title: '推广目标', 
      dataIndex: 'objective', 
      key: 'objective', 
      width: 120,
      render: (obj: string) => <Tag color="purple">{obj}</Tag>
    },
    { title: '预算 (¥)', dataIndex: 'budget', key: 'budget', width: 120, render: (v: number) => v.toLocaleString() },
    { title: '消耗 (¥)', dataIndex: 'spent', key: 'spent', width: 120, render: (v: number) => v.toLocaleString() },
    { title: '进度', key: 'progress', width: 150, render: (_, record: CampaignData) => (
      <Progress percent={Math.round((record.spent / record.budget) * 100)} status={record.spent > record.budget ? 'exception' : 'normal'} />
    )},
    { title: 'CTR (%)', dataIndex: 'ctr', key: 'ctr', width: 100, render: (v: number) => v.toFixed(2) },
    { title: 'CVR (%)', dataIndex: 'cvr', key: 'cvr', width: 100, render: (v: number) => v.toFixed(2) },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', width: 100, render: (v: number) => v.toFixed(2) },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={status === 'enable' ? 'green' : 'red'}>
          {status === 'enable' ? '启用' : '暂停'}
        </Tag>
      ),
    },
  ]

  const handleLogout = () => {
    console.log('用户点击了退出登录')
  }

  const userMenu = (
    <Menu>
      <Menu.Item key="settings" icon={<SettingOutlined />}>系统设置</Menu.Item>
      <Menu.Item key="profile" icon={<UserOutlined />}>个人中心</Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout} danger>
        退出登录
      </Menu.Item>
    </Menu>
  )

  return (
    <div style={{ padding: 0, minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ background: 'white', padding: 24, marginBottom: 24 }}>
        <Title level={2} style={{ marginBottom: 16 }}>数据概览</Title>
        <Row gutter={[24, 24]}>
          <Col span={6}>
            <Card style={{ borderRadius: 8, textAlign: 'center', padding: 24 }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>💰</div>
              <Text type="secondary">今日消耗</Text>
              <div style={{ fontSize: 32, fontWeight: 'bold', marginTop: 8, color: '#FF7A45' }}>
                ¥{(stats.totalSpent / 1000).toFixed(0)}
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card style={{ borderRadius: 8, textAlign: 'center', padding: 24 }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>👁</div>
              <Text type="secondary">总曝光</Text>
              <div style={{ fontSize: 32, fontWeight: 'bold', marginTop: 8, color: '#95DE64' }}>
                {(stats.totalImpressions / 1000).toFixed(0)}K
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card style={{ borderRadius: 8, textAlign: 'center', padding: 24 }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>👆</div>
              <Text type="secondary">总点击</Text>
              <div style={{ fontSize: 32, fontWeight: 'bold', marginTop: 8, color: '#FFA940' }}>
                {(stats.totalClicks / 1000).toFixed(1)}K
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card style={{ borderRadius: 8, textAlign: 'center', padding: 24 }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>✅</div>
              <Text type="secondary">今日转化</Text>
              <div style={{ fontSize: 32, fontWeight: 'bold', marginTop: 8, color: '#52C41A' }}>
                {stats.totalConversions}
              </div>
            </Card>
          </Col>
        </Row>

        <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
          <Col span={12}>
            <Card title="点击率 (CTR)" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 48, fontWeight: 'bold', color: '#1677FF' }}>
                {stats.ctr.toFixed(2)}%
              </div>
              <Text type="secondary">行业平均: 1.8%</Text>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="转化率 (CVR)" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 48, fontWeight: 'bold', color: '#52C41A' }}>
                {stats.cvr.toFixed(2)}%
              </div>
              <Text type="secondary">行业平均: 3.5%</Text>
            </Card>
          </Col>
        </Row>
      </div>

      <div style={{ background: 'white', padding: 24, marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={3}>账户余额</Title>
          <Space>
            <Button>充值</Button>
            <Button>查看账单</Button>
          </Space>
        </div>
        <Row gutter={[24, 24]}>
          <Col span={6}>
            <Card>
              <Statistic title="账户总余额" value={5000} prefix="¥" />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="今日消耗" value={125} prefix="¥" />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="本月消耗" value={3500} prefix="¥" />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="预计可用天数" value={30} suffix="天" />
            </Card>
          </Col>
        </Row>
      </div>

      <div style={{ background: 'white', padding: 24 }}>
        <Title level={3} style={{ marginBottom: 16 }}>广告计划列表</Title>
        <Table
          columns={columns}
          dataSource={campaigns}
          rowKey="id"
          scroll={{ x: 1400 }}
          pagination={{ pageSize: 10 }}
        />
      </div>
    </div>
  )
}

export default Dashboard
