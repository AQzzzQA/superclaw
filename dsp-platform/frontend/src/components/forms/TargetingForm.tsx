import { Form, InputNumber, Select, Collapse, Space, Tag } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import type { Targeting } from '../../types'

const { Panel } = Collapse

interface TargetingFormProps {
  form: any
  initialValues?: Partial<Targeting>
}

const TargetingForm = ({ form, initialValues }: TargetingFormProps) => {
  return (
    <Collapse defaultActiveKey={['age', 'location']}>
      <Panel header="年龄定向" key="age">
        <Space.Compact style={{ width: '100%' }}>
          <Form.Item
            name={['targeting', 'age', 'min']}
            label="最小年龄"
            style={{ flex: 1 }}
          >
            <InputNumber min={18} max={65} placeholder="18" style={{ width: '100%' }} />
          </Form.Item>
          <span style={{ display: 'flex', alignItems: 'center', padding: '0 8px' }}>至</span>
          <Form.Item
            name={['targeting', 'age', 'max']}
            label="最大年龄"
            style={{ flex: 1 }}
          >
            <InputNumber min={18} max={65} placeholder="65" style={{ width: '100%' }} />
          </Form.Item>
        </Space.Compact>
      </Panel>

      <Panel header="性别定向" key="gender">
        <Form.Item
          name={['targeting', 'gender']}
          label="性别"
        >
          <Select
            options={[
              { label: '全部', value: 'all' },
              { label: '男', value: 'male' },
              { label: '女', value: 'female' },
            ]}
          />
        </Form.Item>
      </Panel>

      <Panel header="地域定向" key="location">
        <Form.Item
          name={['targeting', 'location']}
          label="地区"
          tooltip="选择目标投放地区"
        >
          <Select
            mode="tags"
            placeholder="输入地区名称，按回车添加"
            options={[
              { label: '北京市', value: '北京市' },
              { label: '上海市', value: '上海市' },
              { label: '广州市', value: '广州市' },
              { label: '深圳市', value: '深圳市' },
              { label: '杭州市', value: '杭州市' },
            ]}
            tokenSeparators={[',']}
            tagRender={(props) => (
              <Tag {...props} closable={props.closable} onClose={props.onClose}>
                {props.label}
              </Tag>
            )}
          />
        </Form.Item>
      </Panel>

      <Panel header="兴趣定向" key="interests">
        <Form.Item
          name={['targeting', 'interests']}
          label="兴趣标签"
          tooltip="选择用户兴趣标签"
        >
          <Select
            mode="multiple"
            placeholder="选择兴趣标签"
            options={[
              { label: '科技', value: 'tech' },
              { label: '时尚', value: 'fashion' },
              { label: '美食', value: 'food' },
              { label: '旅行', value: 'travel' },
              { label: '运动', value: 'sports' },
              { label: '音乐', value: 'music' },
              { label: '游戏', value: 'gaming' },
              { label: '教育', value: 'education' },
            ]}
          />
        </Form.Item>
      </Panel>

      <Panel header="设备定向" key="device">
        <Form.Item
          name={['targeting', 'deviceType']}
          label="设备类型"
        >
          <Select
            mode="multiple"
            placeholder="选择设备类型"
            options={[
              { label: '手机', value: 'mobile' },
              { label: '平板', value: 'tablet' },
              { label: '电脑', value: 'desktop' },
            ]}
          />
        </Form.Item>

        <Form.Item
          name={['targeting', 'os']}
          label="操作系统"
        >
          <Select
            mode="multiple"
            placeholder="选择操作系统"
            options={[
              { label: 'iOS', value: 'ios' },
              { label: 'Android', value: 'android' },
              { label: 'Windows', value: 'windows' },
              { label: 'macOS', value: 'macos' },
            ]}
          />
        </Form.Item>
      </Panel>

      <Panel header="网络环境" key="network">
        <Form.Item
          name={['targeting', 'networkType']}
          label="网络类型"
        >
          <Select
            mode="multiple"
            placeholder="选择网络类型"
            options={[
              { label: 'WiFi', value: 'wifi' },
              { label: '4G', value: '4g' },
              { label: '5G', value: '5g' },
            ]}
          />
        </Form.Item>
      </Panel>

      <Panel header="自定义人群" key="custom">
        <Form.Item
          name={['targeting', 'customAudiences']}
          label="自定义人群包"
          tooltip="选择已创建的自定义人群包"
        >
          <Select
            mode="multiple"
            placeholder="选择人群包"
            options={[
              { label: '高价值用户', value: 'high-value' },
              { label: '活跃用户', value: 'active' },
              { label: '新用户', value: 'new-user' },
            ]}
          />
        </Form.Item>
      </Panel>
    </Collapse>
  )
}

export default TargetingForm
