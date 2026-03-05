import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Row, Col, Button, Typography, Space, Statistic } from 'antd'
import {
  UserOutlined,
  MobileOutlined,
  EnvironmentOutlined,
  ClockCircleOutlined,
  WifiOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

const TargetingHome = () => {
  const navigate = useNavigate()

  const targetingTypes = [
    {
      key: 'audience',
      title: '人群定向',
      icon: <UserOutlined style={{ fontSize: 48, color: '#1677FF' }} />,
      description: '基于用户兴趣、行为等标签进行精准定向',
      count: 0,
      color: '#1677FF',
    },
    {
      key: 'device',
      title: '设备定向',
      icon: <MobileOutlined style={{ fontSize: 48, color: '#52C41A' }} />,
      description: '按操作系统、设备品牌、网络类型等定向',
      count: 0,
      color: '#52C41A',
    },
    {
      key: 'geo',
      title: '地域定向',
      icon: <EnvironmentOutlined style={{ fontSize: 48, color: '#FAAD14' }} />,
      description: '按省、市、区、商圈、LBS 位置定向',
      count: 0,
      color: '#FAAD14',
    },
    {
      key: 'time',
      title: '时间定向',
      icon: <ClockCircleOutlined style={{ fontSize: 48, color: '#722ED1' }} />,
      description: '按小时、星期、自定义时间段定向',
      count: 0,
      color: '#722ED1',
    },
    {
      key: 'environment',
      title: '环境定向',
      icon: <WifiOutlined style={{ fontSize: 48, color: '#EB2F96' }} />,
      description: '按网络类型、运营商、App 环境等定向',
      count: 0,
      color: '#EB2F96',
    },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <Title level={2}>定向投放</Title>
      <Text type="secondary">创建和管理各种定向策略，实现精准投放</Text>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        {targetingTypes.map((item) => (
          <Col span={6} key={item.key}>
            <Card
              hoverable
              onClick={() => navigate(`/targeting/${item.key}`)}
              style={{
                cursor: 'pointer',
                transition: 'all 0.3s',
                height: '100%',
              }}
              bodyStyle={{ padding: 24 }}
            >
              <div style={{ textAlign: 'center' }}>
                {item.icon}
                <div style={{ marginTop: 16, marginBottom: 8 }}>
                  <Text strong style={{ fontSize: 18 }}>{item.title}</Text>
                </div>
                <div style={{ marginBottom: 16 }}>
                  <Text type="secondary" style={{ fontSize: 14 }}>
                    {item.description}
                  </Text>
                </div>
                <Statistic
                  value={item.count}
                  suffix="个规则"
                  valueStyle={{ color: item.color }}
                />
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Card
        title="快速开始"
        style={{ marginTop: 24 }}
        extra={
          <Button type="primary" onClick={() => navigate('/campaigns')}>
            跳转到广告计划
          </Button>
        }
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Text strong>1. 创建定向规则</Text>
            <br />
            <Text type="secondary">选择定向类型，配置定向参数</Text>
          </div>
          <div>
            <Text strong>2. 应用到广告计划</Text>
            <br />
            <Text type="secondary">将定向规则应用到具体的广告计划中</Text>
          </div>
          <div>
            <Text strong>3. 监控投放效果</Text>
            <br />
            <Text type="secondary">在报表中查看各定向策略的投放效果</Text>
          </div>
        </Space>
      </Card>
    </div>
  )
}

export default TargetingHome
