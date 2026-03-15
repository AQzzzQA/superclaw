import { Card, Row, Col, Table } from 'antd'
import { BarChart, PieChart } from '../../components/charts'

const AudienceAnalysis = () => {
  const ageDistribution = [
    { name: '18-24岁', value: 25 },
    { name: '25-34岁', value: 35 },
    { name: '35-44岁', value: 22 },
    { name: '45-54岁', value: 12 },
    { name: '55岁以上', value: 6 },
  ]

  const genderDistribution = [
    { name: '男性', value: 48 },
    { name: '女性', value: 52 },
  ]

  const topInterests = [
    { name: '科技', users: 280000, conversions: 520, roas: 4.2 },
    { name: '时尚', users: 250000, conversions: 450, roas: 3.8 },
    { name: '美食', users: 220000, conversions: 380, roas: 3.5 },
    { name: '旅行', users: 190000, conversions: 320, roas: 3.3 },
    { name: '运动', users: 160000, conversions: 280, roas: 3.1 },
  ]

  const interestColumns = [
    { title: '兴趣标签', dataIndex: 'name', key: 'name' },
    { title: '覆盖用户', dataIndex: 'users', key: 'users', render: (v: number) => v.toLocaleString() },
    { title: '转化数', dataIndex: 'conversions', key: 'conversions', render: (v: number) => v.toLocaleString() },
    { title: 'ROAS', dataIndex: 'roas', key: 'roas', render: (v: number) => v.toFixed(2) },
  ]

  return (
    <div>
      <Card title="人群画像分析" style={{ marginBottom: 16 }}>
        <p>分析目标人群的特征和行为，优化定向策略</p>
      </Card>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="年龄分布" style={{ marginBottom: 16 }}>
            <BarChart title="占比 (%)" data={ageDistribution} color="#1890ff" />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="性别分布" style={{ marginBottom: 16 }}>
            <PieChart
              data={genderDistribution}
              colors={['#1890ff', '#eb2f96']}
            />
          </Card>
        </Col>
      </Row>

      <Card title="兴趣标签表现">
        <Table
          columns={interestColumns}
          dataSource={topInterests}
          rowKey="name"
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default AudienceAnalysis
