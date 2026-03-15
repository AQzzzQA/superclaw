import { Form, Input, Select, DatePicker, InputNumber, Card, Row, Col } from 'antd'
import dayjs from 'dayjs'
import type { CampaignFormData, Account } from '../../types'

const { RangePicker } = DatePicker

interface CampaignFormProps {
  form: any
  accounts: Account[]
  initialValues?: Partial<CampaignFormData>
}

const CampaignForm = ({ form, accounts, initialValues }: CampaignFormProps) => {
  return (
    <Card title="基本信息">
      <Row gutter={16}>
        <Col span={24}>
          <Form.Item
            name="name"
            label="计划名称"
            rules={[{ required: true, message: '请输入计划名称' }]}
          >
            <Input placeholder="请输入广告计划名称" maxLength={100} />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="accountId"
            label="所属账户"
            rules={[{ required: true, message: '请选择账户' }]}
          >
            <Select
              placeholder="请选择账户"
              options={accounts.map((acc) => ({
                label: `${acc.name} (${acc.platform})`,
                value: acc.id,
              }))}
            />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="campaignType"
            label="计划类型"
            rules={[{ required: true, message: '请选择计划类型' }]}
          >
            <Select
              placeholder="请选择计划类型"
              options={[
                { label: '搜索广告', value: 'search' },
                { label: '展示广告', value: 'display' },
                { label: '视频广告', value: 'video' },
                { label: '信息流广告', value: 'feed' },
              ]}
            />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="budgetType"
            label="预算类型"
            rules={[{ required: true, message: '请选择预算类型' }]}
          >
            <Select
              placeholder="请选择预算类型"
              options={[
                { label: '日预算', value: 'daily' },
                { label: '总预算', value: 'total' },
              ]}
            />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="budget"
            label="预算金额（元）"
            rules={[{ required: true, message: '请输入预算金额' }]}
          >
            <InputNumber
              min={1}
              max={1000000}
              precision={2}
              placeholder="请输入预算金额"
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="dateRange"
            label="投放时间"
            rules={[{ required: true, message: '请选择投放时间' }]}
          >
            <RangePicker
              showTime
              format="YYYY-MM-DD HH:mm"
              placeholder={['开始时间', '结束时间']}
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="objectives"
            label="营销目标"
            rules={[{ required: true, message: '请输入营销目标' }]}
          >
            <Select
              placeholder="请选择营销目标"
              options={[
                { label: '品牌曝光', value: 'brand' },
                { label: '点击转化', value: 'click' },
                { label: '应用下载', value: 'app_install' },
                { label: '商品购买', value: 'purchase' },
                { label: '表单提交', value: 'lead' },
              ]}
            />
          </Form.Item>
        </Col>
      </Row>
    </Card>
  )
}

export default CampaignForm
