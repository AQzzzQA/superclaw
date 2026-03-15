import { Card, Form, Input, InputNumber, Select, Button, Switch, message } from 'antd'

const SystemSettings = () => {
  const [form] = Form.useForm()

  const onFinish = (values: any) => {
    console.log('保存设置:', values)
    message.success('保存成功')
  }

  return (
    <div>
      <Card title="系统设置" style={{ marginBottom: 16 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            dataRetentionDays: 90,
            autoRefreshInterval: 30,
            emailNotifications: true,
            alertThreshold: 1000,
          }}
        >
          <Form.Item
            name="dataRetentionDays"
            label="数据保留天数"
            tooltip="超过此天数的数据将被归档或删除"
          >
            <InputNumber min={30} max={365} style={{ width: 200 }} />
          </Form.Item>

          <Form.Item
            name="autoRefreshInterval"
            label="自动刷新间隔（秒）"
          >
            <InputNumber min={10} max={300} style={{ width: 200 }} />
          </Form.Item>

          <Form.Item
            name="alertThreshold"
            label="消耗告警阈值（元）"
            tooltip="当消耗超过此阈值时发送告警"
          >
            <InputNumber min={100} max={100000} style={{ width: 200 }} />
          </Form.Item>

          <Form.Item
            name="emailNotifications"
            label="邮件通知"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">保存</Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default SystemSettings
