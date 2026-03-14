import React, { useState } from 'react'
import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Checkbox, Switch, Progress } from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface Campaign {
  id: number
  name: string
  objectiveType: string
  budget: number
  spent: number
  status: string
  ctr: number
  cvr: number
  roi: number
}

const Campaigns: React.FC = () => {
  const [data, setData] = useState<Campaign[]>([
    {
      id: 1,
      name: '夏季促销活动',
      objectiveType: '产品推广',
      budget: 100000,
      spent: 45000,
      status: 'enable',
      ctr: 2.5,
      cvr: 5.0,
      roi: 3.2,
    },
    {
      id: 2,
      name: '节日营销活动',
      objectiveType: '应用推广',
      budget: 80000,
      spent: 35000,
      status: 'enable',
      ctr: 2.0,
      cvr: 4.5,
      roi: 2.8,
    },
  ])

  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  const handleAdd = () => {
    setEditingId(null)
    form.resetFields()
    setModalOpen(true)
  }

  const handleEdit = (record: Campaign) => {
    setEditingId(record.id)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const handleToggleStatus = (id: number) => {
    setData(
      data.map((c) =>
        c.id === id ? { ...c, status: c.status === 'enable' ? 'disable' : 'enable' } : c
      )
    )
    message.success('状态更新成功')
  }

  const handleBatchEnable = () => {
    if (selectedIds.length === 0) return message.warning('请先选择计划')
    setData(data.map((c) => (selectedIds.includes(c.id) ? { ...c, status: 'enable' } : c)))
    message.success(`已启用 ${selectedIds.length} 个计划`)
    setSelectedIds([])
  }

  const handleBatchDisable = () => {
    if (selectedIds.length === 0) return message.warning('请先选择计划')
    setData(data.map((c) => (selectedIds.includes(c.id) ? { ...c, status: 'disable' } : c)))
    message.success(`已暂停 ${selectedIds.length} 个计划`)
    setSelectedIds([])
  }

  const handleClearSelection = () => {
    setSelectedIds([])
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()

      if (editingId) {
        setData(
          data.map((c) => (c.id === editingId ? { ...c, ...values, updatedAt: new Date().toISOString() } : c))
        )
        message.success('更新成功')
      } else {
        const newCampaign: Campaign = {
          id: data.length + 1,
          ...values,
          status: 'enable',
          spent: 0,
          ctr: 0,
          cvr: 0,
          roi: 0,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }
        setData([...data, newCampaign])
        message.success('创建成功')
      }

      setModalOpen(false)
      form.resetFields()
    } catch (error) {
      message.error('提交失败')
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '计划名称', dataIndex: 'name', key: 'name', width: 200 },
    { title: '推广目标', dataIndex: 'objectiveType', key: 'objectiveType', width: 120 },
    { title: '预算 (¥)', dataIndex: 'budget', key: 'budget', width: 120, render: (v: number) => v.toLocaleString() },
    { title: '消耗 (¥)', dataIndex: 'spent', key: 'spent', width: 120, render: (v: number) => v.toLocaleString() },
    {
      title: '进度',
      key: 'progress',
      width: 150,
      render: (_: any, record: Campaign) => (
        <Progress
          percent={Math.round((record.spent / record.budget) * 100)}
          status={record.spent > record.budget ? 'exception' : 'normal'}
        />
      ),
    },
    { title: 'CTR (%)', dataIndex: 'ctr', key: 'ctr', width: 100, render: (v: number) => v.toFixed(2) },
    { title: 'CVR (%)', dataIndex: 'cvr', key: 'cvr', width: 100, render: (v: number) => v.toFixed(2) },
    { title: 'ROI', dataIndex: 'roi', key: 'roi', width: 100, render: (v: number) => v?.toFixed(2) ?? '-' },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={status === 'enable' ? 'green' : 'red'}>{status === 'enable' ? '启用' : '暂停'}</Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_: any, record: Campaign) => (
        <Space>
          <Button
            size="small"
            type={record.status === 'enable' ? 'default' : 'primary'}
            icon={record.status === 'enable' ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
            onClick={() => handleToggleStatus(record.id)}
          >
            {record.status === 'enable' ? '暂停' : '启用'}
          </Button>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 0, minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ padding: 24, background: 'white', marginBottom: 16 }}>
        <Title level={2}>广告计划</Title>
        <Text type="secondary">按小时、星期、自定义时段定向</Text>
      </div>

      <div style={{ padding: 24, background: '#F5F7FA', marginBottom: 16 }}>
        <Space style={{ marginBottom: 16 }}>
          <Button icon={<ReloadOutlined />}>刷新</Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            创建计划
          </Button>
        </Space>

        <Card>
          <Table
            columns={columns}
            dataSource={data}
            rowKey="id"
            rowSelection={{
              selectedRowKeys: selectedIds,
              onChange: (selectedRowKeys) => setSelectedIds(selectedRowKeys as number[]),
            }}
            pagination={{ pageSize: 10 }}
          />
        </Card>
      </div>

      {selectedIds.length > 0 && (
        <div
          style={{
            position: 'fixed',
            bottom: 24,
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: 1000,
            background: 'rgba(0,0,0,0.8)',
            padding: '12px 24px',
            borderRadius: 8,
            display: 'flex',
            gap: 12,
          }}
        >
          <Text style={{ color: 'white' }}>已选择 {selectedIds.length} 项</Text>
          <Button size="small" type="primary" onClick={handleBatchEnable}>
            批量启用
          </Button>
          <Button size="small" onClick={handleBatchDisable}>批量暂停</Button>
          <Button size="small" onClick={handleClearSelection}>取消选择</Button>
        </div>
      )}

      <Modal
        title={editingId ? '编辑广告计划' : '创建广告计划'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setModalOpen(false)
          form.resetFields()
        }}
        width={600}
        okText="创建"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="计划名称" rules={[{ required: true, message: '请输入计划名称' }]}>
            <Input placeholder="请输入计划名称" />
          </Form.Item>
          <Form.Item
            name="objectiveType"
            label="推广目标"
            initialValue="产品推广"
            rules={[{ required: true, message: '请选择推广目标' }]}
          >
            <Select>
              <Select.Option value="产品推广">产品推广</Select.Option>
              <Select.Option value="应用推广">应用推广</Select.Option>
              <Select.Option value="网页转化">网页转化</Select.Option>
              <Select.Option value="收集线索">收集线索</Select.Option>
              <Select.Option value="门店推广">门店推广</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="budget" label="预算金额" initialValue={1000} rules={[{ required: true, message: '请输入预算金额' }]}>
            <Input type="number" min={0} placeholder="请输入预算金额" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Campaigns
