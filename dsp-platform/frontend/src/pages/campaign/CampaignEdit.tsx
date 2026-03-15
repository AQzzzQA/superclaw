import { useParams, useNavigate } from 'react-router-dom'
import { Form, Button, message, Card, Spin } from 'antd'
import { ArrowLeftOutlined } from '@ant-design/icons'
import { useGetCampaignQuery, useUpdateCampaignMutation } from '../../store/services/campaignApi'
import { useGetAccountsQuery } from '../../store/services/accountApi'
import CampaignForm from '../../components/forms/CampaignForm'
import dayjs from 'dayjs'

const CampaignEdit = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const { data: campaign, isLoading } = useGetCampaignQuery(id!, { skip: !id })
  const [updateCampaign, { isLoading: updating }] = useUpdateCampaignMutation()
  const { data: accountsData } = useGetAccountsQuery({ page: 1, pageSize: 100 })

  if (isLoading) {
    return (
      <div style={{ padding: 40, textAlign: 'center' }}>
        <Spin size="large" />
      </div>
    )
  }

  const onFinish = async (values: any) => {
    try {
      const { dateRange, ...rest } = values
      const payload = {
        ...rest,
        startTime: dateRange[0].format('YYYY-MM-DD HH:mm:ss'),
        endTime: dateRange[1].format('YYYY-MM-DD HH:mm:ss'),
      }

      await updateCampaign({ id: id!, data: payload }).unwrap()
      message.success('更新成功')
      navigate('/campaigns')
    } catch (error) {
      message.error('更新失败')
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
            编辑广告计划
          </div>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={campaign ? {
            ...campaign,
            dateRange: [dayjs(campaign.startTime), dayjs(campaign.endTime)],
          } : undefined}
        >
          <CampaignForm
            form={form}
            accounts={accountsData?.items || []}
          />

          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Button onClick={() => navigate('/campaigns')} style={{ marginRight: 8 }}>
              取消
            </Button>
            <Button type="primary" htmlType="submit" loading={updating}>
              保存
            </Button>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default CampaignEdit
