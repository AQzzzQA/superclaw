import { Card, Row, Col, Statistic } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'
import { formatNumber, formatCurrency, formatPercent } from '../../utils/format'
import { LineChart, BarChart, PieChart } from '../../components/charts'

const ReportWeekly = () => {
  const currentWeekData = {
    impressions: 956000,
    clicks: 27100,
    cost: 66300,
    conversions: 1400,
    roas: 3.85,
  }

  const lastWeekData = {
    impressions: 823000,
    clicks: 24100,
    cost: 58900,
    conversions: 1200,
    roas: 3.62,
  }

  const trendData = [
    { name: '周一', value: 8800 },
    { name: '周二', value: 9200 },
    { name: '周三', value: 8900 },
    { name: '周四', value: 9800 },
    { name: '周五', value: 10500 },
    { name: '周六', value: 14200 },
    { name: '周日', value: 14900 },
  ]

  const platformData = [
    { name: '抖音', value: 45 },
    { name: '快手', value: 30 },
    { name: 'B站', value: 15 },
    { name: '微博', value: 8 },
    { name: '小红书', value: 2 },
  ]

  const renderChange = (current: number, last: number) => {
    const change = ((current - last) / last) * 100
    if (change > 0) {
      return (
        <span style={{ color: '#52c41a' }}>
          <ArrowUpOutlined /> {change.toFixed(2)}%
        </span>
      )
    } else if (change < 0) {
      return (
        <span style={{ color: '#ff4d4f' }}>
          <ArrowDownOutlined /> {Math.abs(change).toFixed(2)}%
        </span>
      )
    }
    return <span style={{ color: '#999' }}>-</span>
  }

  return (
    <div>
      <Card title="周报表" style={{ marginBottom: 16 }}>
        <p>本周：2026-03-09 至 2026-03-15</p>
      </Card>

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总曝光量"
              value={currentWeekData.impressions}
              formatter={(value) => formatNumber(Number(value))}
              prefix={renderChange(currentWeekData.impressions, lastWeekData.impressions)}
            />
            <div style={{ fontSize: 12, color: '#999', marginTop: 8 }}>
              上周：{formatNumber(lastWeekData.impressions)}
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总点击数"
              value={currentWeekData.clicks}
              formatter={(value) => formatNumber(Number(value))}
              prefix={renderChange(currentWeekData.clicks, lastWeekData.clicks)}
            />
            <div style={{ fontSize: 12, color: '#999', marginTop: 8 }}>
              上周：{formatNumber(lastWeekData.clicks)}
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总消耗"
              value={currentWeekData.cost}
              formatter={(value) => formatCurrency(Number(value))}
              prefix={renderChange(currentWeekData.cost, lastWeekData.cost)}
            />
            <div style={{ fontSize: 12, color: '#999', marginTop: 8 }}>
              上周：{formatCurrency(lastWeekData.cost)}
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总转化数"
              value={currentWeekData.conversions}
              formatter={(value) => formatNumber(Number(value))}
              prefix={renderChange(currentWeekData.conversions, lastWeekData.conversions)}
            />
            <div style={{ fontSize: 12, color: '#999', marginTop: 8 }}>
              上周：{formatNumber(lastWeekData.conversions)}
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={16}>
          <Card title="每日消耗趋势" style={{ marginBottom: 16 }}>
            <LineChart title="消耗（元）" data={trendData} showArea />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="平台占比" style={{ marginBottom: 16 }}>
            <PieChart
              data={platformData}
              colors={['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={24}>
          <Card title="关键指标对比">
            <BarChart
              title="ROAS"
              data={[
                { name: '本周', value: currentWeekData.roas },
                { name: '上周', value: lastWeekData.roas },
              ]}
              color="#52c41a"
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default ReportWeekly
