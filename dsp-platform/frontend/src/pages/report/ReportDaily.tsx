import { useState } from 'react'
import { Card, DatePicker, Button, Table, Space } from 'antd'
import { DownloadOutlined, PrinterOutlined } from '@ant-design/icons'
import { LineChart, BarChart } from '../../components/charts'
import { formatNumber, formatCurrency, formatPercent, formatDate } from '../../utils/format'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

const ReportDaily = () => {
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().subtract(7, 'day'),
    dayjs(),
  ])

  const mockData = [
    { date: '2026-03-09', impressions: 120000, clicks: 3500, cost: 8500, conversions: 180, roas: 3.5 },
    { date: '2026-03-10', impressions: 135000, clicks: 3800, cost: 9200, conversions: 195, roas: 3.8 },
    { date: '2026-03-11', impressions: 128000, clicks: 3600, cost: 8800, conversions: 175, roas: 3.4 },
    { date: '2026-03-12', impressions: 142000, clicks: 4000, cost: 9800, conversions: 210, roas: 4.0 },
    { date: '2026-03-13', impressions: 150000, clicks: 4200, cost: 10500, conversions: 225, roas: 4.2 },
    { date: '2026-03-14', impressions: 138000, clicks: 3900, cost: 9500, conversions: 200, roas: 3.9 },
    { date: '2026-03-15', impressions: 145000, clicks: 4100, cost: 10000, conversions: 215, roas: 4.1 },
  ]

  const columns = [
    { title: '日期', dataIndex: 'date', key: 'date' },
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
      key: 'ctr',
      render: (record: any) => formatPercent((record.clicks / record.impressions) * 100),
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
      key: 'cpa',
      render: (record: any) => formatCurrency(record.cost / record.conversions),
    },
    {
      title: 'ROAS',
      dataIndex: 'roas',
      key: 'roas',
      render: (value: number) => value.toFixed(2),
    },
  ]

  const trendData = mockData.map((d) => ({ name: d.date, value: d.cost }))
  const roasData = mockData.map((d) => ({ name: d.date, value: d.roas }))

  return (
    <div>
      <Card
        title="日报表"
        extra={
          <Space>
            <RangePicker
              value={dateRange}
              onChange={(dates) => setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs])}
            />
            <Button icon={<DownloadOutlined />}>导出</Button>
            <Button icon={<PrinterOutlined />}>打印</Button>
          </Space>
        }
        style={{ marginBottom: 16 }}
      >
        <p>
          报表周期：{formatDate(dateRange[0])} 至 {formatDate(dateRange[1])}
        </p>
      </Card>

      <Card title="消耗趋势" style={{ marginBottom: 16 }}>
        <LineChart title="消耗（元）" data={trendData} showArea />
      </Card>

      <Card title="ROAS趋势" style={{ marginBottom: 16 }}>
        <LineChart title="ROAS" data={roasData} color="#52c41a" />
      </Card>

      <Card title="详细数据">
        <Table
          columns={columns}
          dataSource={mockData}
          rowKey="date"
          pagination={false}
          summary={(pageData) => {
            const totalImpressions = pageData.reduce((sum, record) => sum + record.impressions, 0)
            const totalClicks = pageData.reduce((sum, record) => sum + record.clicks, 0)
            const totalCost = pageData.reduce((sum, record) => sum + record.cost, 0)
            const totalConversions = pageData.reduce((sum, record) => sum + record.conversions, 0)

            return (
              <Table.Summary>
                <Table.Summary.Row>
                  <Table.Summary.Cell index={0}>合计</Table.Summary.Cell>
                  <Table.Summary.Cell index={1}>{formatNumber(totalImpressions)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={2}>{formatNumber(totalClicks)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={3}>{formatPercent((totalClicks / totalImpressions) * 100)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={4}>{formatCurrency(totalCost)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={5}>{formatNumber(totalConversions)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={6}>{formatCurrency(totalCost / totalConversions)}</Table.Summary.Cell>
                  <Table.Summary.Cell index={7}>-</Table.Summary.Cell>
                </Table.Summary.Row>
              </Table.Summary>
            )
          }}
        />
      </Card>
    </div>
  )
}

export default ReportDaily
