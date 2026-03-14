import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Progress, Table, Select, DatePicker, Button, Space, Tag, Alert } from 'antd'
import { ReloadOutlined, AlertOutlined, CheckCircleOutlined, WarningOutlined } from '@ant-design/icons'
import type { TableProps } from 'antd'

const { Option } = Select

interface MonitoringData {
  key: string
  campaignId: string
  campaignName: string
  status: string
  spend: number
  impressions: number
  clicks: number
  ctr: number
  cpc: number
  conversions: number
  cvr: number
  roi: number
  alertLevel: string
}

const MonitoringPage = () => {
  const [loading, setLoading] = useState(false)
  const [timeRange, setTimeRange] = useState('today')

  const monitoringData: MonitoringData[] = [
    {
      key: '1',
      campaignId: '100001',
      campaignName: '夏季促销活动',
      status: 'running',
      spend: 2500.00,
      impressions: 125000,
      clicks: 2500,
      ctr: 2.0,
      cpc: 1.0,
      conversions: 125,
      cvr: 5.0,
      roi: 3.2,
      alertLevel: 'warning',
    },
    {
      key: '2',
      campaignId: '100002',
      campaignName: '节日营销活动',
      status: 'paused',
      spend: 1800.00,
      impressions: 90000,
      clicks: 1800,
      ctr: 2.0,
      cpc: 1.0,
      conversions: 90,
      cvr: 5.0,
      roi: 2.8,
      alertLevel: 'normal',
    },
    {
      key: '3',
      campaignId: '100003',
      campaignName: '品牌推广计划',
      status: 'running',
      spend: 3200.00,
      impressions: 160000,
      clicks: 3200,
      ctr: 2.0,
      cpc: 1.0,
      conversions: 160,
      cvr: 5.0,
      roi: 4.1,
      alertLevel: 'error',
    },
  ]

  const columns: TableProps<MonitoringData>['columns'] = [
    { title: '计划ID', dataIndex: 'campaignId', key: 'campaignId', width: 100 },
    { title: '计划名称', dataIndex: 'campaignName', key: 'campaignName', width: 150 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => {
        const statusMap: Record<string, { text: string, color: string }> = {
          running: { text: '运行中', color: 'green' },
          paused: { text: '已暂停', color: 'red' },
          pending: { text: '待审核', color: 'orange' },
        }
        const s = statusMap[status] || { text: status, color: 'default' }
        return <Tag color={s.color}>{s.text}</Tag>
      },
    },
    { title: '消耗(元)', dataIndex: 'spend', key: 'spend', width: 100, align: 'right', render: (v) => `¥${v.toFixed(2)}` },
    { title: '曝光量', dataIndex: 'impressions', key: 'impressions', width: 100, align: 'right' },
    { title: '点击量', dataIndex: 'clicks', key: 'clicks', width: 100, align: 'right' },
    { title: 'CTR(%)', dataIndex: 'ctr', key: 'ctr', width: 80, align: 'center' },
    { title: 'CPC(元)', dataIndex: 'cpc', key: 'cpc', width: 100, align: 'right', render: (v) => `¥${v.toFixed(2)}` },
    { title: '转化数', dataIndex: 'conversions', key: 'conversions', width: 100, align: 'right' },
    { title: 'CVR(%)', dataIndex: 'cvr', key: 'cvr', width: 80, align: 'center' },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', width: 80, align: 'center' },
    {
      title: '告警等级',
      dataIndex: 'alertLevel',
      key: 'alertLevel',
      width: 100,
      render: (level: string) => {
        const levelMap: Record<string, { icon: any, color: string, text: string }> = {
          error: { icon: <AlertOutlined />, color: 'red', text: '严重' },
          warning: { icon: <WarningOutlined />, color: 'orange', text: '警告' },
          normal: { icon: <CheckCircleOutlined />, color: 'green', text: '正常' },
        }
        const l = levelMap[level] || levelMap.normal
        return <Tag icon={l.icon} color={l.color}>{l.text}</Tag>
      },
    },
  ]

  const handleRefresh = () => {
    setLoading(true)
    setTimeout(() => setLoading(false), 1000)
  }

  useEffect(() => {
    const interval = setInterval(handleRefresh, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <h2>实时监控</h2>
        <p style={{ color: '#666' }}>广告投放实时监控与告警</p>
      </div>

      {/* 实时统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={4}>
          <Card>
            <Statistic
              title="实时消耗"
              value={7500}
              prefix="¥"
              suffix="元"
              valueStyle={{ color: '#1677FF' }}
            />
            <Progress percent={75} status="active" strokeColor="#1677FF" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="实时曝光"
              value={375000}
              valueStyle={{ color: '#52C41A' }}
            />
            <Progress percent={60} status="active" strokeColor="#52C41A" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="实时点击"
              value={7500}
              valueStyle={{ color: '#FA8C16' }}
            />
            <Progress percent={65} status="active" strokeColor="#FA8C16" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="实时转化"
              value={375}
              valueStyle={{ color: '#722ED1' }}
            />
            <Progress percent={50} status="active" strokeColor="#722ED1" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="CTR"
              value={2.0}
              suffix="%"
              valueStyle={{ color: '#EB2F96' }}
            />
            <Progress percent={80} status="active" strokeColor="#EB2F96" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="CVR"
              value={5.0}
              suffix="%"
              valueStyle={{ color: '#13C2C2' }}
            />
            <Progress percent={55} status="active" strokeColor="#13C2C2" />
          </Card>
        </Col>
      </Row>

      {/* 告警信息 */}
      <Card style={{ marginBottom: 24 }}>
        <Alert
          message="告警提示"
          description="检测到 2 个计划消耗异常，1 个计划点击率下降，请及时处理！"
          type="warning"
          showIcon
          closable
        />
      </Card>

      {/* 筛选和操作 */}
      <Card style={{ marginBottom: 16 }}>
        <Space size="large">
          <Space>
            <span>时间范围：</span>
            <Select value={timeRange} onChange={setTimeRange} style={{ width: 150 }}>
              <Option value="today">今日</Option>
              <Option value="week">本周</Option>
              <Option value="month">本月</Option>
            </Select>
          </Space>
          <Space>
            <span>告警等级：</span>
            <Select defaultValue="all" style={{ width: 120 }}>
              <Option value="all">全部</Option>
              <Option value="error">严重</Option>
              <Option value="warning">警告</Option>
              <Option value="normal">正常</Option>
            </Select>
          </Space>
          <Space>
            <span>计划状态：</span>
            <Select defaultValue="all" style={{ width: 120 }}>
              <Option value="all">全部</Option>
              <Option value="running">运行中</Option>
              <Option value="paused">已暂停</Option>
            </Select>
          </Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={loading}>
            刷新
          </Button>
        </Space>
      </Card>

      {/* 监控数据表格 */}
      <Card>
        <Table
          columns={columns}
          dataSource={monitoringData}
          loading={loading}
          pagination={{ pageSize: 20 }}
          scroll={{ x: 1400 }}
          rowClassName={(record) => {
            if (record.alertLevel === 'error') return 'error-row'
            if (record.alertLevel === 'warning') return 'warning-row'
            return ''
          }}
        />
        <style>{`
          .error-row { background-color: #fff1f0; }
          .warning-row { background-color: #fffbe6; }
        `}</style>
      </Card>
    </div>
  )
}

export default MonitoringPage
