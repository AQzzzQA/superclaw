import { Card, Row, Col, Table } from 'antd'
import { LineChart, BarChart } from '../../components/charts'
import { formatNumber, formatCurrency, formatPercent } from '../../utils/format'

const CreativeAnalysis = () => {
  const topCreatives = [
    { name: '创意X', type: '视频', impressions: 88000, clicks: 2800, cost: 6800, conversions: 150, roas: 4.5 },
    { name: '创意Y', type: '图片', impressions: 75000, clicks: 2200, cost: 5300, conversions: 115, roas: 4.2 },
    { name: '创意Z', type: '轮播', impressions: 62000, clicks: 1800, cost: 4300, conversions: 90, roas: 3.9 },
    { name: '创意W', type: '图片', impressions: 55000, clicks: 1500, cost: 3600, conversions: 70, roas: 3.5 },
    { name: '创意V', type: '视频', impressions: 48000, clicks: 1200, cost: 2900, conversions: 55, roas: 3.2 },
  ]

  const ctrTrend = [
    { name: '周一', value: 2.8 },
    { name: '周二', value: 3.0 },
    { name: '周三', value: 2.9 },
    { name: '周四', value: 3.2 },
    { name: '周五', value: 3.5 },
    { name: '周六', value: 3.8 },
    { name: '周日', value: 3.6 },
  ]

  const typePerformance = [
    { name: '视频', value: 4.2 },
    { name: '图片', value: 3.5 },
    { name: '轮播', value: 3.2 },
  ]

  const columns = [
    { title: '创意名称', dataIndex: 'name', key: 'name' },
    { title: '类型', dataIndex: 'type', key: 'type' },
    { title: '曝光量', dataIndex: 'impressions', key: 'impressions', render: formatNumber },
    { title: '点击数', dataIndex: 'clicks', key: 'clicks', render: formatNumber },
    { title: '消耗', dataIndex: 'cost', key: 'cost', render: formatCurrency },
    { title: '转化数', dataIndex: 'conversions', key: 'conversions', render: formatNumber },
    { title: 'ROAS', dataIndex: 'roas', key: 'roas', render: (v: number) => v.toFixed(2) },
  ]

  return (
    <div>
      <Card title="广告创意分析" style={{ marginBottom: 16 }}>
        <p>分析不同创意素材的表现，优化创意策略</p>
      </Card>

      <Row gutter={16}>
        <Col span={16}>
          <Card title="CTR趋势" style={{ marginBottom: 16 }}>
            <LineChart title="CTR (%)" data={ctrTrend} color="#1890ff" />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="创意类型表现" style={{ marginBottom: 16 }}>
            <BarChart title="ROAS" data={typePerformance} horizontal color="#52c41a" />
          </Card>
        </Col>
      </Row>

      <Card title="TOP 5 创意表现">
        <Table
          columns={columns}
          dataSource={topCreatives}
          rowKey="name"
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default CreativeAnalysis
