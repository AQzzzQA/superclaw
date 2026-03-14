import React, { useState } from 'react'
import { Card, Form, Input, Switch, Select, Button, Space, Table, Modal, message, Tag, Divider } from 'antd'
import { SaveOutlined, EditOutlined } from '@ant-design/icons'

const { Option } = Select

interface Setting {
  key: string
  category: string
  name: string
  value: any
  description: string
}

const SettingsPage = () => {
  const [form] = Form.useForm()
  const [modalVisible, setModalVisible] = useState(false)
  const [editingKey, setEditingKey] = useState<string | null>(null)

  const [settings, setSettings] = useState<Setting[]>([
    { key: '1', category: '账户设置', name: '账户名称', value: '我的广告账户', description: '显示在系统中的账户名称' },
    { key: '2', category: '账户设置', name: '货币单位', value: 'CNY', description: '账户消费和预算的货币单位' },
    { key: '3', category: '通知设置', name: '消耗预警', value: true, description: '当消耗达到预算80%时发送通知' },
    { key: '4', category: '通知设置', name: '邮件通知', value: true, description: '接收重要通知邮件' },
    { key: '5', category: 'API设置', name: 'API访问密钥', value: 'sk_**********************', description: '用于API接口调用的访问密钥' },
    { key: '6', category: '安全设置', name: '两步验证', value: false, description: '登录时需要两步验证' },
    { key: '7', category: '数据设置', name: '数据保留期', value: 90, description: '数据保留天数，超过将自动删除' },
  ])

  const columns = [
    { title: '分类', dataIndex: 'category', key: 'category', width: 120 },
    { title: '设置项', dataIndex: 'name', key: 'name', width: 200 },
    {
      title: '当前值',
      dataIndex: 'value',
      key: 'value',
      width: 200,
      render: (value: any, record: Setting) => {
        if (typeof value === 'boolean') {
          return <Switch checked={value} disabled />
        } else if (typeof value === 'number') {
          return <span>{value} 天</span>
        }
        return <span style={{ fontFamily: 'monospace' }}>{String(value)}</span>
      },
    },
    { title: '说明', dataIndex: 'description', key: 'description', ellipsis: true },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>编辑</Button>
      ),
    },
  ]

  const handleEdit = (record: Setting) => {
    setEditingKey(record.key)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleSave = async () => {
    const values = await form.validateFields()
    setSettings(settings.map(item => item.key === editingKey ? { ...item, ...values } : item))
    message.success('设置已保存')
    setModalVisible(false)
  }

  const categories = ['账户设置', '通知设置', 'API设置', '安全设置', '数据设置']

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <h2>系统设置</h2>
      <Card style={{ marginBottom: 24 }}>
        <p style={{ color: '#666', marginBottom: 16 }}>配置系统参数和账户设置</p>
        <Space>
          <Button icon={<SaveOutlined />}>保存所有设置</Button>
          <Button>重置默认</Button>
        </Space>
      </Card>
      {categories.map(cat => (
        <Card key={cat} title={cat} style={{ marginBottom: 16 }}>
          <Table
            columns={columns}
            dataSource={settings.filter(s => s.category === cat)}
            pagination={false}
            showHeader={false}
          />
        </Card>
      ))}
      <Modal title="编辑设置" open={modalVisible} onOk={handleSave} onCancel={() => setModalVisible(false)} width={600}>
        <Form form={form} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item label="设置项" name="name"><Input disabled /></Form.Item>
          <Form.Item label="分类" name="category"><Input disabled /></Form.Item>
          <Form.Item label="说明" name="description"><Input.TextArea disabled /></Form.Item>
          <Form.Item label="当前值" name="value" rules={[{ required: true }]}>
            <Input placeholder="输入新值" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default SettingsPage
