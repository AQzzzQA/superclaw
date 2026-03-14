import React, { useState } from 'react'
import { Card, Form, Select, Input, InputNumber, Slider, Button, Space, Table, Modal, message, Tag, Switch } from 'antd'
import { SaveOutlined, PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import type { TableProps } from 'antd'

const { Option } = Select

interface BiddingStrategy {
  key: string
  name: string
  strategyType: string
  bidAmount: number
  bidMode: string
  target: string
  status: string
  performance: string
}

const BiddingPage = () => {
  const [form] = Form.useForm()
  const [modalVisible, setModalVisible] = useState(false)
  const [editingKey, setEditingKey] = useState<string | null>(null)

  const [bidding, setBidding] = useState<BiddingStrategy[]>([
    {
      key: '1',
      name: '智能优化策略',
      strategyType: 'auto',
      bidAmount: 2.5,
      bidMode: 'cpc',
      target: 'max_conversions',
      status: 'enabled',
      performance: 'good',
    },
    {
      key: '2',
      name: '固定出价策略',
      strategyType: 'manual',
      bidAmount: 1.8,
      bidMode: 'cpm',
      target: 'max_impressions',
      status: 'enabled',
      performance: 'average',
    },
  ])

  const columns: TableProps<BiddingStrategy>['columns'] = [
    { title: '策略名称', dataIndex: 'name', key: 'name', width: 150 },
    { title: '策略类型', dataIndex: 'strategyType', key: 'strategyType', width: 100, render: (t) => t === 'auto' ? '智能' : '手动' },
    { title: '出价金额', dataIndex: 'bidAmount', key: 'bidAmount', width: 100, align: 'right', render: (v) => `¥${v.toFixed(2)}` },
    { title: '出价方式', dataIndex: 'bidMode', key: 'bidMode', width: 100, render: (m) => m === 'cpc' ? 'CPC' : 'CPM' },
    { title: '优化目标', dataIndex: 'target', key: 'target', width: 150 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (s) => <Tag color={s === 'enabled' ? 'green' : 'red'}>{s === 'enabled' ? '启用' : '停用'}</Tag>
    },
    {
      title: '效果',
      dataIndex: 'performance',
      key: 'performance',
      width: 100,
      render: (p) => {
        const map = { good: { text: '优秀', color: 'green' }, average: { text: '一般', color: 'orange' }, poor: { text: '较差', color: 'red' } }
        const m = map[p as keyof typeof map] || map.average
        return <Tag color={m.color}>{m.text}</Tag>
      },
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>编辑</Button>
          <Button icon={<DeleteOutlined />} size="small" danger onClick={() => handleDelete(record.key)}>删除</Button>
        </Space>
      ),
    },
  ]

  const handleEdit = (record: BiddingStrategy) => {
    setEditingKey(record.key)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = (key: string) => {
    setBidding(bidding.filter(item => item.key !== key))
    message.success('删除成功')
  }

  const handleSave = async () => {
    const values = await form.validateFields()
    if (editingKey) {
      setBidding(bidding.map(item => item.key === editingKey ? { ...item, ...values } : item))
      message.success('更新成功')
    } else {
      setBidding([...bidding, { ...values, key: String(bidding.length + 1) }])
      message.success('添加成功')
    }
    setModalVisible(false)
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <h2>出价策略</h2>
      <Card style={{ marginBottom: 24 }}>
        <Space size="large">
          <div><div style={{ color: '#666' }}>平均CPC</div><div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677FF' }}>¥2.15</div></div>
          <div><div style={{ color: '#666' }}>平均CPM</div><div style={{ fontSize: 24, fontWeight: 'bold', color: '#52C41A' }}>¥18.50</div></div>
          <div><div style={{ color: '#666' }}>竞价胜率</div><div style={{ fontSize: 24, fontWeight: 'bold', color: '#FA8C16' }}>68.5%</div></div>
        </Space>
      </Card>
      <Card style={{ marginBottom: 16 }}><Space><Button type="primary" icon={<PlusOutlined />}>添加策略</Button><Button icon={<SaveOutlined />}>批量调整</Button></Space></Card>
      <Card><Table columns={columns} dataSource={bidding} pagination={{ pageSize: 10 }} scroll={{ x: 1000 }} /></Card>
      <Modal title={editingKey ? '编辑策略' : '添加策略'} open={modalVisible} onOk={handleSave} onCancel={() => setModalVisible(false)} width={600}>
        <Form form={form} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item label="策略名称" name="name" rules={[{ required: true }]}><Input placeholder="输入策略名称" /></Form.Item>
          <Form.Item label="策略类型" name="strategyType" rules={[{ required: true }]}>
            <Select><Option value="auto">智能优化</Option><Option value="manual">手动出价</Option></Select>
          </Form.Item>
          <Form.Item label="出价金额" name="bidAmount" rules={[{ required: true }]}><InputNumber min={0.01} step={0.01} style={{ width: '100%' }} /></Form.Item>
          <Form.Item label="出价方式" name="bidMode" rules={[{ required: true }]}>
            <Select><Option value="cpc">CPC（按点击）</Option><Option value="cpm">CPM（按千次展示）</Option></Select>
          </Form.Item>
          <Form.Item label="优化目标" name="target" rules={[{ required: true }]}>
            <Select><Option value="max_conversions">最大化转化</Option><Option value="max_impressions">最大化曝光</Option><Option value="max_clicks">最大化点击</Option><Option value="target_cost">目标成本</Option></Select>
          </Form.Item>
          <Form.Item label="目标成本" name="targetCost"><InputNumber min={0.01} step={0.01} style={{ width: '100%' }} placeholder="可选，仅目标成本模式" /></Form.Item>
          <Form.Item label="状态" name="status" initialValue="enabled"><Select><Option value="enabled">启用</Option><Option value="disabled">停用</Option></Select></Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default BiddingPage
