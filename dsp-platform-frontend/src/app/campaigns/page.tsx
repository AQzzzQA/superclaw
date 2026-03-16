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
  DatePicker,
  InputNumber,
  message,
  Popconfirm,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '@/lib/api';
import { Campaign, PaginatedResponse } from '@/types';

const Campaigns = () => {
  const [loading, setLoading] = useState(false);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCampaign, setEditingCampaign] = useState<Campaign | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchCampaigns();
  }, [page]);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<Campaign>>(`/campaigns?page=${page}&limit=10`);
      setCampaigns(response.data.data.list);
      setTotal(response.data.data.total);
    } catch (error) {
      message.error('获取广告计划列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingCampaign(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Campaign) => {
    setEditingCampaign(record);
    form.setFieldsValue({
      ...record,
      start_date: dayjs(record.start_date),
      end_date: dayjs(record.end_date),
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/campaigns/${id}`);
      message.success('删除成功');
      fetchCampaigns();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleStart = async (id: number) => {
    try {
      await api.post(`/campaigns/${id}/start`);
      message.success('启动成功');
      fetchCampaigns();
    } catch (error) {
      message.error('启动失败');
    }
  };

  const handlePause = async (id: number) => {
    try {
      await api.post(`/campaigns/${id}/pause`);
      message.success('暂停成功');
      fetchCampaigns();
    } catch (error) {
      message.error('暂停失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const data = {
        ...values,
        start_date: values.start_date.format('YYYY-MM-DD'),
        end_date: values.end_date.format('YYYY-MM-DD'),
      };

      if (editingCampaign) {
        await api.put(`/campaigns/${editingCampaign.id}`, data);
        message.success('更新成功');
      } else {
        await api.post('/campaigns', data);
        message.success('创建成功');
      }

      setModalVisible(false);
      fetchCampaigns();
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
      title: '计划名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          display: { text: '展示', color: 'blue' },
          video: { text: '视频', color: 'green' },
          native: { text: '原生', color: 'purple' },
        };
        const { text, color } = typeMap[type] || { text: type, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '预算',
      dataIndex: 'budget',
      key: 'budget',
      render: (value: number) => `¥${value.toLocaleString()}`,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          active: { text: '投放中', color: 'green' },
          paused: { text: '已暂停', color: 'orange' },
          completed: { text: '已完成', color: 'blue' },
          pending: { text: '待投放', color: 'default' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '开始日期',
      dataIndex: 'start_date',
      key: 'start_date',
    },
    {
      title: '结束日期',
      dataIndex: 'end_date',
      key: 'end_date',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Campaign) => (
        <Space size="small">
          {record.status === 'paused' || record.status === 'pending' ? (
            <Button
              type="link"
              icon={<PlayCircleOutlined />}
              onClick={() => handleStart(record.id)}
            >
              启动
            </Button>
          ) : record.status === 'active' ? (
            <Button
              type="link"
              icon={<PauseCircleOutlined />}
              onClick={() => handlePause(record.id)}
            >
              暂停
            </Button>
          ) : null}
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确认删除"
            description="确定要删除这个广告计划吗？"
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
        title="广告计划管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新建计划
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={campaigns}
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
        title={editingCampaign ? '编辑广告计划' : '新建广告计划'}
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
            label="计划名称"
            rules={[{ required: true, message: '请输入计划名称' }]}
          >
            <Input placeholder="请输入计划名称" />
          </Form.Item>

          <Form.Item
            name="type"
            label="广告类型"
            rules={[{ required: true, message: '请选择广告类型' }]}
          >
            <Select placeholder="请选择广告类型">
              <Select.Option value="display">展示广告</Select.Option>
              <Select.Option value="video">视频广告</Select.Option>
              <Select.Option value="native">原生广告</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="start_date"
            label="开始日期"
            rules={[{ required: true, message: '请选择开始日期' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="end_date"
            label="结束日期"
            rules={[{ required: true, message: '请选择结束日期' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="budget"
            label="预算（元）"
            rules={[{ required: true, message: '请输入预算' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0}
              precision={2}
              placeholder="请输入预算"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Campaigns;
