import React, { useState, useEffect } from 'react'
import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Popconfirm, Switch, Tabs } from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  BellOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface AlertRule {
  id: number
  campaign_id?: number
  tenant_id: number
  name: string
  rule_type: string
  threshold: number
  period: string
  action: string
  is_enabled: boolean
  created_at: string
  updated_at: string
  last_triggered_at?: string
  trigger_count: number
}

interface AlertEvent {
  id: number
  rule_id: number
  campaign_id: number
  tenant_id: number
  alert_type: string
  alert_message: string
  current_value: number
  threshold_value: number
  severity: string
  is_resolved: boolean
  created_at: string
  resolved_at?: string
}

const AlertsPage = () => {
  const [activeTab, setActiveTab] = useState<'rules' | 'events'>('rules')
  const [rules, setRules] = useState<AlertRule[]>([])
  const [events, setEvents] = useState<AlertEvent[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'rules') {
        // 模拟加载预警规则
        await new Promise(resolve => setTimeout(resolve, 300))
        setRules([
          {
            id: 1,
            campaign_id: 100001,
            tenant_id: 1,
            name: '日消耗预警',
            rule_type: 'cost_alert',
            threshold: 1000,
            period: 'daily',
            action: 'send_notification',
            is_enabled: true,
            created_at: '2026-03-01 10:00:00',
            updated_at: '2026-03-01 10:00:00',
            last_triggered_at: '2026-03-01 09:00:00',
            trigger_count: 3,
          },
          {
            id: 2,
            campaign_id: 100001,
            tenant_id: 1,
            name: 'CTR下降预警',
            rule_type: 'performance_alert',
            threshold: 1.5,
            period: 'hourly',
            action: 'pause_campaign',
            is_enabled: true,
            created_at: '2026-03-01 10:00:00',
            updated_at: '2026-03-01 10:00:00',
            last_triggered_at: null,
            trigger_count: 0,
          },
        ])
      } else {
        // 模拟加载预警事件
        await new Promise(resolve => setTimeout(resolve, 300))
        setEvents([
          {
            id: 1,
            rule_id: 1,
            campaign_id: 100001,
            tenant_id: 1,
            alert_type: 'cost_alert',
            alert_message: '日消耗预警触发：当前值 1200，阈值 1000',
            current_value: 1200,
            threshold_value: 1000,
            severity: 'high',
            is_resolved: false,
            created_at: '2026-03-01 09:00:00',
            resolved_at: null,
          },
          {
            id: 2,
            rule_id: 2,
            campaign_id: 100001,
            tenant_id: 1,
            alert_type: 'performance_alert',
            alert_message: 'CTR下降预警触发：当前值 1.2，阈值 1.5',
            current_value: 1.2,
            threshold_value: 1.5,
            severity: 'medium',
            is_resolved: true,
            created_at: '2026-03-01 08:00:00',
            resolved_at: '2026-03-01 08:30:00',
          },
        ])
      }
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingId(null)
    form.resetFields()
    form.setFieldsValue({ is_enabled: true, period: 'daily' })
    setModalOpen(true)
  }

  const handleEdit = (record: AlertRule) => {
    setEditingId(record.id)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setRules(rules.filter(r => r.id !== id))
      message.success('删除成功')
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      await new Promise(resolve => setTimeout(resolve, 500))

      if (editingId) {
        setRules(rules.map(r => r.id === editingId ? { ...r, ...values, updated_at: new Date().toISOString() } : r))
        message.success('更新成功')
      } else {
        const newRule: AlertRule = {
          id: rules.length + 1,
          ...values,
          tenant_id: 1,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          trigger_count: 0,
        }
        setRules([...rules, newRule])
        message.success('创建成功')
      }

      setModalOpen(false)
      form.resetFields()
    } catch (error) {
      message.error('提交失败')
    }
  }

  const ruleColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '规则名称', dataIndex: 'name', key: 'name', width: 150 },
    {
      title: '规则类型',
      dataIndex: 'rule_type',
      key: 'rule_type',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          cost_alert: { text: '消耗预警', color: 'red' },
          performance_alert: { text: '效果预警', color: 'orange' },
          anomaly_detection: { text: '异常检测', color: 'purple' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    { title: '阈值', dataIndex: 'threshold', key: 'threshold', width: 100 },
    {
      title: '周期',
      dataIndex: 'period',
      key: 'period',
      width: 80,
      render: (period: string) => {
        const periodMap: Record<string, string> = {
          hourly: '小时',
          daily: '天',
          weekly: '周',
        }
        return periodMap[period] || period
      },
    },
    {
      title: '触发动作',
      dataIndex: 'action',
      key: 'action',
      width: 150,
      render: (action: string) => {
        const actionMap: Record<string, string> = {
          pause_campaign: '暂停计划',
          send_notification: '发送通知',
          both: '暂停+通知',
        }
        return actionMap[action] || action
      },
    },
    {
      title: '状态',
      dataIndex: 'is_enabled',
      key: 'is_enabled',
      width: 80,
      render: (enabled: boolean) => (
        <Tag color={enabled ? 'green' : 'red'}>{enabled ? '启用' : '禁用'}</Tag>
      ),
    },
    { title: '触发次数', dataIndex: 'trigger_count', key: 'trigger_count', width: 100 },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right' as const,
      render: (_: any, record: AlertRule) => (
        <Space>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const eventColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    {
      title: '预警类型',
      dataIndex: 'alert_type',
      key: 'alert_type',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          cost_alert: { text: '消耗', color: 'red' },
          performance_alert: { text: '效果', color: 'orange' },
          anomaly_detection: { text: '异常', color: 'purple' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    { title: '预警消息', dataIndex: 'alert_message', key: 'alert_message', ellipsis: true },
    { title: '当前值', dataIndex: 'current_value', key: 'current_value', width: 100 },
    { title: '阈值', dataIndex: 'threshold_value', key: 'threshold_value', width: 100 },
    {
      title: '严重程度',
      dataIndex: 'severity',
      key: 'severity',
      width: 100,
      render: (severity: string) => {
        const severityMap: Record<string, { text: string; color: string }> = {
          low: { text: '低', color: 'blue' },
          medium: { text: '中', color: 'orange' },
          high: { text: '高', color: 'red' },
          critical: { text: '严重', color: 'red' },
        }
        const config = severityMap[severity] || { text: severity, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    {
      title: '状态',
      dataIndex: 'is_resolved',
      key: 'is_resolved',
      width: 100,
      render: (resolved: boolean) => (
        <Tag icon={resolved ? <CheckCircleOutlined /> : <BellOutlined />} color={resolved ? 'green' : 'red'}>
          {resolved ? '已解决' : '未解决'}
        </Tag>
      ),
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 180 },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2}>预警管理</Title>
          <Text type="secondary">配置预警规则，及时响应异常情况</Text>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>
            刷新
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
            创建规则
          </Button>
        </Space>
      </div>

      <Card>
        <Tabs activeKey={activeTab} onChange={(key) => setActiveTab(key as 'rules' | 'events')}>
          <Tabs.TabPane tab="预警规则" key="rules">
            <Table
              columns={ruleColumns}
              dataSource={rules}
              rowKey="id"
              loading={loading}
              scroll={{ x: 1400 }}
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab="预警事件" key="events">
            <Table
              columns={eventColumns}
              dataSource={events}
              rowKey="id"
              loading={loading}
              scroll={{ x: 1400 }}
            />
          </Tabs.TabPane>
        </Tabs>
      </Card>

      <Modal
        title={editingId ? '编辑预警规则' : '创建预警规则'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => { setModalOpen(false); form.resetFields() }}
        width={600}
        okText="确定"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="campaign_id" label="广告计划ID" rules={[{ required: true, message: '请输入广告计划ID' }]}>
            <Input placeholder="请输入广告计划ID" type="number" />
          </Form.Item>
          <Form.Item name="name" label="规则名称" rules={[{ required: true, message: '请输入规则名称' }]}>
            <Input placeholder="请输入规则名称" />
          </Form.Item>
          <Form.Item name="rule_type" label="规则类型" rules={[{ required: true, message: '请选择规则类型' }]}>
            <Select placeholder="请选择规则类型">
              <Select.Option value="cost_alert">消耗预警</Select.Option>
              <Select.Option value="performance_alert">效果预警</Select.Option>
              <Select.Option value="anomaly_detection">异常检测</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="threshold" label="阈值" rules={[{ required: true, message: '请输入阈值' }]}>
            <Input placeholder="请输入阈值" type="number" />
          </Form.Item>
          <Form.Item name="period" label="周期" rules={[{ required: true, message: '请选择周期' }]}>
            <Select placeholder="请选择周期">
              <Select.Option value="hourly">每小时</Select.Option>
              <Select.Option value="daily">每天</Select.Option>
              <Select.Option value="weekly">每周</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="action" label="触发动作" rules={[{ required: true, message: '请选择触发动作' }]}>
            <Select placeholder="请选择触发动作">
              <Select.Option value="pause_campaign">暂停计划</Select.Option>
              <Select.Option value="send_notification">发送通知</Select.Option>
              <Select.Option value="both">暂停+通知</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="is_enabled" label="启用状态" valuePropName="checked">
            <Switch checkedChildren="启用" unCheckedChildren="禁用" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default AlertsPage
