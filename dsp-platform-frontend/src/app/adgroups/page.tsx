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
  InputNumber,
  message,
  Popconfirm,
  Select,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api from '@/lib/api';
import { AdGroup, Campaign, PaginatedResponse } from '@/types';

const AdGroups = () => {
  const [loading, setLoading] = useState(false);
  const [adgroups, setAdgroups] = useState<AdGroup[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingAdGroup, setEditingAdGroup] = useState<AdGroup | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchAdGroups();
    fetchCampaigns();
  }, [page]);

  const fetchAdGroups = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<AdGroup>>(`/adgroups?page=${page}&limit=10`);
      setAdgroups(response.data.data.list);
      setTotal(response.data.data.total);
    } catch (error) {
      message.error('获取广告组列表失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchCampaigns = async () => {
    try {
      const response = await api.get<{ list: Campaign[] }>('/campaigns?limit=100');
      setCampaigns(response.data.data.list || []);
    } catch (error) {
      console.error('获取广告计划失败');
    }
  };

  const handleAdd = () => {
    setEditingAdGroup(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: AdGroup) => {
    setEditingAdGroup(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/adgroups/${id}`);
      message.success('删除成功');
      fetchAdGroups();
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
          gender: values.gender || [],
        },
      };

      if (editingAdGroup) {
        await api.put(`/adgroups/${editingAdGroup.id}`, data);
        message.success('更新成功');
      } else {
        await api.post('/adgroups', data);
        message.success('创建成功');
      }

      setModalVisible(false);
      fetchAdGroups();
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
      title: '广告组名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '所属计划',
      dataIndex: 'campaign',
      key: 'campaign',
      render: (campaign: Campaign) => campaign?.name || '-',
    },
    {
      title: '出价（元）',
      dataIndex: 'bid_amount',
      key: 'bid_amount',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          active: { text: '投放中', color: 'green' },
          paused: { text: '已暂停', color: 'orange' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: AdGroup) => (
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
            description="确定要删除这个广告组吗？"
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
        title="广告组管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新建广告组
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={adgroups}
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
        title={editingAdGroup ? '编辑广告组' : '新建广告组'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={600}
        okText="确认"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="campaign_id"
            label="所属广告计划"
            rules={[{ required: true, message: '请选择广告计划' }]}
          >
            <Select
              placeholder="请选择广告计划"
              showSearch
              optionFilterProp="children"
            >
              {campaigns.map((c) => (
                <Select.Option key={c.id} value={c.id}>
                  {c.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="name"
            label="广告组名称"
            rules={[{ required: true, message: '请输入广告组名称' }]}
          >
            <Input placeholder="请输入广告组名称" />
          </Form.Item>

          <Form.Item
            name="bid_amount"
            label="出价（元）"
            rules={[{ required: true, message: '请输入出价' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0}
              precision={2}
              placeholder="请输入出价"
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
            name="gender"
            label="性别定向"
          >
            <Select mode="tags" placeholder="请选择性别">
              <Select.Option value="male">男性</Select.Option>
              <Select.Option value="female">女性</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default AdGroups;
