import React, { useState } from 'react'
import { Card, Form, Select, Input, InputNumber, Switch, Button, Space, Table, Modal, message, Tag, Slider, Checkbox, Radio } from 'antd'
import { SaveOutlined, PlusOutlined, EditOutlined, DeleteOutlined, CopyOutlined } from '@ant-design/icons'
import type { TableProps } from 'antd'

const { Option } = Select

interface TargetingRule {
  key: string
  name: string
  type: string
  conditions: string[]
  status: string
  lastModified: string
}

const TargetingPage = () => {
  const [form] = Form.useForm()
  const [modalVisible, setModalVisible] = useState(false)
  const [editingKey, setEditingKey] = useState<string | null>(null)

  const [targetings, setTargetings] = useState<TargetingRule[]>([
    {
      key: '1',
      name: '移动端-18-35岁-女性',
      type: 'device',
      conditions: ['device=mobile', 'age=[18,35]', 'gender=female'],
      status: 'enabled',
      lastModified: '2026-03-02 15:30:00',
    },
    {
      key: '2',
      name: '一线城市-高消费',
      type: 'geo',
      conditions: ['city=beijing,shanghai,guangzhou', 'consume_level=high'],
      status: 'enabled',
      lastModified: '2026-03-02 15:30:00',
    },
    {
      key: '3',
      name: '兴趣标签-母婴',
      type: 'interest',
      conditions: ['interest=baby,pregnant,maternal'],
      status: 'disabled',
      lastModified: '2026-03-01 10:00:00',
    },
  ])

  const columns: TableProps<TargetingRule>['columns'] = [
    { title: '定向名称', dataIndex: 'name', key: 'name', width: 200 },
    { title: '定向类型', dataIndex: 'type', key: 'type', width: 120, render: (type) => {
      const typeMap: Record<string, string> = { device: '设备', geo: '地域', interest: '兴趣', behavior: '行为' }
      return typeMap[type] || type
    }},
    { title: '定向条件', dataIndex: 'conditions', key: 'conditions', width: 300, render: (conds) => conds.join(', ') },
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
    { title: '最后修改', dataIndex: 'lastModified', key: 'lastModified', width: 180 },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>编辑</Button>
          <Button icon={<CopyOutlined />} size="small" onClick={() => handleCopy(record)}>复制</Button>
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

  const handleEdit = (record: TargetingRule) => {
    setEditingKey(record.key)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleCopy = (record: TargetingRule) => {
    const newKey = String(targetings.length + 1)
    setTargetings([
      ...targetings,
      {
        ...record,
        key: newKey,
        name: record.name + ' (副本)',
      },
    ])
    message.success('复制成功')
  }

  const handleDelete = (key: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个定向规则吗？',
      onOk: () => {
        setTargetings(targetings.filter(item => item.key !== key))
        message.success('删除成功')
      },
    })
  }

  const handleSave = async () => {
    try {
      const values = await form.validateFields()
      if (editingKey) {
        setTargetings(targetings.map(item =>
          item.key === editingKey ? { ...item, ...values } : item
        ))
        message.success('更新成功')
      } else {
        const newKey = String(targetings.length + 1)
        setTargetings([
          ...targetings,
          {
            ...values,
            key: newKey,
            lastModified: new Date().toLocaleString('zh-CN'),
          },
        ])
        message.success('添加成功')
      }
      setModalVisible(false)
    } catch (error) {
      console.error('表单验证失败:', error)
    }
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <h2>定向投放</h2>
        <p style={{ color: '#666' }}>配置广告投放定向规则，精准触达目标受众</p>
      </div>

      {/* 定向统计 */}
      <Card style={{ marginBottom: 24 }}>
        <Space size="large">
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>活跃定向</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677FF' }}>23</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>覆盖人群(万)</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52C41A' }}>1,234</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>定向效率</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#FA8C16' }}>2.5x</div>
          </div>
        </Space>
      </Card>

      {/* 操作按钮 */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>添加定向</Button>
          <Button icon={<SaveOutlined />}>批量导入</Button>
        </Space>
      </Card>

      {/* 定向规则列表 */}
      <Card>
        <Table
          columns={columns}
          dataSource={targetings}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 添加/编辑模态框 */}
      <Modal
        title={editingKey ? '编辑定向规则' : '添加定向规则'}
        open={modalVisible}
        onOk={handleSave}
        onCancel={() => setModalVisible(false)}
        width={700}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item
            label="定向名称"
            name="name"
            rules={[{ required: true, message: '请输入定向名称' }]}
          >
            <Input placeholder="例如：移动端-18-35岁-女性" />
          </Form.Item>

          <Form.Item
            label="定向类型"
            name="type"
            rules={[{ required: true, message: '请选择定向类型' }]}
          >
            <Select placeholder="选择定向类型">
              <Option value="device">设备定向</Option>
              <Option value="geo">地域定向</Option>
              <Option value="interest">兴趣定向</Option>
              <Option value="behavior">行为定向</Option>
              <Option value="keyword">关键词定向</Option>
            </Select>
          </Form.Item>

          <Card size="small" style={{ marginBottom: 16, background: '#F9F9F9' }}>
            <h4>定向条件</h4>

            <Form.Item label="设备类型" name="device">
              <Checkbox.Group>
                <Checkbox value="mobile">移动端</Checkbox>
                <Checkbox value="tablet">平板</Checkbox>
                <Checkbox value="desktop">PC端</Checkbox>
              </Checkbox.Group>
            </Form.Item>

            <Form.Item label="年龄范围" name="age">
              <Slider range min={18} max={65} defaultValue={[18, 35]} />
            </Form.Item>

            <Form.Item label="性别" name="gender">
              <Radio.Group>
                <Radio value="all">不限</Radio>
                <Radio value="male">男</Radio>
                <Radio value="female">女</Radio>
              </Radio.Group>
            </Form.Item>

            <Form.Item label="地域" name="region">
              <Select mode="multiple" placeholder="选择城市/省份">
                <Option value="beijing">北京</Option>
                <Option value="shanghai">上海</Option>
                <Option value="guangzhou">广州</Option>
                <Option value="shenzhen">深圳</Option>
              </Select>
            </Form.Item>

            <Form.Item label="兴趣标签" name="interests">
              <Select mode="tags" placeholder="输入兴趣标签" />
            </Form.Item>
          </Card>

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

export default TargetingPage
