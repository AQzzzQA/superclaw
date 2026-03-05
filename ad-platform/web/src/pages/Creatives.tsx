import React, { useState } from 'react'
import { Card, Form, Input, Select, Upload, Button, Space, Table, Modal, message, Tag, Image, Progress } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, UploadOutlined, PlayCircleOutlined, EyeOutlined } from '@ant-design/icons'
import type { TableProps, UploadProps } from 'antd'

const { Option } = Select
const { TextArea } = Input

interface CreativeData {
  key: string
  name: string
  type: string
  format: string
  status: string
  size: string
  duration: number
  clickRate: number
  impressions: number
  createdAt: string
}

const CreativesPage = () => {
  const [form] = Form.useForm()
  const [modalVisible, setModalVisible] = useState(false)
  const [previewVisible, setPreviewVisible] = useState(false)
  const [previewImage, setPreviewImage] = useState('')
  const [editingKey, setEditingKey] = useState<string | null>(null)
  const [fileList, setFileList] = useState<any[]>([])

  const [creatives, setCreatives] = useState<CreativeData[]>([
    {
      key: '1',
      name: '夏季促销-横幅广告',
      type: 'image',
      format: 'jpg',
      status: 'approved',
      size: '150KB',
      duration: 0,
      clickRate: 3.2,
      impressions: 125000,
      createdAt: '2026-03-01 10:00:00',
    },
    {
      key: '2',
      name: '节日营销-视频广告',
      type: 'video',
      format: 'mp4',
      status: 'approved',
      size: '5.2MB',
      duration: 15,
      clickRate: 4.5,
      impressions: 89000,
      createdAt: '2026-03-01 14:30:00',
    },
    {
      key: '3',
      name: '品牌推广-Flash创意',
      type: 'flash',
      format: 'swf',
      status: 'pending',
      size: '2.1MB',
      duration: 10,
      clickRate: 0,
      impressions: 0,
      createdAt: '2026-03-02 09:15:00',
    },
  ])

  const columns: TableProps<CreativeData>['columns'] = [
    { title: '预览', key: 'preview', width: 80, render: (_, record) => (
      record.type === 'image' ? (
        <Button icon={<EyeOutlined />} size="small" onClick={() => handlePreview(record)}>预览</Button>
      ) : (
        <Button icon={<PlayCircleOutlined />} size="small">播放</Button>
      )
    )},
    { title: '创意名称', dataIndex: 'name', key: 'name', width: 200 },
    { title: '类型', dataIndex: 'type', key: 'type', width: 100, render: (t) => {
      const typeMap = { image: '图片', video: '视频', flash: 'Flash', html: 'HTML5' }
      return typeMap[t as keyof typeof typeMap] || t
    }},
    { title: '格式', dataIndex: 'format', key: 'format', width: 80 },
    { title: '大小', dataIndex: 'size', key: 'size', width: 100, align: 'right' },
    { title: '时长(秒)', dataIndex: 'duration', key: 'duration', width: 100, align: 'center', render: (d) => d > 0 ? d : '-' },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (s) => {
        const statusMap = { approved: { text: '已通过', color: 'green' }, pending: { text: '审核中', color: 'orange' }, rejected: { text: '已拒绝', color: 'red' } }
        const st = statusMap[s as keyof typeof statusMap] || statusMap.approved
        return <Tag color={st.color}>{st.text}</Tag>
      },
    },
    { title: '点击率(%)', dataIndex: 'clickRate', key: 'clickRate', width: 120, align: 'right', render: (r) => r > 0 ? r.toFixed(2) + '%' : '-' },
    { title: '曝光量', dataIndex: 'impressions', key: 'impressions', width: 120, align: 'right', render: (i) => i.toLocaleString() },
    { title: '创建时间', dataIndex: 'createdAt', key: 'createdAt', width: 180 },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right' as const,
      render: (_, record) => (
        <Space>
          <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>编辑</Button>
          <Button icon={<DeleteOutlined />} size="small" danger onClick={() => handleDelete(record.key)}>删除</Button>
        </Space>
      ),
    },
  ]

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    onChange: ({ fileList: newFileList }) => setFileList(newFileList),
    beforeUpload: () => false,
  }

  const handleAdd = () => {
    setModalVisible(true)
    setEditingKey(null)
    form.resetFields()
    setFileList([])
  }

  const handleEdit = (record: CreativeData) => {
    setEditingKey(record.key)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handlePreview = (record: CreativeData) => {
    setPreviewImage('https://via.placeholder.com/300x200?text=' + record.name)
    setPreviewVisible(true)
  }

  const handleDelete = (key: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个创意吗？',
      onOk: () => {
        setCreatives(creatives.filter(item => item.key !== key))
        message.success('删除成功')
      },
    })
  }

  const handleSave = async () => {
    const values = await form.validateFields()
    if (editingKey) {
      setCreatives(creatives.map(item => item.key === editingKey ? { ...item, ...values } : item))
      message.success('更新成功')
    } else {
      const newKey = String(creatives.length + 1)
      setCreatives([
        ...creatives,
        {
          ...values,
          key: newKey,
          status: 'pending',
          clickRate: 0,
          impressions: 0,
          createdAt: new Date().toLocaleString('zh-CN'),
        },
      ])
      message.success('上传成功，等待审核')
    }
    setModalVisible(false)
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ marginBottom: 24 }}>
        <h2>创意管理</h2>
        <p style={{ color: '#666' }}>上传和管理广告创意素材</p>
      </div>

      {/* 创意统计 */}
      <Card style={{ marginBottom: 24 }}>
        <Space size="large">
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>总创意数</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677FF' }}>{creatives.length}</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>已通过</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52C41A' }}>{creatives.filter(c => c.status === 'approved').length}</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>审核中</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#FA8C16' }}>{creatives.filter(c => c.status === 'pending').length}</div>
          </div>
          <div>
            <div style={{ color: '#666', marginBottom: 8 }}>平均点击率</div>
            <div style={{ fontSize: 24, fontWeight: 'bold', color: '#722ED1' }}>3.85%</div>
          </div>
        </Space>
      </Card>

      {/* 操作按钮 */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>上传创意</Button>
          <Button icon={<UploadOutlined />}>批量上传</Button>
          <Button icon={<EditOutlined />}>批量编辑</Button>
        </Space>
      </Card>

      {/* 创意列表 */}
      <Card>
        <Table
          columns={columns}
          dataSource={creatives}
          pagination={{ pageSize: 10, showSizeChanger: true }}
          scroll={{ x: 1400 }}
        />
      </Card>

      {/* 上传/编辑模态框 */}
      <Modal
        title={editingKey ? '编辑创意' : '上传创意'}
        open={modalVisible}
        onOk={handleSave}
        onCancel={() => setModalVisible(false)}
        width={700}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item
            label="创意名称"
            name="name"
            rules={[{ required: true, message: '请输入创意名称' }]}
          >
            <Input placeholder="例如：夏季促销-横幅广告" />
          </Form.Item>

          <Form.Item
            label="创意类型"
            name="type"
            rules={[{ required: true, message: '请选择创意类型' }]}
          >
            <Select placeholder="选择创意类型">
              <Option value="image">图片创意</Option>
              <Option value="video">视频创意</Option>
              <Option value="flash">Flash创意</Option>
              <Option value="html">HTML5创意</Option>
            </Select>
          </Form.Item>

          <Form.Item label="上传文件" rules={[{ required: !editingKey, message: '请上传文件' }]}>
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />}>选择文件</Button>
            </Upload>
            <div style={{ marginTop: 8, color: '#999', fontSize: 12 }}>
              支持格式：JPG、PNG、GIF、MP4（单个文件不超过5MB）
            </div>
          </Form.Item>

          <Form.Item
            label="点击跳转链接"
            name="landingUrl"
            rules={[{ required: true, message: '请输入跳转链接' }, { type: 'url', message: '请输入有效的URL' }]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>

          <Form.Item label="创意描述" name="description">
            <TextArea rows={3} placeholder="描述创意内容、设计理念等" />
          </Form.Item>

          <Form.Item label="尺寸规格" name="sizeSpec">
            <Select placeholder="选择尺寸规格" defaultValue="custom">
              <Option value="320x50">320x50 (移动通栏)</Option>
              <Option value="640x100">640x100 (iPad横幅)</Option>
              <Option value="300x250">300x250 (中矩形)</Option>
              <Option value="custom">自定义</Option>
            </Select>
          </Form.Item>

          {form.getFieldValue('type') === 'video' && (
            <Form.Item label="视频时长限制">
              <Space>
                <span>5-30秒</span>
                <Progress percent={50} status="active" showInfo={false} style={{ width: 150 }} />
              </Space>
            </Form.Item>
          )}
        </Form>
      </Modal>

      {/* 预览模态框 */}
      <Modal open={previewVisible} footer={null} onCancel={() => setPreviewVisible(false)} width={600}>
        <Image src={previewImage} alt="预览" style={{ width: '100%' }} />
      </Modal>
    </div>
  )
}

export default CreativesPage
