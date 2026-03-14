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
  TimePicker,
  Checkbox,
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons'
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'

const { Title, Text } = Typography
const { RangePicker: TimeRangePicker } = TimePicker

interface TimeTargeting {
  id: number
  campaignId: number
  targetingType: string
  timeConfig: string
  timezone: string
  createdAt: string
  updatedAt: string
}

const TimeTargetingPage = () => {
  const navigate = useNavigate()

  const [data, setData] = useState<TimeTargeting[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  const mockData: TimeTargeting[] = [
    {
      id: 1,
      campaignId: 100001,
      targetingType: 'hour',
      timeConfig: JSON.stringify({
        hours: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
      }),
      timezone: 'Asia/Shanghai',
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
    form.setFieldsValue({ timezone: 'Asia/Shanghai' })
    setModalOpen(true)
  }

  const handleEdit = (record: TimeTargeting) => {
    setEditingId(record.id)
    const config = JSON.parse(record.timeConfig)
    form.setFieldsValue({
      ...record,
      ...config,
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

      const timeConfig = {
        hours: values.hours || [],
        days: values.days || [],
        weeks: values.weeks || [],
        customRanges: values.customRanges || [],
      }

      const formattedValues = {
        campaignId: values.campaignId,
        targetingType: values.targetingType,
        timeConfig: JSON.stringify(timeConfig),
        timezone: values.timezone,
      }

      if (editingId) {
        setData(data.map(item => item.id === editingId ? { ...item, ...formattedValues, updatedAt: new Date().toISOString() } : item))
        message.success('更新成功')
      } else {
        const newItem: TimeTargeting = {
          id: data.length + 1,
          ...formattedValues,
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
      title: '时间类型',
      dataIndex: 'targetingType',
      key: 'targetingType',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          hour: { text: '按小时', color: 'blue' },
          day: { text: '按天', color: 'green' },
          week: { text: '按星期', color: 'orange' },
          custom: { text: '自定义', color: 'purple' },
        }
        const config = typeMap[type] || { text: type, color: 'default' }
        return <Tag color={config.color}>{config.text}</Tag>
      },
    },
    {
      title: '时间配置',
      dataIndex: 'timeConfig',
      key: 'timeConfig',
      ellipsis: true,
      render: (value: string) => {
        try {
          const parsed = JSON.parse(value)
          if (parsed.hours) return `小时: ${parsed.hours.join(', ')}`
          if (parsed.days) return `天数: ${parsed.days.join(', ')}`
          if (parsed.weeks) return `星期: ${parsed.weeks.join(', ')}`
          if (parsed.customRanges) return `自定义: ${parsed.customRanges.length} 条`
          return JSON.stringify(parsed)
        } catch {
          return value
        }
      },
    },
    {
      title: '时区',
      dataIndex: 'timezone',
      key: 'timezone',
      width: 150,
      render: (tz: string) => <Tag color="cyan">{tz}</Tag>,
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
      render: (_: any, record: TimeTargeting) => (
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

  const hourOptions = Array.from({ length: 24 }, (_, i) => i)

  const dayOptions = Array.from({ length: 31 }, (_, i) => i + 1)

  const weekOptions = [
    { label: '周一', value: 1 },
    { label: '周二', value: 2 },
    { label: '周三', value: 3 },
    { label: '周四', value: 4 },
    { label: '周五', value: 5 },
    { label: '周六', value: 6 },
    { label: '周日', value: 7 },
  ]

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2} style={{ margin: 0 }}>
            <ClockCircleOutlined /> 时间定向
          </Title>
          <Text type="secondary">按小时、星期、自定义时间段定向</Text>
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
        <Table columns={columns} dataSource={data} rowKey="id" loading={loading} scroll={{ x: 1300 }} />
      </Card>

      <Modal
        title={editingId ? '编辑时间定向' : '创建时间定向'}
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
          <Form.Item name="targetingType" label="时间类型" rules={[{ required: true, message: '请选择时间类型' }]}>
            <Select placeholder="请选择时间类型">
              <Select.Option value="hour">按小时</Select.Option>
              <Select.Option value="day">按天</Select.Option>
              <Select.Option value="week">按星期</Select.Option>
              <Select.Option value="custom">自定义</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item label="按小时选择">
            <Form.Item name="hours" noStyle>
              <Select
                mode="multiple"
                placeholder="请选择小时"
                options={hourOptions.map((h) => ({ label: `${h}:00`, value: h }))}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Form.Item>

          <Form.Item label="按天选择">
            <Form.Item name="days" noStyle>
              <Select
                mode="multiple"
                placeholder="请选择天数"
                options={dayOptions.map((d) => ({ label: `每月${d}日`, value: d }))}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Form.Item>

          <Form.Item label="按星期选择">
            <Form.Item name="weeks" noStyle>
              <Checkbox.Group options={weekOptions} style={{ width: '100%' }} />
            </Form.Item>
          </Form.Item>

          <Form.Item name="timezone" label="时区" rules={[{ required: true, message: '请选择时区' }]}>
            <Select placeholder="请选择时区">
              <Select.Option value="Asia/Shanghai">上海 (GMT+8)</Select.Option>
              <Select.Option value="Asia/Hong_Kong">香港 (GMT+8)</Select.Option>
              <Select.Option value="Asia/Tokyo">东京 (GMT+9)</Select.Option>
              <Select.Option value="UTC">UTC (GMT+0)</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default TimeTargetingPage
