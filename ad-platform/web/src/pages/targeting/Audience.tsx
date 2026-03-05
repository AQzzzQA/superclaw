import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Card,
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  Space,
  Typography,
  Tag,
  message,
  Popconfirm,
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  UserOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography
const { TextArea } = Input

interface AudienceTargeting {
  id: number
  campaignId: number
  targetingType: string
  targetingValue: string
  isInclude: boolean
  createdAt: string
  updatedAt: string
}

const AudienceTargetingPage = () => {
  const navigate = useNavigate()
  const { campaignId } = useParams()

  const [data, setData] = useState<AudienceTargeting[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  const mockData: AudienceTargeting[] = [
    {
      id: 1,
      campaignId: 100001,
      targetingType: 'interest',
      targetingValue: JSON.stringify({ tags: ['科技', '金融', '购物'] }),
      isInclude: true,
      createdAt: '2026-03-01 10:00:00',
      updatedAt: '2026-03-01 10:00:00',
    },
  ]

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    setLoading(true)
    try {
      // 模拟 API 调用
      await new Promise(resolve => setTimeout(resolve, 500))
      setData(mockData)
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingId(null)
    form.resetFields()
    setModalOpen(true)
  }

  const handleEdit = (record: AudienceTargeting) => {
    setEditingId(record.id)
    form.setFieldsValue({
      campaignId: record.campaignId,
      targetingType: record.targetingType,
      targetingValue: record.targetingValue,
      isInclude: record.isInclude,
    })
    setModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setData(data.filter(item => item.id !== id))
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
        // 更新
        setData(
          data.map(item =>
            item.id === editingId
              ? { ...item, ...values, updatedAt: new Date().toISOString() }
              : item
          )
        )
        message.success('更新成功')
      } else {
        // 创建
        const newItem: AudienceTargeting = {
          id: data.length + 1,
          campaignId: values.campaignId,
          targetingType: values.targetingType,
          targetingValue: values.targetingValue,
          isInclude: values.isInclude,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }
        setData([...data, newItem])
        message.success('创建成功')
      }

      setModalOpen(false)
      form.resetFields()
    } catch (error) {
      message.error('提交失败')
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '广告计划ID',
      dataIndex: 'campaignId',
      key: 'campaignId',
      width: 120,
    },
    {
      title: '定向类型',
      dataIndex: 'targetingType',
      key: 'targetingType',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          interest: { text: '兴趣定向', color: 'blue' },
          behavior: { text: '行为定向', color: 'green' },
          custom: { text: '自定义定向', color: 'purple' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    {
      title: '定向值',
      dataIndex: 'targetingValue',
      key: 'targetingValue',
      ellipsis: true,
      render: (value: string) => {
        try {
          const parsed = JSON.parse(value)
          return Array.isArray(parsed) ? parsed.join(', ') : JSON.stringify(parsed)
        } catch {
          return value
        }
      },
    },
    {
      title: '包含/排除',
      dataIndex: 'isInclude',
      key: 'isInclude',
      width: 100,
      render: (isInclude: boolean) => (
        <Tag color={isInclude ? 'green' : 'red'}>
          {isInclude ? '包含' : '排除'}
        </Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 180,
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_: any, record: AudienceTargeting) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除吗？"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
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
          <Title level={2} style={{ margin: 0 }}>
            <UserOutlined /> 人群定向
          </Title>
          <Text type="secondary">基于用户兴趣、行为等标签进行精准定向</Text>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>
            刷新
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
            创建定向
          </Button>
        </Space>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={data}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title={editingId ? '编辑人群定向' : '创建人群定向'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setModalOpen(false)
          form.resetFields()
        }}
        width={600}
        okText="确定"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="campaignId"
            label="广告计划ID"
            rules={[{ required: true, message: '请输入广告计划ID' }]}
          >
            <Input placeholder="请输入广告计划ID" type="number" />
          </Form.Item>

          <Form.Item
            name="targetingType"
            label="定向类型"
            rules={[{ required: true, message: '请选择定向类型' }]}
          >
            <Select placeholder="请选择定向类型">
              <Select.Option value="interest">兴趣定向</Select.Option>
              <Select.Option value="behavior">行为定向</Select.Option>
              <Select.Option value="custom">自定义定向</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="targetingValue"
            label="定向值"
            rules={[{ required: true, message: '请输入定向值（JSON格式）' }]}
          >
            <TextArea
              rows={4}
              placeholder='请输入定向值，例如：{"tags": ["科技", "金融", "购物"]}'
            />
          </Form.Item>

          <Form.Item name="isInclude" label="包含/排除" valuePropName="checked">
            <Switch checkedChildren="包含" unCheckedChildren="排除" defaultChecked />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default AudienceTargetingPage
