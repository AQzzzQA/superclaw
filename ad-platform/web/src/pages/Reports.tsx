import React from 'react'
import { Card, Typography, Button, Space, Table, DatePicker, Select, Row, Col, Statistic } from 'antd'
import { ReloadOutlined, DownloadOutlined } from '@ant-design/icons'
import type { TableProps } from 'antd'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

interface ReportData {
  key: string
  date: string
  accountId: string
  campaignName: string
  impressions: number
  clicks: number
  cost: number
  ctr: string
  cpc: number
  conversions: number
  cvr: string
  roi: number
}

const ReportsPage = () => {
  const reportData: ReportData[] = [
    {
      key: '1',
      date: '2026-03-02',
      accountId: '100000001',
      campaignName: '夏季促销活动',
      impressions: 50000,
      clicks: 1000,
      cost: 1000.00,
      ctr: '2.0%',
      cpc: 1.0,
      conversions: 50,
      cvr: '5.0%',
      roi: 3.2,
    },
    {
      key: '2',
      date: '2026-03-01',
      accountId: '100000001',
      campaignName: '节日营销活动',
      impressions: 60000,
      clicks: 1200,
      cost: 1200.00,
      ctr: '2.0%',
      cpc: 1.0,
      conversions: 60,
      cvr: '5.0%',
      roi: 3.5,
    },
    {
      key: '3',
      date: '2026-02-28',
      accountId: '100000002',
      campaignName: '品牌推广计划',
      impressions: 40000,
      clicks: 800,
      cost: 800.00,
      ctr: '2.0%',
      cpc: 1.0,
      conversions: 40,
      cvr: '5.0%',
      roi: 2.8,
    },
  ]

  const columns: TableProps<ReportData>['columns'] = [
    { title: '日期', dataIndex: 'date', key: 'date', width: 120 },
    { title: '账户ID', dataIndex: 'accountId', key: 'accountId', width: 120 },
    { title: '计划名称', dataIndex: 'campaignName', key: 'campaignName', width: 150 },
    { title: '曝光量', dataIndex: 'impressions', key: 'impressions', width: 100, align: 'right' },
    { title: '点击量', dataIndex: 'clicks', key: 'clicks', width: 100, align: 'right' },
    { title: '消耗(元)', dataIndex: 'cost', key: 'cost', width: 120, align: 'right', render: (value) => `¥${value.toFixed(2)}` },
    { title: 'CTR', dataIndex: 'ctr', key: 'ctr', width: 80, align: 'center' },
    { title: 'CPC(元)', dataIndex: 'cpc', key: 'cpc', width: 100, align: 'right', render: (value) => `¥${value.toFixed(2)}` },
    { title: '转化数', dataIndex: 'conversions', key: 'conversions', width: 100, align: 'right' },
    { title: 'CVR', dataIndex: 'cvr', key: 'cvr', width: 80, align: 'center' },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', width: 100, align: 'right' },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <Title level={2}>数据报表</Title>
        <Text type="secondary">广告投放数据报表</Text>
      </div>

      {/* 筛选条件 */}
      <Card style={{ marginBottom: 24 }}>
        <Space size="large">
          <Space>
            <Text>日期范围：</Text>
            <RangePicker />
          </Space>
          <Space>
            <Text>账户：</Text>
            <Select style={{ width: 200 }} placeholder="选择账户" defaultValue="all">
              <Select.Option value="all">全部账户</Select.Option>
              <Select.Option value="100000001">测试账户1</Select.Option>
              <Select.Option value="100000002">测试账户2</Select.Option>
            </Select>
          </Space>
          <Space>
            <Text>维度：</Text>
            <Select style={{ width: 150 }} placeholder="选择维度" defaultValue="daily">
              <Select.Option value="daily">按天</Select.Option>
              <Select.Option value="campaign">按计划</Select.Option>
              <Select.Option value="account">按账户</Select.Option>
            </Select>
          </Space>
          <Space>
            <Button icon={<ReloadOutlined />}>刷新</Button>
            <Button type="primary" icon={<DownloadOutlined />}>导出报表</Button>
          </Space>
        </Space>
      </Card>

      {/* 汇总统计 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={4}>
          <Card>
            <Statistic title="总消耗" value={3000} prefix="¥" suffix="元" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="总曝光" value={150000} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="总点击" value={3000} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="平均CTR" value={2.0} suffix="%" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="平均CPC" value={1.0} prefix="¥" suffix="元" />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="总转化" value={150} />
          </Card>
        </Col>
      </Row>

      {/* 数据表格 */}
      <Card>
        <Table
          columns={columns}
          dataSource={reportData}
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条数据`,
          }}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  )
}

export default ReportsPage
