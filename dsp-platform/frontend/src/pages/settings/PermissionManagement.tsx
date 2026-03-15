import { Card, Table, Button, Modal, Form, Select, Input, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'

const PermissionManagement = () => {
  const mockUsers = [
    { id: '1', username: 'admin', email: 'admin@example.com', role: 'admin', lastLogin: '2026-03-15 10:30:00' },
    { id: '2', username: 'manager', email: 'manager@example.com', role: 'manager', lastLogin: '2026-03-15 09:15:00' },
    { id: '3', username: 'operator', email: 'operator@example.com', role: 'operator', lastLogin: '2026-03-14 16:45:00' },
    { id: '4', username: 'viewer', email: 'viewer@example.com', role: 'viewer', lastLogin: '2026-03-14 14:20:00' },
  ]

  const columns = [
    { title: '用户名', dataIndex: 'username', key: 'username' },
    { title: '邮箱', dataIndex: 'email', key: 'email' },
    { title: '角色', dataIndex: 'role', key: 'role', render: (role: string) => {
      const roleMap: Record<string, string> = {
        admin: '管理员',
        manager: '经理',
        operator: '操作员',
        viewer: '查看者',
      }
      return roleMap[role] || role
    }},
    { title: '最后登录', dataIndex: 'lastLogin', key: 'lastLogin' },
    {
      title: '操作',
      key: 'actions',
      render: () => (
        <Button.Group>
          <Button size="small" icon={<EditOutlined />}>编辑</Button>
          <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
        </Button.Group>
      ),
    },
  ]

  const handleAddUser = () => {
    Modal.confirm({
      title: '添加用户',
      content: (
        <Form layout="vertical">
          <Form.Item label="用户名" name="username" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item label="邮箱" name="email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item label="角色" name="role" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="admin">管理员</Select.Option>
              <Select.Option value="manager">经理</Select.Option>
              <Select.Option value="operator">操作员</Select.Option>
              <Select.Option value="viewer">查看者</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label="密码" name="password" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
        </Form>
      ),
      onOk: () => {
        message.success('添加成功')
      },
    })
  }

  return (
    <div>
      <Card
        title="权限管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddUser}>
            添加用户
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={mockUsers}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default PermissionManagement
