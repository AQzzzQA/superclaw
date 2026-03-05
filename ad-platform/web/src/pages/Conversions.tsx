import React, { useState } from 'react'
import { Card, Form, Input, InputNumber, Switch, Select, Button, Space, Table, Modal, message, Tag } from 'antd'
import { SaveOutlined, PlusOutlined, EditOutlined, DeleteOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons'
import type { TableProps } from 'antd'

const { TextArea } = Input
const { Option } = Select

interface ConversionRule {
  key: string
  name: string
  eventType: string
  mappingUrl: string
  clickWindow: number
  viewWindow: number
  status: string
  lastSync: string
}

const ConversionsPage = () => {
  const [form] = Form.useForm()
  const [modalVisible, setModalVisible] = useState(false)
  const [editingKey, setEditingKey] = useState<string | null>(null)

  const [conversions, setConversions] = useState<ConversionRule[]>([
    {
      key: '1',
      name: '注册转化',
      eventType: 'register',
      mappingUrl: 'https://api.example.com/callback/register',
      clickWindow: 7,
      viewWindow: 1,
      status: 'enabled',
      lastSync: '2026-03-02 15:30:00',
    },
    {
      key: '2',
      name: '下单转化',
      eventType: 'purchase',
      mappingUrl: 'https://api.example.com/callback/purchase',
      clickWindow: 30,
      viewWindow: 7,
      status: 'enabled',
      lastSync: '2026-03-02 15:30:00',
    },
    {
      key: '3',
      name: '支付转化',
      eventType: 'payment',
      mappingUrl: 'https://api.example.com/callback/payment',
      clickWindow: 30,
      viewWindow: 7,
      status: 'disabled',
      lastSync: '2026-03-01 10:00:00',
    },
  ])

  const columns: TableProps<ConversionRule>['columns'] = [
    { title: '转化名称', dataIndex: 'name', key: 'name', width: 150 },
    { title: '事件类型', dataIndex: 'eventType', key: 'eventType', width: 120 },
    { title: '回调URL', dataIndex: 'mappingUrl', key: 'mappingUrl', width: 250, ellipsis: true },
    { title: '点击归因(天)', dataIndex: 'clickWindow', key: 'clickWindow', width: 120, align: 'center' },
    { title: '浏览归因(天)', dataIndex: 'viewWindow', key: 'viewWindow', width: 120, align: 'center' },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      align: 'center',
      render: (status: string) => (
        <Tag color={status === 'enabled' ? 'green' : 'red'}>
          {status === 'enabled' ? '启用' : '停用'}
        </Tag>
      ),
    },
    { title: '最后同步', dataIndex: 'lastSync', key: 'lastSync', width: 180 },
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

  const handleAdd = () => {
    setModalVisible(true)
    setEditingKey(null)
    form.resetFields()
  }

  const handleEdit = (record: ConversionRule) => {
    setEditingKey(record.key)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = (key: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个转化规则吗？',
      onOk: () => {
        setConversions(conversions.filter(item => item.key !== key))
        message.success('删除成功')
      },
    })
  }

  const handleSave = async () => {
    try {
      const values = await form.validateFields()
      if (editingKey) {
        setConversions(conversions.map(item =>
          item.key === editingKey ? { ...item, ...values } : item
        ))
        message.success('更新成功')
      } else {
        const newKey = String(conversions.length + 1)
        setConversions([
          ...conversions,
          {
            ...values,
            key: newKey,
            lastSync: new Date().toLocaleString('zh-CN'),
          },
        ])
        message.success('添加成功')
      }
      setModalVisible(false)
    } catch (error) {
      console.error('表单验证失败:', error)
    }
  }

  const handleStatusToggle = (key: string, status: string) => {
    setConversions(conversions.map(item =>
      item.key === key ? { ...item, status: status === 'enabled' ? 'disabled' : 'enabled' } : item
    ))
    message.success(status === 'enabled' ? '已停用' : '已启用')
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <h2>转化追踪</h2>
        <p style={{ color: '#666' }}>配置转化规则，追踪广告投放效果</p>
      </div>

      {/* 转化统计 */}
      <Card style={{ marginBottom: 24 }}>
        <Space size="large">
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>今日转化</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677FF' }}>1,234</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>转化率</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52C41A' }}>5.2%</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>归因转化</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#FA8C16' }}>987</div>
          </div>
        </Space>
      </Card>

      {/* 操作按钮 */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>添加转化</Button>
          <Button icon={<SaveOutlined />}>批量操作</Button>
        </Space>
      </Card>

      {/* 转化规则列表 */}
      <Card>
        <Table
          columns={columns}
          dataSource={conversions}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 添加/编辑模态框 */}
      <Modal
        title={editingKey ? '编辑转化规则' : '添加转化规则'}
        open={modalVisible}
        onOk={handleSave}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item
            label="转化名称"
            name="name"
            rules={[{ required: true, message: '请输入转化名称' }]}
          >
            <Input placeholder="例如：注册转化、下单转化" />
          </Form.Item>

          <Form.Item
            label="事件类型"
            name="eventType"
            rules={[{ required: true, message: '请选择事件类型' }]}
          >
            <Select placeholder="选择事件类型">
              <Option value="register">注册</Option>
              <Option value="purchase">下单</Option>
              <Option value="payment">支付</Option>
              <Option value="add_to_cart">加入购物车</Option>
              <Option value="view_content">浏览内容</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="回调URL"
            name="mappingUrl"
            rules={[
              { required: true, message: '请输入回调URL' },
              { type: 'url', message: '请输入有效的URL' },
            ]}
          >
            <Input placeholder="https://api.example.com/callback/register" />
          </Form.Item>

          <Form.Item
            label="点击归因窗口（天）"
            name="clickWindow"
            rules={[{ required: true, message: '请输入点击归因窗口' }]}
          >
            <InputNumber min={1} max={90} placeholder="默认7天" style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            label="浏览归因窗口（天）"
            name="viewWindow"
            rules={[{ required: true, message: '请输入浏览归因窗口' }]}
          >
            <InputNumber min={1} max={90} placeholder="默认1天" style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            label="状态"
            name="status"
            initialValue="enabled"
          >
            <Select>
              <Option value="enabled">启用</Option>
              <Option value="disabled">停用</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ConversionsPage
