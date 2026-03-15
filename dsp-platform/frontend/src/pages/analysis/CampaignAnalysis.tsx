import { Card, Row, Col, Table, Select } from 'antd'
import { LineChart, BarChart, PieChart } from '../../components/charts'
import { formatNumber, formatCurrency, formatPercent } from '../../utils/format'

const CampaignAnalysis = () => {
  const topCampaigns = [
    { name: '计划A', impressions: 145000, clicks: 4100, cost: 10000, conversions: 215, roas: 4.1 },
    { name: '计划B', impressions: 120000, clicks: 3500, cost: 8500, conversions: 180, roas: 3.5 },
    { name: '计划C', impressions: 98000, clicks: 2800, cost: 6800, conversions: 140, roas: 3.2 },
    { name: '计划D', impressions: 85000, clicks: 2400, cost: 5800, conversions: 110, roas: 2.8 },
    { name: '计划E', impressions: 72000, clicks: 2000, cost: 4900, conversions: 90, roas: 2.5 },
  ]

  const performanceTrend = [
    { name: '周一', value: 3.2 },
    { name: '周二', value: 3.5 },
    { name: '周三', value: 3.4 },
    { name: '周四', value: 3.8 },
    { name: '周五', value: 4.0 },
    { name: '周六', value: 4.2 },
    { name: '周日', value: 4.1 },
  ]

  const platformPerformance = [
    { name: '抖音', value: 4.2 },
    { name: '快手', value: 3.8 },
    { name: 'B站', value: 3.5 },
    { name: '微博', value: 3.0 },
    { name: '小红书', value: 2.8 },
  ]

  const columns = [
    { title: '计划名称', dataIndex: 'name', key: 'name' },
    { title: '曝光量', dataIndex: 'impressions', key: 'impressions', render: formatNumber },
    { title: '点击数', dataIndex: 'clicks', key: 'clicks', render: formatNumber },
    { title: '消耗', dataIndex: 'cost', key: 'cost', render: formatCurrency },
    { title: '转化数', dataIndex: 'conversions', key: 'conversions', render: formatNumber },
    { title: 'ROAS', dataIndex: 'roas', key: 'roas', render: (v: number) => v.toFixed(2) },
  ]

  return (
    <div>
      <Card title="广告计划分析" style={{ marginBottom: 16 }}>
        <p>分析广告计划的表现，找出最佳投放策略</p>
      </Card>

      <Row gutter={16}>
        <Col span={16}>
          <Card title="ROAS趋势" style={{ marginBottom: 16 }}>
            <LineChart title="ROAS" data={performanceTrend} color="#52c41a" />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="平台表现排名" style={{ marginBottom: 16 }}>
            <BarChart title="ROAS" data={platformPerformance} horizontal color="#52c41a" />
          </Card>
        </Col>
      </Row>

      <Card title="TOP 5 计划表现">
        <Table
          columns={columns}
          dataSource={topCampaigns}
          rowKey="name"
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default CampaignAnalysis
