import { Form, Input, Select, InputNumber, Card, Row, Col, Upload, message } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'
import type { CreativeFormData, AdGroup } from '../../types'

interface CreativeFormProps {
  form: any
  adGroups: AdGroup[]
  initialValues?: Partial<CreativeFormData>
  onUpload?: (file: File) => Promise<string>
}

const CreativeForm = ({ form, adGroups, initialValues, onUpload }: CreativeFormProps) => {
  const beforeUpload = (file: File) => {
    const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4'].includes(file.type)
    if (!isValidType) {
      message.error('只能上传 JPG/PNG/GIF 图片或 MP4 视频')
      return false
    }
    const isLt50M = file.size / 1024 / 1024 < 50
    if (!isLt50M) {
      message.error('文件大小不能超过 50MB')
      return false
    }
    return true
  }

  const handleUpload: UploadProps['customRequest'] = async ({ file, onSuccess, onError }) => {
    try {
      if (onUpload) {
        const url = await onUpload(file as File)
        onSuccess?.({ url })
        form.setFieldsValue({
          imageUrl: url,
        })
      }
    } catch (error) {
      onError?.(error as Error)
    }
  }

  return (
    <Card title="基本信息">
      <Row gutter={16}>
        <Col span={24}>
          <Form.Item
            name="name"
            label="创意名称"
            rules={[{ required: true, message: '请输入创意名称' }]}
          >
            <Input placeholder="请输入创意名称" maxLength={100} />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="adGroupId"
            label="所属广告组"
            rules={[{ required: true, message: '请选择所属广告组' }]}
          >
            <Select
              placeholder="请选择所属广告组"
              options={adGroups.map((group) => ({
                label: group.name,
                value: group.id,
              }))}
            />
          </Form.Item>
        </Col>

        <Col span={12}>
          <Form.Item
            name="type"
            label="创意类型"
            rules={[{ required: true, message: '请选择创意类型' }]}
          >
            <Select
              placeholder="请选择创意类型"
              options={[
                { label: '图片创意', value: 'image' },
                { label: '视频创意', value: 'video' },
                { label: '轮播创意', value: 'carousel' },
              ]}
            />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            label="创意素材"
            rules={[{ required: true, message: '请上传创意素材' }]}
          >
            <Upload
              listType="picture-card"
              maxCount={1}
              beforeUpload={beforeUpload}
              customRequest={handleUpload}
            >
              <div>
                <PlusOutlined />
                <div style={{ marginTop: 8 }}>上传</div>
              </div>
            </Upload>
          </Form.Item>

          <Form.Item
            name="imageUrl"
            hidden
          >
            <Input />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="title"
            label="创意标题"
            rules={[{ required: true, message: '请输入创意标题' }]}
          >
            <Input placeholder="请输入创意标题" maxLength={50} showCount />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="description"
            label="创意描述"
            rules={[{ required: true, message: '请输入创意描述' }]}
          >
            <Input.TextArea
              placeholder="请输入创意描述"
              maxLength={200}
              showCount
              rows={3}
            />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="callToAction"
            label="行动号召按钮"
            tooltip="选择合适的行动号召按钮文案"
          >
            <Select
              placeholder="请选择行动号召按钮"
              options={[
                { label: '了解更多', value: 'learn_more' },
                { label: '立即购买', value: 'buy_now' },
                { label: '立即下载', value: 'download' },
                { label: '立即报名', value: 'sign_up' },
                { label: '联系我们', value: 'contact_us' },
                { label: '查看详情', value: 'view_details' },
              ]}
            />
          </Form.Item>
        </Col>

        <Col span={24}>
          <Form.Item
            name="landingPageUrl"
            label="落地页链接"
            rules={[
              { required: true, message: '请输入落地页链接' },
              { type: 'url', message: '请输入有效的URL' },
            ]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>
        </Col>
      </Row>
    </Card>
  )
}

export default CreativeForm
