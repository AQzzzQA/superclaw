import { useState } from 'react'
import { Card, Form, Select, DatePicker, Button, Table, Space, Checkbox } from 'antd'
import { DownloadOutlined } from '@ant-design/icons'
import { formatNumber, formatCurrency, formatPercent } from '../../utils/format'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

const ReportCustom = () => {
  const [form] = Form.useForm()

  const dimensions = [
    { label: '日期', value: 'date' },
    { label: '平台', value: 'platform' },
    { label: '计划', value: 'campaign' },
    { label: '广告组', value: 'adgroup' },
    { label: '创意', value: 'creative' },
  ]

  const metrics = [
    { label: '曝光量', value: 'impressions' },
    { label: '点击数', value: 'clicks' },
    { label: 'CTR', value: 'ctr' },
    { label: '消耗', value: 'cost' },
    { label: '转化数', value: 'conversions' },
    { label: 'CPA', value: 'cpa' },
    { label: 'ROAS', value: 'roas' },
  ]

  const mockData = [
    { date: '2026-03-15', platform: '抖音', campaign: '计划A', adgroup: '广告组1', creative: '创意X', impressions: 50000, clicks: 1500, ctr: 3, cost: 3500, conversions: 75, cpa: 46.67, roas: 4.2 },
    { date: '2026-03-15', platform: '抖音', campaign: '计划A', adgroup: '广告组1', creative: '创意Y', impressions: 45000, clicks: 1350, ctr: 3, cost: 3150, conversions: 68, cpa: 46.32, roas: 4.1 },
    { date: '2026-03-15', platform: '快手', campaign: '计划B', adgroup: '广告组2', creative: '创意Z', impressions: 38000, clicks: 1140, ctr: 3, cost: 2660, conversions: 57, cpa: 46.67, roas: 3.9 },
  ]

  const columns = [
    { title: '日期', dataIndex: 'date', key: 'date' },
    { title: '平台', dataIndex: 'platform', key: 'platform' },
    { title: '计划', dataIndex: 'campaign', key: 'campaign' },
    { title: '广告组', dataIndex: 'adgroup', key: 'adgroup' },
    { title: '创意', dataIndex: 'creative', key: 'creative' },
    {
      title: '曝光量',
      dataIndex: 'impressions',
      key: 'impressions',
      render: formatNumber,
    },
    {
      title: '点击数',
      dataIndex: 'clicks',
      key: 'clicks',
      render: formatNumber,
    },
    {
      title: 'CTR',
      dataIndex: 'ctr',
      key: 'ctr',
      render: (value: number) => formatPercent(value),
    },
    {
      title: '消耗',
      dataIndex: 'cost',
      key: 'cost',
      render: formatCurrency,
    },
    {
      title: '转化数',
      dataIndex: 'conversions',
      key: 'conversions',
      render: formatNumber,
    },
    {
      title: 'CPA',
      dataIndex: 'cpa',
      key: 'cpa',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'ROAS',
      dataIndex: 'roas',
      key: 'roas',
      render: (value: number) => value.toFixed(2),
    },
  ]

  const handleGenerate = () => {
    form.validateFields().then((values) => {
      console.log('生成报表:', values)
    })
  }

  return (
    <div>
      <Card title="自定义报表" style={{ marginBottom: 16 }}>
        <Form form={form} layout="vertical">
          <Form.Item label="报表周期" name="dateRange" rules={[{ required: true }]}>
            <RangePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item label="筛选维度" name="dimensions" rules={[{ required: true }]}>
            <Select mode="multiple" placeholder="选择维度" options={dimensions} />
          </Form.Item>

          <Form.Item label="展示指标" name="metrics" rules={[{ required: true }]}>
            <Select mode="multiple" placeholder="选择指标" options={metrics} />
          </Form.Item>

          <Space>
            <Button type="primary" onClick={handleGenerate}>生成报表</Button>
            <Button icon={<DownloadOutlined />}>导出报表</Button>
          </Space>
        </Form>
      </Card>

      <Card title="报表数据">
        <Table
          columns={columns}
          dataSource={mockData}
          rowKey={(record) => `${record.date}-${record.campaign}-${record.creative}`}
          scroll={{ x: 1500 }}
        />
      </Card>
    </div>
  )
}

export default ReportCustom
