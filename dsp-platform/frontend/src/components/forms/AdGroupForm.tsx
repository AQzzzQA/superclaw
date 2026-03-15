import { Form, Input, Select, InputNumber, Card, Row, Col } from 'antd'
import TargetingForm from './TargetingForm'
import type { AdGroupFormData, Campaign } from '../../types'

interface AdGroupFormProps {
  form: any
  campaigns: Campaign[]
  initialValues?: Partial<AdGroupFormData>
}

const AdGroupForm = ({ form, campaigns, initialValues }: AdGroupFormProps) => {
  return (
    <>
      <Card title="基本信息" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="name"
              label="广告组名称"
              rules={[{ required: true, message: '请输入广告组名称' }]}
            >
              <Input placeholder="请输入广告组名称" maxLength={100} />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              name="campaignId"
              label="所属计划"
              rules={[{ required: true, message: '请选择所属计划' }]}
            >
              <Select
                placeholder="请选择所属计划"
                options={campaigns.map((camp) => ({
                  label: camp.name,
                  value: camp.id,
                }))}
              />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              name="bidType"
              label="出价方式"
              rules={[{ required: true, message: '请选择出价方式' }]}
            >
              <Select
                placeholder="请选择出价方式"
                options={[
                  { label: 'CPC（按点击付费）', value: 'cpc' },
                  { label: 'CPM（按千次展示付费）', value: 'cpm' },
                  { label: 'oCPC（按优化点击付费）', value: 'ocpc' },
                  { label: 'oCPM（按优化千次展示付费）', value: 'ocpm' },
                ]}
              />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              name="bid"
              label="出价金额（元）"
              rules={[{ required: true, message: '请输入出价金额' }]}
            >
              <InputNumber
                min={0.01}
                max={10000}
                precision={2}
                placeholder="请输入出价金额"
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>

          <Col span={12}>
            <Form.Item
              name="budget"
              label="广告组预算（元）"
              rules={[{ required: true, message: '请输入预算金额' }]}
            >
              <InputNumber
                min={1}
                max={100000}
                precision={2}
                placeholder="请输入预算金额"
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="定向设置">
        <TargetingForm form={form} initialValues={initialValues?.targeting} />
      </Card>
    </>
  )
}

export default AdGroupForm
