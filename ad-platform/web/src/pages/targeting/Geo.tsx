import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Switch, InputNumber } from 'antd'
import { EnvironmentOutlined, ReloadOutlined, PlusOutlined, DeleteOutlined } from '@ant-design/icons'

const { Title, Text } = Typography

interface GeoTargeting {
  id: number
  campaignId: number
  tenantId: number
  targetingType: string
  geoLevel: number
  geoList: string
  isExclude: boolean
  latitude?: string
  longitude?: string
  radius?: number
  createdAt: string
  updatedAt: string
}

const GeoTargetingPage: React.FC = () => {
  const navigate = useNavigate()
  const [data, setData] = useState<GeoTargeting[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    setLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 300))
      setData([
        {
          id: 1,
          campaignId: 100001,
          tenantId: 1,
          targetingType: 'city',
          geoLevel: 2,
          geoList: JSON.stringify(['北京', '上海', '广州', '深圳']),
          isExclude: false,
          createdAt: '2026-03-01 10:00:00',
          updatedAt: '2026-03-01 10:00:00',
        },
      ])
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingId(null)
    form.resetFields()
    form.setFieldsValue({ isExclude: false })
    setModalOpen(true)
  }

  const handleEdit = (record: GeoTargeting) => {
    setEditingId(record.id)
    form.setFieldsValue({
      targetingType: record.targetingType,
      geoLevel: record.geoLevel,
      geoList: JSON.parse(record.geoList),
      isExclude: record.isExclude,
      latitude: record.latitude,
      longitude: record.longitude,
      radius: record.radius,
    })
    setModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这条地域定向吗？',
      onOk: () => {
        setData(data.filter((item) => item.id !== id))
        message.success('删除成功')
      },
    })
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      await new Promise((resolve) => setTimeout(resolve, 500))

      const geoListStr = Array.isArray(values.geoList) ? JSON.stringify(values.geoList) : values.geoList

      if (editingId) {
        setData(
          data.map((item) =>
            item.id === editingId
              ? {
                  ...item,
                  ...values,
                  geoList: geoListStr,
                  updatedAt: new Date().toISOString(),
                }
              : item
          )
        )
        message.success('更新成功')
      } else {
        const newItem: GeoTargeting = {
          id: data.length + 1,
          campaignId: values.campaignId,
          tenantId: 1,
          targetingType: values.targetingType,
          geoLevel: values.geoLevel,
          geoList: geoListStr,
          isExclude: values.isExclude || false,
          latitude: values.latitude,
          longitude: values.longitude,
          radius: values.radius,
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
      title: '地域类型',
      dataIndex: 'targetingType',
      key: 'targetingType',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          province: { text: '省份', color: 'blue' },
          city: { text: '城市', color: 'green' },
          district: { text: '区县', color: 'orange' },
          business_area: { text: '商圈', color: 'purple' },
          lbs: { text: 'LBS', color: 'red' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    {
      title: '地域级别',
      dataIndex: 'geoLevel',
      key: 'geoLevel',
      width: 100,
      render: (level: number) => {
        const levelMap: Record<number, string> = { 1: '省', 2: '市', 3: '区', 4: '商圈', 5: 'LBS' }
        return levelMap[level] || level
      },
    },
    {
      title: '地域列表',
      dataIndex: 'geoList',
      key: 'geoList',
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
      dataIndex: 'isExclude',
      key: 'isExclude',
      width: 100,
      render: (isExclude: boolean) => (
        <Tag color={isExclude ? 'red' : 'green'}>{isExclude ? '排除' : '包含'}</Tag>
      ),
    },
    {
      title: 'LBS信息',
      key: 'lbs',
      width: 150,
      render: (_: any, record: GeoTargeting) => {
        if (record.latitude && record.longitude && record.radius) {
          return `${record.latitude}, ${record.longitude} (${record.radius}m)`
        }
        return '-'
      },
    },
    { title: '创建时间', dataIndex: 'createdAt', key: 'createdAt', width: 180 },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_: any, record: GeoTargeting) => (
        <Space>
          <Button size="small" type="primary" onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button size="small" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2}>
            <EnvironmentOutlined /> 地域定向
          </Title>
          <Text type="secondary">按省、市、区、商圈、LBS 位置定向</Text>
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
        <Table columns={columns} dataSource={data} rowKey="id" loading={loading} scroll={{ x: 1500 }} />
      </Card>

      <Modal
        title={editingId ? '编辑地域定向' : '创建地域定向'}
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
          <Form.Item name="campaignId" label="广告计划ID" rules={[{ required: true, message: '请输入广告计划ID' }]}>
            <Input placeholder="请输入广告计划ID" type="number" />
          </Form.Item>

          <Form.Item name="targetingType" label="地域类型" rules={[{ required: true, message: '请选择地域类型' }]}>
            <Select placeholder="请选择地域类型">
              <Select.Option value="province">省份</Select.Option>
              <Select.Option value="city">城市</Select.Option>
              <Select.Option value="district">区县</Select.Option>
              <Select.Option value="business_area">商圈</Select.Option>
              <Select.Option value="lbs">LBS位置</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item name="geoLevel" label="地域级别" rules={[{ required: true, message: '请选择地域级别' }]}>
            <Select placeholder="请选择地域级别">
              <Select.Option value={1}>省级 (1)</Select.Option>
              <Select.Option value={2}>市级 (2)</Select.Option>
              <Select.Option value={3}>区级 (3)</Select.Option>
              <Select.Option value={4}>商圈 (4)</Select.Option>
              <Select.Option value={5}>LBS (5)</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="geoList"
            label="地域列表（JSON 格式）"
            rules={[{ required: true, message: '请输入地域列表' }]}
          >
            <Input.TextArea
              rows={3}
              placeholder='请输入地域列表，如：["北京", "上海", "广州"]'
            />
          </Form.Item>

          <Form.Item name="isExclude" label="排除模式" valuePropName="checked">
            <Switch checkedChildren="排除" unCheckedChildren="包含" />
          </Form.Item>

          <div style={{ border: '1px solid #d9d9d9', padding: 16, borderRadius: 4 }}>
            <Text strong>LBS 定向配置</Text>
            <Form.Item name="latitude" label="纬度" style={{ marginBottom: 8 }}>
              <Input placeholder="请输入纬度" />
            </Form.Item>
            <Form.Item name="longitude" label="经度" style={{ marginBottom: 8 }}>
              <Input placeholder="请输入经度" />
            </Form.Item>
            <Form.Item name="radius" label="半径（米）">
              <InputNumber min={1} max={10000} placeholder="请输入半径" style={{ width: '100%' }} />
            </Form.Item>
          </div>
        </Form>
      </Modal>
    </div>
  )
}

export default GeoTargetingPage
