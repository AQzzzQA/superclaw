'use client';

import { useEffect, useState } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Modal,
  Form,
  Input,
  Select,
  message,
  Popconfirm,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api from '@/lib/api';
import { Audience, PaginatedResponse } from '@/types';

const Audiences = () => {
  const [loading, setLoading] = useState(false);
  const [audiences, setAudiences] = useState<Audience[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingAudience, setEditingAudience] = useState<Audience | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchAudiences();
  }, [page]);

  const fetchAudiences = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<Audience>>(`/audiences?page=${page}&limit=10`);
      setAudiences(response.data.data.list);
      setTotal(response.data.data.total);
    } catch (error) {
      message.error('获取受众列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingAudience(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Audience) => {
    setEditingAudience(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/audiences/${id}`);
      message.success('删除成功');
      fetchAudiences();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const data = {
        ...values,
        targeting: {
          location: values.location || [],
          device: values.device || [],
          age_range: values.age_range || [],
          interests: values.interests || [],
        },
      };

      if (editingAudience) {
        await api.put(`/audiences/${editingAudience.id}`, data);
        message.success('更新成功');
      } else {
        await api.post('/audiences', data);
        message.success('创建成功，正在计算受众');
      }

      setModalVisible(false);
      fetchAudiences();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '受众名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '规模',
      dataIndex: 'size',
      key: 'size',
      render: (size: number) => (size ? size.toLocaleString() : '计算中...'),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          active: { text: '已完成', color: 'green' },
          calculating: { text: '计算中', color: 'orange' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Audience) => (
        <Space size="small">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确认删除"
            description="确定要删除这个受众吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确认"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="受众管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新建受众
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={audiences}
          rowKey="id"
          loading={loading}
          pagination={{
            current: page,
            pageSize: 10,
            total,
            onChange: (p) => setPage(p),
            showSizeChanger: false,
            showTotal: (t) => `共 ${t} 条`,
          }}
        />
      </Card>

      <Modal
        title={editingAudience ? '编辑受众' : '新建受众'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={600}
        okText="确认"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="受众名称"
            rules={[{ required: true, message: '请输入受众名称' }]}
          >
            <Input placeholder="请输入受众名称" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea
              rows={3}
              placeholder="请输入描述"
            />
          </Form.Item>

          <Form.Item
            name="location"
            label="地域定向"
          >
            <Select mode="tags" placeholder="请选择地域" />
          </Form.Item>

          <Form.Item
            name="device"
            label="设备定向"
          >
            <Select mode="tags" placeholder="请选择设备类型">
              <Select.Option value="mobile">移动设备</Select.Option>
              <Select.Option value="tablet">平板</Select.Option>
              <Select.Option value="desktop">桌面</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="age_range"
            label="年龄定向"
          >
            <Select mode="tags" placeholder="请选择年龄范围">
              <Select.Option value="18-24">18-24岁</Select.Option>
              <Select.Option value="25-34">25-34岁</Select.Option>
              <Select.Option value="35-44">35-44岁</Select.Option>
              <Select.Option value="45-54">45-54岁</Select.Option>
              <Select.Option value="55+">55岁以上</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="interests"
            label="兴趣定向"
          >
            <Select mode="tags" placeholder="请选择兴趣标签">
              <Select.Option value="technology">科技</Select.Option>
              <Select.Option value="finance">金融</Select.Option>
              <Select.Option value="shopping">购物</Select.Option>
              <Select.Option value="entertainment">娱乐</Select.Option>
              <Select.Option value="sports">体育</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Audiences;
