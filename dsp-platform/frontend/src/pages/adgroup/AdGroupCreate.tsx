import { Form, Button, message, Card } from 'antd'
import { ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useCreateAdGroupMutation } from '../../store/services/adGroupApi'
import { useGetCampaignsQuery } from '../../store/services/campaignApi'
import AdGroupForm from '../../components/forms/AdGroupForm'

const AdGroupCreate = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [createAdGroup, { isLoading: creating }] = useCreateAdGroupMutation()
  const { data: campaignsData } = useGetCampaignsQuery({ page: 1, pageSize: 100 })

  const onFinish = async (values: any) => {
    try {
      await createAdGroup(values).unwrap()
      message.success('创建成功')
      navigate('/ad-groups')
    } catch (error) {
      message.error('创建失败')
    }
  }

  return (
    <div>
      <Card
        title={
          <div>
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/ad-groups')}
              style={{ marginRight: 16 }}
            >
              返回
            </Button>
            新建广告组
          </div>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            bidType: 'cpc',
          }}
        >
          <AdGroupForm
            form={form}
            campaigns={campaignsData?.items || []}
          />

          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Button onClick={() => navigate('/ad-groups')} style={{ marginRight: 8 }}>
              取消
            </Button>
            <Button type="primary" htmlType="submit" loading={creating}>
              创建
            </Button>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default AdGroupCreate
