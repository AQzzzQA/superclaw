import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card,
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
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
  MobileOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface DeviceTargeting {
  id: number
  campaignId: number
  osType?: string
  osVersionMin?: string
  osVersionMax?: string
  deviceBrand?: string
  deviceModel?: string
  deviceType?: string
  networkType?: string
  createdAt: string
  updatedAt: string
}

const DeviceTargetingPage = () => {
  const navigate = useNavigate()

  const [data, setData] = useState<DeviceTargeting[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  const mockData: DeviceTargeting[] = [
    {
      id: 1,
      campaignId: 100001,
      osType: 'iOS',
      osVersionMin: '14.0',
      deviceType: 'phone',
      networkType: '4G',
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

  const handleEdit = (record: DeviceTargeting) => {
    setEditingId(record.id)
    form.setFieldsValue(record)
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
        setData(data.map(item => item.id === editingId ? { ...item, ...values, updatedAt: new Date().toISOString() } : item))
        message.success('更新成功')
      } else {
        const newItem: DeviceTargeting = {
          id: data.length + 1,
          ...values,
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
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    {
      title: '广告计划ID',
      dataIndex: 'campaignId',
      key: 'campaignId',
      width: 120,
    },
    {
      title: '操作系统',
      dataIndex: 'osType',
      key: 'osType',
      width: 100,
      render: (os?: string) => os ? <Tag color="blue">{os}</Tag> : '-',
    },
    {
      title: '版本范围',
      key: 'version',
      width: 150,
      render: (_: any, record: DeviceTargeting) => {
        if (record.osVersionMin && record.osVersionMax) {
          return `${record.osVersionMin} - ${record.osVersionMax}`
        }
        return record.osVersionMin || record.osVersionMax || '-'
      },
    },
    {
      title: '设备品牌',
      dataIndex: 'deviceBrand',
      key: 'deviceBrand',
      width: 120,
    },
    {
      title: '设备型号',
      dataIndex: 'deviceModel',
      key: 'deviceModel',
      width: 120,
    },
    {
      title: '设备类型',
      dataIndex: 'deviceType',
      key: 'deviceType',
      width: 100,
      render: (type?: string) => type ? <Tag color="green">{type}</Tag> : '-',
    },
    {
      title: '网络类型',
      dataIndex: 'networkType',
      key: 'networkType',
      width: 100,
      render: (type?: string) => type ? <Tag color="orange">{type}</Tag> : '-',
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
      fixed: 'right' as const,
      render: (_: any, record: DeviceTargeting) => (
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

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2} style={{ margin: 0 }}>
            <MobileOutlined /> 设备定向
          </Title>
          <Text type="secondary">按操作系统、设备品牌、网络类型等定向</Text>
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
          scroll={{ x: 1400 }}
        />
      </Card>

      <Modal
        title={editingId ? '编辑设备定向' : '创建设备定向'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => { setModalOpen(false); form.resetFields() }}
        width={600}
        okText="确定"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="campaignId" label="广告计划ID" rules={[{ required: true, message: '请输入广告计划ID' }]}>
            <Input placeholder="请输入广告计划ID" type="number" />
          </Form.Item>
          <Form.Item name="osType" label="操作系统">
            <Select placeholder="请选择操作系统" allowClear>
              <Select.Option value="iOS">iOS</Select.Option>
              <Select.Option value="Android">Android</Select.Option>
              <Select.Option value="All">全部</Select.Option>
            </Select>
          </Form.Item>
          <Space style={{ width: '100%' }}>
            <Form.Item name="osVersionMin" label="最低版本" style={{ width: '50%' }}>
              <Input placeholder="如：14.0" />
            </Form.Item>
            <Form.Item name="osVersionMax" label="最高版本" style={{ width: '50%' }}>
              <Input placeholder="如：15.0" />
            </Form.Item>
          </Space>
          <Form.Item name="deviceBrand" label="设备品牌">
            <Input placeholder="请输入设备品牌，如：Apple" />
          </Form.Item>
          <Form.Item name="deviceModel" label="设备型号">
            <Input placeholder="请输入设备型号，如：iPhone 13" />
          </Form.Item>
          <Form.Item name="deviceType" label="设备类型">
            <Select placeholder="请选择设备类型" allowClear>
              <Select.Option value="phone">手机</Select.Option>
              <Select.Option value="tablet">平板</Select.Option>
              <Select.Option value="all">全部</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="networkType" label="网络类型">
            <Select placeholder="请选择网络类型" allowClear>
              <Select.Option value="WiFi">WiFi</Select.Option>
              <Select.Option value="4G">4G</Select.Option>
              <Select.Option value="5G">5G</Select.Option>
              <Select.Option value="All">全部</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default DeviceTargetingPage
