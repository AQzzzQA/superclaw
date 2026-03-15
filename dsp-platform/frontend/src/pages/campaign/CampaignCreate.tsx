import { Form, Button, message, Card } from 'antd'
import { ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useCreateCampaignMutation } from '../../store/services/campaignApi'
import { useGetAccountsQuery } from '../../store/services/accountApi'
import CampaignForm from '../../components/forms/CampaignForm'
import dayjs from 'dayjs'

const CampaignCreate = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [createCampaign, { isLoading: creating }] = useCreateCampaignMutation()
  const { data: accountsData } = useGetAccountsQuery({ page: 1, pageSize: 100 })

  const onFinish = async (values: any) => {
    try {
      const { dateRange, ...rest } = values
      const payload = {
        ...rest,
        startTime: dateRange[0].format('YYYY-MM-DD HH:mm:ss'),
        endTime: dateRange[1].format('YYYY-MM-DD HH:mm:ss'),
      }

      await createCampaign(payload).unwrap()
      message.success('创建成功')
      navigate('/campaigns')
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
              onClick={() => navigate('/campaigns')}
              style={{ marginRight: 16 }}
            >
              返回
            </Button>
            新建广告计划
          </div>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            campaignType: 'search',
            budgetType: 'daily',
          }}
        >
          <CampaignForm
            form={form}
            accounts={accountsData?.items || []}
          />

          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Button onClick={() => navigate('/campaigns')} style={{ marginRight: 8 }}>
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

export default CampaignCreate
