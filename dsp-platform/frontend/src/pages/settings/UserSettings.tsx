import { Card, Form, Input, Button, message } from 'antd'

const UserSettings = () => {
  const [form] = Form.useForm()

  const onFinish = (values: any) => {
    console.log('保存设置:', values)
    message.success('保存成功')
  }

  return (
    <div>
      <Card title="用户设置">
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            username: 'admin',
            email: 'admin@example.com',
            phone: '13800138000',
          }}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { required: true },
              { type: 'email' },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="phone"
            label="手机号"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="修改密码"
          >
            <Input.Password placeholder="新密码（留空则不修改）" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">保存</Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default UserSettings
