import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Typography, Space, Spin, Tag, Button } from 'antd'
import {
  EyeOutlined,
  CheckCircleOutlined,
  DollarOutlined,
  ReloadOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface RealtimeMetric {
  campaign_id: number
  campaign_name: string
  show_count: number
  click_count: number
  convert_count: number
  cost: number
  ctr: number
  cvr: number
  roi?: number
}

interface RealtimeData {
  metrics: RealtimeMetric[]
  summary: {
    total_show: number
    total_click: number
    total_convert: number
    total_cost: number
    avg_ctr: number
    avg_cvr: number
  }
  last_updated: string
}

const RealtimeMonitoringPage = () => {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<RealtimeData | null>(null)
  const [selectedCampaignId, setSelectedCampaignId] = useState<number>(100001)

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // 30秒刷新
    return () => clearInterval(interval)
  }, [selectedCampaignId])

  const fetchData = async () => {
    setLoading(true)
    try {
      // 模拟 API 调用
      await new Promise(resolve => setTimeout(resolve, 500))
      const mockData: RealtimeData = {
        metrics: [
          {
            campaign_id: 100001,
            campaign_name: '夏季促销活动',
            show_count: 12500,
            click_count: 250,
            convert_count: 12,
            cost: 125.0,
            ctr: 2.0,
            cvr: 4.8,
            roi: 3.2,
          },
        ],
        summary: {
          total_show: 12500,
          total_click: 250,
          total_convert: 12,
          total_cost: 125.0,
          avg_ctr: 2.0,
          avg_cvr: 4.8,
        },
        last_updated: new Date().toISOString(),
      }
      setData(mockData)
    } catch (error) {
      console.error('加载失败', error)
    } finally {
      setLoading(false)
    }
  }

  if (!data) {
    return (
      <div style={{ textAlign: 'center', padding: '48px' }}>
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2}>实时监控</Title>
          <Text type="secondary">实时追踪广告投放数据</Text>
        </div>
        <Button icon={<ReloadOutlined />} loading={loading} onClick={fetchData}>
          刷新
        </Button>
      </div>

      <Spin spinning={loading}>
        <Row gutter={[16, 16]}>
          <Col span={6}>
            <Card>
              <Statistic
                title="总曝光"
                value={data.summary.total_show}
                prefix={<EyeOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总点击"
                value={data.summary.total_click}
                prefix={<EyeOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总转化"
                value={data.summary.total_convert}
                prefix={<CheckCircleOutlined />}
                valueStyle={{ color: '#faad14' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总消耗"
                value={data.summary.total_cost}
                prefix="¥"
                suffix="元"
                precision={2}
                valueStyle={{ color: '#ff4d4f' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
          <Col span={12}>
            <Card title="点击率 (CTR)" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 48, fontWeight: 'bold', color: '#1890ff' }}>
                {data.summary.avg_ctr.toFixed(2)}%
              </div>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="转化率 (CVR)" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 48, fontWeight: 'bold', color: '#52c41a' }}>
                {data.summary.avg_cvr.toFixed(2)}%
              </div>
            </Card>
          </Col>
        </Row>

        <Card title="广告计划详情" style={{ marginTop: 24 }}>
          {data.metrics.map((metric) => (
            <div key={metric.campaign_id} style={{ marginBottom: 16 }}>
              <Row gutter={[16, 16]}>
                <Col span={8}>
                  <Text strong>广告计划:</Text> {metric.campaign_name}
                </Col>
                <Col span={4}>
                  <Text>曝光:</Text> {metric.show_count.toLocaleString()}
                </Col>
                <Col span={4}>
                  <Text>点击:</Text> {metric.click_count.toLocaleString()}
                </Col>
                <Col span={4}>
                  <Text>转化:</Text> {metric.convert_count}
                </Col>
                <Col span={4}>
                  <Text>消耗:</Text> ¥{metric.cost.toFixed(2)}
                </Col>
              </Row>
              <Row gutter={[16, 16]}>
                <Col span={8}>
                  <Text>CTR: <Tag color="blue">{metric.ctr.toFixed(2)}%</Tag></Text>
                  {' '}
                  <Text>CVR: <Tag color="green">{metric.cvr.toFixed(2)}%</Tag></Text>
                  {metric.roi && <Text> ROI: <Tag color="orange">{metric.roi.toFixed(2)}</Tag></Text>}
                </Col>
              </Row>
            </div>
          ))}
        </Card>

        <div style={{ textAlign: 'right', marginTop: 16, color: '#999' }}>
          <Text>最后更新: {new Date(data.last_updated).toLocaleString()}</Text>
        </div>
      </Spin>
    </div>
  )
}

export default RealtimeMonitoringPage
