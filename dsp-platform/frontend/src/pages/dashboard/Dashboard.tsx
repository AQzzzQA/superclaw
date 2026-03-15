import { Row, Col, Statistic, Card, Space } from 'antd'
import {
  EyeOutlined,
  ClickOutlined,
  DollarOutlined,
  ShoppingCartOutlined,
} from '@ant-design/icons'
import { LineChart, BarChart, PieChart } from '../../components/charts'
import { formatNumber, formatCurrency } from '../../utils/format'
import dayjs from 'dayjs'

const Dashboard = () => {
  // 模拟数据
  const stats = {
    impressions: 1234567,
    clicks: 45678,
    cost: 123456.78,
    conversions: 1234,
  }

  const trendData = [
    { name: '00:00', value: 120 },
    { name: '04:00', value: 80 },
    { name: '08:00', value: 320 },
    { name: '12:00', value: 480 },
    { name: '16:00', value: 520 },
    { name: '20:00', value: 380 },
    { name: '23:59', value: 180 },
  ]

  const platformData = [
    { name: '抖音', value: 45 },
    { name: '快手', value: 30 },
    { name: 'B站', value: 15 },
    { name: '微博', value: 8 },
    { name: '小红书', value: 2 },
  ]

  const campaignPerformance = [
    { name: '计划A', value: 89 },
    { name: '计划B', value: 76 },
    { name: '计划C', value: 65 },
    { name: '计划D', value: 54 },
    { name: '计划E', value: 43 },
  ]

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>数据总览</h2>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总曝光量"
              value={stats.impressions}
              prefix={<EyeOutlined />}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总点击数"
              value={stats.clicks}
              prefix={<ClickOutlined />}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总消耗"
              value={stats.cost}
              prefix={<DollarOutlined />}
              formatter={(value) => formatCurrency(Number(value))}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总转化数"
              value={stats.conversions}
              prefix={<ShoppingCartOutlined />}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 图表区域 */}
      <Row gutter={16}>
        <Col span={16}>
          <Card title="今日消耗趋势" style={{ marginBottom: 16 }}>
            <LineChart
              title="消耗（元）"
              data={trendData}
              xKey="name"
              yKey="value"
              color="#1890ff"
              showArea
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="平台占比">
            <PieChart
              data={platformData}
              colors={['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card title="计划ROI排名">
            <BarChart
              title="ROI"
              data={campaignPerformance}
              color="#52c41a"
              horizontal
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard
