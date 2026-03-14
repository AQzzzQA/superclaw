import React, { useState } from 'react'
import { Card, Form, Input, Button, Space, Avatar, message, Modal, Divider, Row, Col, Tag } from 'antd'
import { SaveOutlined, EditOutlined, LockOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons'

const { TextArea } = Input

const ProfilePage = () => {
  const [form] = Form.useForm()
  const [passwordForm] = Form.useForm()
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [passwordModalVisible, setPasswordModalVisible] = useState(false)

  const [user, setUser] = useState({
    username: 'admin',
    realName: '管理员',
    email: 'admin@example.com',
    phone: '13800138000',
    avatar: null,
    role: '超级管理员',
    department: '运营部',
    createTime: '2026-01-01',
    lastLogin: '2026-03-02 15:30:00',
    status: 'active',
  })

  const handleProfileSave = async () => {
    const values = await form.validateFields()
    setUser({ ...user, ...values })
    message.success('个人信息已更新')
    setEditModalVisible(false)
  }

  const handlePasswordChange = async () => {
    const values = await passwordForm.validateFields()
    if (values.newPassword !== values.confirmPassword) {
      message.error('两次输入的密码不一致')
      return
    }
    message.success('密码修改成功，请重新登录')
    setPasswordModalVisible(false)
    passwordForm.resetFields()
  }

  return (
    <div style={{ padding: 24, background: '#F5F7FA', minHeight: 'calc(100vh - 64px)' }}>
      <h2>个人中心</h2>
      <Card style={{ marginBottom: 24 }}>
        <Space align="start" size="large">
          <Avatar size={100} style={{ backgroundColor: '#1677FF' }}>管</Avatar>
          <div>
            <h3 style={{ marginBottom: 8 }}>{user.realName}</h3>
            <p style={{ color: '#666', marginBottom: 4 }}>{user.username}</p>
            <Tag color="green">在线</Tag>
          </div>
        </Space>
      </Card>

      <Row gutter={24}>
        <Col span={16}>
          <Card title="基本信息" style={{ marginBottom: 16 }}>
            <Form form={form} layout="vertical" initialValues={user}>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item label="用户名" name="username">
                    <Input disabled />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item label="真实姓名" name="realName" rules={[{ required: true }]}>
                    <Input />
                  </Form.Item>
                </Col>
              </Row>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item label="邮箱" name="email" rules={[{ required: true, type: 'email' }]}>
                    <Input prefix={<MailOutlined />} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item label="手机号" name="phone" rules={[{ required: true }]}>
                    <Input prefix={<PhoneOutlined />} />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item label="部门" name="department">
                <Input />
              </Form.Item>
              <Space>
                <Button type="primary" icon={<SaveOutlined />} onClick={handleProfileSave}>保存</Button>
                <Button icon={<EditOutlined />} onClick={() => setEditModalVisible(true)}>更多编辑</Button>
              </Space>
            </Form>
          </Card>

          <Card title="安全设置">
            <Divider>密码修改</Divider>
            <Form form={passwordForm} layout="vertical">
              <Form.Item label="原密码" name="oldPassword" rules={[{ required: true }]}>
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              <Form.Item label="新密码" name="newPassword" rules={[{ required: true, min: 6 }]}>
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              <Form.Item label="确认密码" name="confirmPassword" rules={[{ required: true }]}>
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              <Button type="primary" onClick={handlePasswordChange}>修改密码</Button>
            </Form>
          </Card>
        </Col>

        <Col span={8}>
          <Card title="账户信息" style={{ marginBottom: 16 }}>
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div><span style={{ color: '#666' }}>角色：</span><strong>{user.role}</strong></div>
              <div><span style={{ color: '#666' }}>部门：</span><strong>{user.department}</strong></div>
              <div><span style={{ color: '#666' }}>创建时间：</span><strong>{user.createTime}</strong></div>
              <div><span style={{ color: '#666' }}>最后登录：</span><strong>{user.lastLogin}</strong></div>
              <div><span style={{ color: '#666' }}>状态：</span><Tag color="green">正常</Tag></div>
            </Space>
          </Card>

          <Card title="快速操作">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button block icon={<EditOutlined />}>编辑资料</Button>
              <Button block icon={<LockOutlined />}>安全设置</Button>
              <Button block>查看日志</Button>
            </Space>
          </Card>
        </Col>
      </Row>

      <Modal title="编辑个人信息" open={editModalVisible} onOk={handleProfileSave} onCancel={() => setEditModalVisible(false)} width={600}>
        <Form form={form} layout="vertical">
          <Form.Item label="真实姓名" name="realName"><Input /></Form.Item>
          <Form.Item label="邮箱" name="email"><Input /></Form.Item>
          <Form.Item label="手机号" name="phone"><Input /></Form.Item>
          <Form.Item label="部门" name="department"><Input /></Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ProfilePage
