import { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, Space, Tag, Switch, message } from 'antd'
import { WifiOutlined, ClockCircleOutlined } from '@ant-design/icons'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../store/store'
import { toggleAutoRefresh } from '../../store/slices/monitorSlice'
import RealtimeChart from '../../components/charts/RealtimeChart'
import { formatNumber, formatCurrency, formatDateTime } from '../../utils/format'
import useWebSocket from '../../hooks/useWebSocket'

interface RealtimeStats {
  timestamp: string
  impressions: number
  clicks: number
  cost: number
  conversions: number
}

const DataMonitor = () => {
  const dispatch = useDispatch()
  const autoRefresh = useSelector((state: RootState) => state.monitor.autoRefresh)

  const [realtimeData, setRealtimeData] = useState<RealtimeStats[]>([])
  const [currentStats, setCurrentStats] = useState<RealtimeStats>({
    timestamp: new Date().toISOString(),
    impressions: 0,
    clicks: 0,
    cost: 0,
    conversions: 0,
  })

  const { connected } = useWebSocket({
    onConnect: () => {
      message.success('实时数据连接已建立')
    },
    onDisconnect: () => {
      message.warning('实时数据连接已断开')
    },
    onMessage: (data) => {
      if (data.type === 'realtime_stats') {
        const newStats: RealtimeStats = {
          timestamp: new Date().toISOString(),
          ...data.payload,
        }
        setCurrentStats(newStats)
        setRealtimeData((prev) => [...prev.slice(-59), newStats])
      }
    },
  })

  useEffect(() => {
    // 模拟初始数据
    const initialData: RealtimeStats[] = []
    const now = new Date()
    for (let i = 0; i < 60; i++) {
      const time = new Date(now.getTime() - (59 - i) * 60000)
      initialData.push({
        timestamp: time.toISOString(),
        impressions: Math.floor(Math.random() * 1000) + 500,
        clicks: Math.floor(Math.random() * 100) + 50,
        cost: Math.random() * 100 + 50,
        conversions: Math.floor(Math.random() * 10) + 1,
      })
    }
    setRealtimeData(initialData)
    setCurrentStats(initialData[initialData.length - 1])
  }, [])

  const handleAutoRefreshChange = (checked: boolean) => {
    dispatch(toggleAutoRefresh())
    message.info(checked ? '已开启自动刷新' : '已关闭自动刷新')
  }

  return (
    <div>
      <Card
        title="数据实时监控"
        extra={
          <Space>
            <Tag color={connected ? 'success' : 'error'}>
              <WifiOutlined /> {connected ? '已连接' : '未连接'}
            </Tag>
            <Space>
              <ClockCircleOutlined />
              <span>自动刷新</span>
              <Switch checked={autoRefresh} onChange={handleAutoRefreshChange} />
            </Space>
          </Space>
        }
        style={{ marginBottom: 16 }}
      >
        <Row gutter={16}>
          <Col span={6}>
            <Statistic
              title="实时曝光"
              value={currentStats.impressions}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#3f8600' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="实时点击"
              value={currentStats.clicks}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#1890ff' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="实时消耗"
              value={currentStats.cost}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#cf1322' }}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="实时转化"
              value={currentStats.conversions}
              formatter={(value) => formatNumber(Number(value))}
              valueStyle={{ color: '#722ed1' }}
            />
          </Col>
        </Row>
      </Card>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="曝光量趋势">
            <RealtimeChart
              title="曝光量"
              data={realtimeData.map((d) => ({ timestamp: d.timestamp, value: d.impressions }))}
              color="#3f8600"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="点击量趋势">
            <RealtimeChart
              title="点击量"
              data={realtimeData.map((d) => ({ timestamp: d.timestamp, value: d.clicks }))}
              color="#1890ff"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="消耗趋势">
            <RealtimeChart
              title="消耗（元）"
              data={realtimeData.map((d) => ({ timestamp: d.timestamp, value: d.cost }))}
              color="#cf1322"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="转化趋势">
            <RealtimeChart
              title="转化数"
              data={realtimeData.map((d) => ({ timestamp: d.timestamp, value: d.conversions }))}
              color="#722ed1"
            />
          </Card>
        </Col>
      </Row>

      <Card title="数据更新记录" style={{ marginTop: 16 }}>
        <div style={{ color: '#666', fontSize: 12 }}>
          最后更新：{formatDateTime(currentStats.timestamp)}
        </div>
      </Card>
    </div>
  )
}

export default DataMonitor
