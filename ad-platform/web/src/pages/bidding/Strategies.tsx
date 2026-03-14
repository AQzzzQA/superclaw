import React, { useState, useEffect } from 'react'
import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Popconfirm, Statistic, Row, Col, Switch, Tabs } from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  LineChartOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface BiddingStrategy {
  id: number
  campaign_id: number
  tenant_id: number
  name: string
  strategy_type: string
  target_cpa?: number
  target_cpc?: number
  target_roas?: number
  min_bid: number
  max_bid: number
  learning_period: number
  is_enabled: boolean
  created_at: string
  updated_at: string
  activated_at?: string
  avg_cpa?: number
  avg_cpc?: number
  avg_roas?: number
}

interface BiddingRule {
  id: number
  strategy_id: number
  tenant_id: number
  rule_name: string
  rule_type: string
  adjustment_type: string
  adjustment_value: number
  conditions: Record<string, any>
  is_enabled: boolean
  created_at: string
  updated_at: string
}

const BiddingStrategiesPage = () => {
  const [activeTab, setActiveTab] = useState<'strategies' | 'rules' | 'performance'>('strategies')
  const [strategies, setStrategies] = useState<BiddingStrategy[]>([])
  const [rules, setRules] = useState<BiddingRule[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [modalType, setModalType] = useState<'strategy' | 'rule'>('strategy')
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'strategies') {
        // 模拟加载出价策略
        await new Promise(resolve => setTimeout(resolve, 300))
        setStrategies([
          {
            id: 1,
            campaign_id: 100001,
            tenant_id: 1,
            name: 'oCPA 策略',
            strategy_type: 'ocpa',
            target_cpa: 50.0,
            min_bid: 0.10,
            max_bid: 5.0,
            learning_period: 7,
            is_enabled: true,
            created_at: '2026-03-01 10:00:00',
            updated_at: '2026-03-01 10:00:00',
            activated_at: '2026-03-01 10:00:00',
            avg_cpa: 48.5,
            avg_cpc: 1.95,
            avg_roas: 3.2,
          },
        ])
      } else if (activeTab === 'rules') {
        // 模拟加载出价规则
        await new Promise(resolve => setTimeout(resolve, 300))
        setRules([
          {
            id: 1,
            strategy_id: 1,
            tenant_id: 1,
            rule_name: '夜间提价规则',
            rule_type: 'hourly',
            adjustment_type: 'percentage',
            adjustment_value: 0.2,
            conditions: { 'hour': { 'start': 22, 'end': 6 } },
            is_enabled: true,
            created_at: '2026-03-01 10:00:00',
            updated_at: '2026-03-01 10:00:00',
          },
        ])
      }
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateStrategy = () => {
    setModalType('strategy')
    setEditingId(null)
    form.resetFields()
    form.setFieldsValue({ is_enabled: true, learning_period: 7 })
    setModalOpen(true)
  }

  const handleCreateRule = () => {
    setModalType('rule')
    setEditingId(null)
    form.resetFields()
    form.setFieldsValue({ is_enabled: true })
    setModalOpen(true)
  }

  const handleEditStrategy = (record: BiddingStrategy) => {
    setModalType('strategy')
    setEditingId(record.id)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const handleEditRule = (record: BiddingRule) => {
    setModalType('rule')
    setEditingId(record.id)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const handleDeleteStrategy = async (id: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setStrategies(strategies.filter(s => s.id !== id))
      message.success('删除成功')
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleDeleteRule = async (id: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setRules(rules.filter(r => r.id !== id))
      message.success('删除成功')
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleActivate = async (id: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setStrategies(strategies.map(s => ({
        ...s,
        is_enabled: s.id === id ? true : (s.campaign_id === strategies.find(item => item.id === id)?.campaign_id ? false : s.is_enabled)
      })))
      message.success('策略激活成功')
    } catch (error) {
      message.error('激活失败')
    }
  }

  const handleSubmitStrategy = async () => {
    try {
      const values = await form.validateFields()
      await new Promise(resolve => setTimeout(resolve, 500))

      if (editingId) {
        setStrategies(strategies.map(s => s.id === editingId ? { ...s, ...values, updated_at: new Date().toISOString() } : s))
        message.success('更新成功')
      } else {
        const newStrategy: BiddingStrategy = {
          id: strategies.length + 1,
          ...values,
          campaign_id: values.campaign_id,
          tenant_id: 1,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }
        setStrategies([...strategies, newStrategy])
        message.success('创建成功')
      }

      setModalOpen(false)
      form.resetFields()
    } catch (error) {
      message.error('提交失败')
    }
  }

  const handleSubmitRule = async () => {
    try {
      const values = await form.validateFields()
      await new Promise(resolve => setTimeout(resolve, 500))

      if (editingId) {
        setRules(rules.map(r => r.id === editingId ? { ...r, ...values, updated_at: new Date().toISOString() } : r))
        message.success('更新成功')
      } else {
        const newRule: BiddingRule = {
          id: rules.length + 1,
          ...values,
          tenant_id: 1,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
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

  const strategyColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '策略名称', dataIndex: 'name', key: 'name', width: 150 },
    {
      title: '策略类型',
      dataIndex: 'strategy_type',
      key: 'strategy_type',
      width: 100,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          ocpa: { text: 'oCPA', color: 'blue' },
          ocpc: { text: 'oCPC', color: 'green' },
          roas: { text: 'ROAS', color: 'orange' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    {
      title: '目标值',
      key: 'target_value',
      width: 120,
      render: (_: any, record: BiddingStrategy) => {
        if (record.target_cpa) return `¥${record.target_cpa}`
        if (record.target_cpc) return `¥${record.target_cpc}`
        if (record.target_roas) return `${record.target_roas.toFixed(2)}x`
        return '-'
      },
    },
    {
      title: '出价范围',
      key: 'bid_range',
      width: 120,
      render: (_: any, record: BiddingStrategy) => `¥${record.min_bid.toFixed(2)} - ¥${record.max_bid.toFixed(2)}`,
    },
    {
      title: '实际效果',
      key: 'performance',
      width: 180,
      render: (_: any, record: BiddingStrategy) => (
        <div>
          <div>CPA: <Text type="secondary">{record.avg_cpa?.toFixed(2) || '-'}¥</Text></div>
          <div>CPC: <Text type="secondary">{record.avg_cpc?.toFixed(2) || '-'}¥</Text></div>
          <div>ROI: <Text type="secondary">{record.avg_roas?.toFixed(2) || '-'}x</Text></div>
        </div>
      ),
    },
    {
      title: '状态',
      dataIndex: 'is_enabled',
      key: 'is_enabled',
      width: 100,
      render: (enabled: boolean) => (
        <Tag color={enabled ? 'green' : 'red'}>{enabled ? '启用' : '禁用'}</Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      fixed: 'right' as const,
      render: (_: any, record: BiddingStrategy) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEditStrategy(record)}
          >
            编辑
          </Button>
          <Button
            type="link"
            size="small"
            icon={<PlayCircleOutlined />}
            onClick={() => handleActivate(record.id)}
            disabled={record.is_enabled}
          >
            激活
          </Button>
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDeleteStrategy(record.id)}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const ruleColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '规则名称', dataIndex: 'rule_name', key: 'rule_name', width: 150 },
    {
      title: '规则类型',
      dataIndex: 'rule_type',
      key: 'rule_type',
      width: 100,
      render: (type: string) => {
        const typeMap: Record<string, string> = {
          hourly: '每小时',
          daily: '每天',
          weekly: '每周',
          custom: '自定义',
        }
        return typeMap[type] || type
      },
    },
    { title: '调整类型', dataIndex: 'adjustment_type', key: 'adjustment_type', width: 100 },
    { title: '调整值', dataIndex: 'adjustment_value', key: 'adjustment_value', width: 100 },
    {
      title: '触发条件',
      dataIndex: 'conditions',
      key: 'conditions',
      ellipsis: true,
      render: (conds: Record<string, any>) => JSON.stringify(conds),
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
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right' as const,
      render: (_: any, record: BiddingRule) => (
        <Space>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => handleEditRule(record)}>
            编辑
          </Button>
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDeleteRule(record.id)}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2}>出价策略</Title>
          <Text type="secondary">智能化出价优化，提升广告效果</Text>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>
            刷新
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreateStrategy}>
            创建策略
          </Button>
        </Space>
      </div>

      <Card>
        <Tabs activeKey={activeTab} onChange={(key) => setActiveTab(key as 'strategies' | 'rules' | 'performance')}>
          <Tabs.TabPane tab="出价策略" key="strategies">
            <Table
              columns={strategyColumns}
              dataSource={strategies}
              rowKey="id"
              loading={loading}
              scroll={{ x: 1600 }}
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab="出价规则" key="rules">
            <Space style={{ marginBottom: 16 }}>
              <Button type="primary" icon={<PlusOutlined />} onClick={handleCreateRule}>
                创建规则
              </Button>
            </Space>
            <Table
              columns={ruleColumns}
              dataSource={rules}
              rowKey="id"
              loading={loading}
              scroll={{ x: 1400 }}
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab="效果分析" key="performance">
            <div style={{ textAlign: 'center', padding: '48px' }}>
              <Text type="secondary">效果分析功能开发中...</Text>
            </div>
          </Tabs.TabPane>
        </Tabs>
      </Card>

      <Modal
        title={modalType === 'strategy' ? '编辑出价策略' : '编辑出价规则'}
        open={modalOpen}
        onOk={modalType === 'strategy' ? handleSubmitStrategy : handleSubmitRule}
        onCancel={() => { setModalOpen(false); form.resetFields() }}
        width={600}
        okText="确定"
        cancelText="取消"
      >
        {modalType === 'strategy' ? (
          <Form form={form} layout="vertical">
            <Form.Item name="campaign_id" label="广告计划ID" rules={[{ required: true, message: '请输入广告计划ID' }]}>
              <Input type="number" placeholder="请输入广告计划ID" />
            </Form.Item>
            <Form.Item name="name" label="策略名称" rules={[{ required: true, message: '请输入策略名称' }]}>
              <Input placeholder="请输入策略名称" />
            </Form.Item>
            <Form.Item name="strategy_type" label="策略类型" rules={[{ required: true, message: '请选择策略类型' }]}>
              <Select placeholder="请选择策略类型">
                <Select.Option value="ocpa">oCPA (优化转化成本)</Select.Option>
                <Select.Option value="ocpc">oCPC (优化点击成本)</Select.Option>
                <Select.Option value="roas">ROAS (优化投资回报)</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item dependencies={['strategy_type']}>
              {({ getFieldValue }) => (
                <>
                  <Form.Item noStyle name="target_cpa" label="目标转化成本">
                    <Input disabled={getFieldValue('strategy_type') !== 'ocpa'} placeholder="请输入目标CPA" />
                  </Form.Item>
                  <Form.Item noStyle name="target_cpc" label="目标点击成本">
                    <Input disabled={getFieldValue('strategy_type') !== 'ocpc'} placeholder="请输入目标CPC" />
                  </Form.Item>
                  <Form.Item noStyle name="target_roas" label="目标ROI">
                    <Input disabled={getFieldValue('strategy_type') !== 'roas'} placeholder="请输入目标ROI" />
                  </Form.Item>
                </>
              )}
            </Form.Item>
            <Space style={{ width: '100%' }}>
              <Form.Item name="min_bid" label="最低出价" style={{ width: '50%' }}>
                <Input type="number" placeholder="0.10" />
              </Form.Item>
              <Form.Item name="max_bid" label="最高出价" style={{ width: '50%' }}>
                <Input type="number" placeholder="10.0" />
              </Form.Item>
            </Space>
            <Form.Item name="learning_period" label="学习周期（天）">
              <Input type="number" placeholder="7" />
            </Form.Item>
            <Form.Item name="is_enabled" label="启用状态" valuePropName="checked">
              <Switch checkedChildren="启用" unCheckedChildren="禁用" />
            </Form.Item>
          </Form>
        ) : (
          <Form form={form} layout="vertical">
            <Form.Item name="strategy_id" label="策略ID" rules={[{ required: true, message: '请选择策略' }]}>
              <Select placeholder="请选择策略">
                {strategies.map(s => (
                  <Select.Option key={s.id} value={s.id}>{s.name}</Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="rule_name" label="规则名称" rules={[{ required: true, message: '请输入规则名称' }]}>
              <Input placeholder="请输入规则名称" />
            </Form.Item>
            <Form.Item name="rule_type" label="规则类型" rules={[{ required: true, message: '请选择规则类型' }]}>
              <Select placeholder="请选择规则类型">
                <Select.Option value="hourly">每小时</Select.Option>
                <Select.Option value="daily">每天</Select.Option>
                <Select.Option value="weekly">每周</Select.Option>
                <Select.Option value="custom">自定义</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item name="adjustment_type" label="调整类型" rules={[{ required: true, message: '请选择调整类型' }]}>
              <Select placeholder="请选择调整类型">
                <Select.Option value="percentage">百分比</Select.Option>
                <Select.Option value="fixed">固定值</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item name="adjustment_value" label="调整值" rules={[{ required: true, message: '请输入调整值' }]}>
              <Input type="number" placeholder="请输入调整值" />
            </Form.Item>
            <Form.Item name="conditions" label="触发条件" rules={[{ required: true, message: '请输入触发条件' }]}>
              <Input.TextArea rows={3} placeholder='{"hour": {"start": 22, "end": 6}}' />
            </Form.Item>
            <Form.Item name="is_enabled" label="启用状态" valuePropName="checked">
              <Switch checkedChildren="启用" unCheckedChildren="禁用" />
            </Form.Item>
          </Form>
        )}
      </Modal>
    </div>
  )
}

export default BiddingStrategiesPage
