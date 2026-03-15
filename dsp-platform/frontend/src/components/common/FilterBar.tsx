import { Form, Input, Select, DatePicker, Button, Space, Card } from 'antd'
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons'
import type { FormInstance } from 'antd/es/form'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

interface FilterItem {
  name: string
  label: string
  type: 'input' | 'select' | 'dateRange'
  placeholder?: string
  options?: { label: string; value: any }[]
}

interface FilterBarProps {
  items: FilterItem[]
  onSearch: (values: any) => void
  onReset?: () => void
  loading?: boolean
}

const FilterBar = ({ items, onSearch, onReset, loading }: FilterBarProps) => {
  const [form] = Form.useForm<FormInstance>()

  const handleSearch = () => {
    const values = form.getFieldsValue()
    const formattedValues = { ...values }

    // 格式化日期范围
    items.forEach((item) => {
      if (item.type === 'dateRange' && values[item.name]) {
        formattedValues[item.name] = [
          values[item.name][0]?.format('YYYY-MM-DD'),
          values[item.name][1]?.format('YYYY-MM-DD'),
        ]
      }
    })

    onSearch(formattedValues)
  }

  const handleReset = () => {
    form.resetFields()
    onReset?.()
  }

  return (
    <Card style={{ marginBottom: 16 }}>
      <Form form={form} layout="inline">
        {items.map((item) => (
          <Form.Item
            key={item.name}
            name={item.name}
            label={item.label}
            style={{ marginBottom: 16 }}
          >
            {item.type === 'input' && (
              <Input placeholder={item.placeholder} allowClear />
            )}
            {item.type === 'select' && (
              <Select
                placeholder={item.placeholder}
                options={item.options}
                allowClear
                style={{ width: 150 }}
              />
            )}
            {item.type === 'dateRange' && (
              <RangePicker style={{ width: 240 }} />
            )}
          </Form.Item>
        ))}
        <Form.Item style={{ marginBottom: 16 }}>
          <Space>
            <Button
              type="primary"
              icon={<SearchOutlined />}
              onClick={handleSearch}
              loading={loading}
            >
              查询
            </Button>
            <Button icon={<ReloadOutlined />} onClick={handleReset}>
              重置
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  )
}

export default FilterBar
