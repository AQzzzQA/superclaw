import { useParams, useNavigate } from 'react-router-dom'
import { Form, Button, message, Card, Spin } from 'antd'
import { ArrowLeftOutlined } from '@ant-design/icons'
import { useGetAdGroupQuery, useUpdateAdGroupMutation } from '../../store/services/adGroupApi'
import { useGetCampaignsQuery } from '../../store/services/campaignApi'
import AdGroupForm from '../../components/forms/AdGroupForm'

const AdGroupEdit = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const { data: adGroup, isLoading } = useGetAdGroupQuery(id!, { skip: !id })
  const [updateAdGroup, { isLoading: updating }] = useUpdateAdGroupMutation()
  const { data: campaignsData } = useGetCampaignsQuery({ page: 1, pageSize: 100 })

  if (isLoading) {
    return (
      <div style={{ padding: 40, textAlign: 'center' }}>
        <Spin size="large" />
      </div>
    )
  }

  const onFinish = async (values: any) => {
    try {
      await updateAdGroup({ id: id!, data: values }).unwrap()
      message.success('更新成功')
      navigate('/ad-groups')
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
              onClick={() => navigate('/ad-groups')}
              style={{ marginRight: 16 }}
            >
              返回
            </Button>
            编辑广告组
          </div>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={adGroup}
        >
          <AdGroupForm
            form={form}
            campaigns={campaignsData?.items || []}
          />

          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Button onClick={() => navigate('/ad-groups')} style={{ marginRight: 8 }}>
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

export default AdGroupEdit
