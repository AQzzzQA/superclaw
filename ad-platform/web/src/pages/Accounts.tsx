import React, { useState, useEffect } from 'react'
import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Popconfirm, Progress } from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface Account {
  id: number
  advertiserId: string
  advertiserName: string
  advertiserType: string
  balance: number
  status: string
}

const Accounts: React.FC = () => {
  const [data, setData] = useState<Account[]>([
    {
      id: 1,
      advertiserId: '100000001',
      advertiserName: '测试账户1',
      advertiserType: '直客账户',
      balance: 5000,
      status: 'active',
    },
    {
      id: 2,
      advertiserId: '100000002',
      advertiserName: '测试账户2',
      advertiserType: '代理商账户',
      balance: 10000,
      status: 'active',
    },
  ])

  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      message.success('刷新成功')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingId(null)
    form.resetFields()
    setModalOpen(true)
  }

  const handleEdit = (record: Account) => {
    setEditingId(record.id)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    try {
      setData(data.filter((item) => item.id !== id))
      message.success('删除成功')
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleRecharge = (id: number) => {
    Modal.confirm({
      title: '账户充值',
      content: '确认要为该账户充值吗？',
      onOk: () => {
        message.success('充值申请已提交，等待审核')
      },
    })
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      await new Promise((resolve) => setTimeout(resolve, 500))

      if (editingId) {
        setData(
          data.map((item) =>
            item.id === editingId ? { ...item, ...values } : item
          )
        )
        message.success('更新成功')
      } else {
        const newAccount: Account = {
          id: data.length + 1,
          ...values,
          status: 'active',
        }
        setData([...data, newAccount])
        message.success('添加成功')
      }

      setModalOpen(false)
      form.resetFields()
    } catch (error) {
      message.error('提交失败')
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: '广告主ID', dataIndex: 'advertiserId', key: 'advertiserId', width: 150 },
    { title: '账户名称', dataIndex: 'advertiserName', key: 'advertiserName', width: 200 },
    {
      title: '账户类型',
      dataIndex: 'advertiserType',
      key: 'advertiserType',
      width: 120,
      render: (type: string) => <Tag color="blue">{type}</Tag>,
    },
    { title: '余额 (¥)', dataIndex: 'balance', key: 'balance', width: 120, render: (v: number) => v.toLocaleString() },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>{status === 'active' ? '已授权' : '未授权'}</Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_: any, record: Account) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button size="small" icon={<PlayCircleOutlined />}>启用</Button>
          <Button size="small" icon={<DeleteOutlined />} danger onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 0, minHeight: 'calc(100vh - 64px)' }}>
      <div style={{ padding: 24, background: 'white', marginBottom: 16 }}>
        <Title level={2}>账户管理</Title>
        <Text type="secondary">管理广告账户，查看余额和状态</Text>
      </div>

      <div style={{ padding: 24 }}>
        <Space style={{ marginBottom: 16 }}>
          <Button icon={<ReloadOutlined />} loading={loading} onClick={fetchData}>
            刷新
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加账户
          </Button>
        </Space>

        <Table
          columns={columns}
          dataSource={data}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </div>

      <Modal
        title={editingId ? '编辑账户' : '添加账户'}
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
          <Form.Item name="advertiserId" label="广告主ID" rules={[{ required: true, message: '请输入广告主ID' }]}>
            <Input placeholder="请输入广告主ID" />
          </Form.Item>
          <Form.Item name="advertiserName" label="账户名称" rules={[{ required: true, message: '请输入账户名称' }]}>
            <Input placeholder="请输入账户名称" />
          </Form.Item>
          <Form.Item name="advertiserType" label="账户类型" initialValue="直客账户" rules={[{ required: true, message: '请选择账户类型' }]}>
            <Select>
              <Select.Option value="直客账户">直客账户</Select.Option>
              <Select.Option value="代理商账户">代理商账户</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="balance" label="初始余额" initialValue={5000} rules={[{ required: true, message: '请输入初始余额' }]}>
            <Input type="number" min={0} placeholder="请输入初始余额" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Accounts
