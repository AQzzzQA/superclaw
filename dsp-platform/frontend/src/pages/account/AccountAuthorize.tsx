import { useState } from 'react'
import { Form, Input, Select, Button, Card, message, Steps, Space } from 'antd'
import { ArrowRightOutlined } from '@ant-design/icons'
import { useCreateAccountMutation } from '../../store/services/accountApi'
import { useNavigate } from 'react-router-dom'

const { Step } = Steps
const { TextArea } = Input

const AccountAuthorize = () => {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(0)
  const [createAccount] = useCreateAccountMutation()
  const [form] = Form.useForm()

  const platforms = [
    { label: '抖音', value: 'douyin' },
    { label: '快手', value: 'kuaishou' },
    { label: 'B站', value: 'bilibili' },
    { label: '微博', value: 'weibo' },
    { label: '小红书', value: 'xiaohongshu' },
  ]

  const steps = [
    {
      title: '选择平台',
      content: 'accountForm',
    },
    {
      title: '输入授权信息',
      content: 'authInfo',
    },
    {
      title: '完成',
      content: 'complete',
    },
  ]

  const handleNext = async () => {
    try {
      await form.validateFields()
      if (currentStep === 0) {
        setCurrentStep(1)
      } else if (currentStep === 1) {
        // 提交创建账户
        const values = form.getFieldsValue()
        try {
          await createAccount(values).unwrap()
          setCurrentStep(2)
          message.success('账户创建成功')
        } catch (error) {
          message.error('账户创建失败')
        }
      }
    } catch (error) {
      message.error('请填写完整信息')
    }
  }

  const handleBack = () => {
    setCurrentStep(currentStep - 1)
  }

  return (
    <div>
      <Card title="账户授权" style={{ marginBottom: 24 }}>
        <Steps current={currentStep}>
          {steps.map((step, index) => (
            <Step key={index} title={step.title} />
          ))}
        </Steps>
      </Card>

      <Card>
        <Form
          form={form}
          layout="vertical"
        >
          {currentStep === 0 && (
            <Form.Item
              name="platform"
              label="选择平台"
              rules={[{ required: true, message: '请选择平台' }]}
            >
              <Select
                placeholder="请选择媒体平台"
                options={platforms}
                size="large"
              />
            </Form.Item>
          )}

          {currentStep === 1 && (
            <>
              <Form.Item
                name="name"
                label="账户名称"
                rules={[{ required: true, message: '请输入账户名称' }]}
              >
                <Input placeholder="请输入账户名称" />
              </Form.Item>

              <Form.Item
                name="appId"
                label="App ID"
                rules={[{ required: true, message: '请输入App ID' }]}
              >
                <Input placeholder="请输入平台的App ID" />
              </Form.Item>

              <Form.Item
                name="appSecret"
                label="App Secret"
                rules={[{ required: true, message: '请输入App Secret' }]}
              >
                <Input.Password placeholder="请输入平台的App Secret" />
              </Form.Item>

              <Form.Item
                name="accessToken"
                label="Access Token"
                rules={[{ required: true, message: '请输入Access Token' }]}
              >
                <TextArea
                  rows={4}
                  placeholder="请输入授权后获取的Access Token"
                />
              </Form.Item>

              <Card
                type="inner"
                title="授权说明"
                size="small"
                style={{ marginTop: 16, background: '#f6f6f6' }}
              >
                <p style={{ marginBottom: 8 }}>1. 在所选媒体平台的开放平台创建应用</p>
                <p style={{ marginBottom: 8 }}>2. 获取 App ID 和 App Secret</p>
                <p style={{ marginBottom: 0 }}>3. 授权后获取 Access Token 并填入上方</p>
              </Card>
            </>
          )}

          {currentStep === 2 && (
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <div style={{ fontSize: 72, marginBottom: 16 }}>✅</div>
              <h3 style={{ marginBottom: 8 }}>账户授权成功！</h3>
              <p style={{ color: '#666' }}>您的账户已成功添加到系统中</p>
            </div>
          )}
        </Form>

        {currentStep < 2 && (
          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Space>
              {currentStep > 0 && (
                <Button onClick={handleBack}>
                  上一步
                </Button>
              )}
              <Button type="primary" onClick={handleNext}>
                {currentStep === 1 ? '完成' : '下一步'}
                {currentStep < 1 && <ArrowRightOutlined />}
              </Button>
            </Space>
          </div>
        )}

        {currentStep === 2 && (
          <div style={{ marginTop: 24, textAlign: 'center' }}>
            <Button type="primary" onClick={() => navigate('/accounts')}>
              返回账户列表
            </Button>
          </div>
        )}
      </Card>
    </div>
  )
}

export default AccountAuthorize
