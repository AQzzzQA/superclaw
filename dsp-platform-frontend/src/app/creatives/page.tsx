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
  Upload,
  message,
  Image,
  Popconfirm,
  Select,
} from 'antd';
import { PlusOutlined, UploadOutlined, DeleteOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd';
import api from '@/lib/api';
import { Creative, PaginatedResponse } from '@/types';

const Creatives = () => {
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [creatives, setCreatives] = useState<Creative[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [modalVisible, setModalVisible] = useState(false);
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewUrl, setPreviewUrl] = useState('');
  const [form] = Form.useForm();

  useEffect(() => {
    fetchCreatives();
  }, [page]);

  const fetchCreatives = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<Creative>>(`/creatives?page=${page}&limit=10`);
      setCreatives(response.data.data.list);
      setTotal(response.data.data.total);
    } catch (error) {
      message.error('获取创意列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    form.resetFields();
    setFileList([]);
    setModalVisible(true);
  };

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const response = await api.post<{ file_url: string }>('/creatives/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const fileUrl = response.data.data.file_url;
      form.setFieldsValue({ file_url, type: 'image' });

      setFileList([
        {
          uid: '-1',
          name: file.name,
          status: 'done',
          url: fileUrl,
        },
      ]);

      message.success('上传成功');
      return false; // 阻止默认上传
    } catch (error) {
      message.error('上传失败');
      return false;
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/creatives/${id}`);
      message.success('删除成功');
      fetchCreatives();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await api.post('/creatives', values);
      message.success('创建成功');
      setModalVisible(false);
      fetchCreatives();
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
      title: '创意名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          image: { text: '图片', color: 'blue' },
          video: { text: '视频', color: 'green' },
          html: { text: 'HTML', color: 'purple' },
        };
        const { text, color } = typeMap[type] || { text: type, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '尺寸',
      key: 'size',
      render: (_: any, record: Creative) =>
        `${record.width} x ${record.height}`,
    },
    {
      title: '预览',
      dataIndex: 'file_url',
      key: 'file_url',
      render: (url: string) =>
        url ? (
          <Image
            width={60}
            height={60}
            src={url}
            preview={{
              mask: '点击预览',
            }}
          />
        ) : '-',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          active: { text: '启用', color: 'green' },
          paused: { text: '暂停', color: 'orange' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '审核状态',
      dataIndex: 'approval_status',
      key: 'approval_status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          approved: { text: '已通过', color: 'green' },
          pending: { text: '审核中', color: 'orange' },
          rejected: { text: '已拒绝', color: 'red' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Creative) => (
        <Popconfirm
          title="确认删除"
          description="确定要删除这个创意吗？"
          onConfirm={() => handleDelete(record.id)}
          okText="确认"
          cancelText="取消"
        >
          <Button type="link" danger icon={<DeleteOutlined />}>
            删除
          </Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="创意管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新建创意
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={creatives}
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
        title="新建创意"
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
            label="创意名称"
            rules={[{ required: true, message: '请输入创意名称' }]}
          >
            <Input placeholder="请输入创意名称" />
          </Form.Item>

          <Form.Item
            name="file_url"
            label="上传文件"
            rules={[{ required: true, message: '请上传文件' }]}
          >
            <Upload
              listType="picture-card"
              fileList={fileList}
              beforeUpload={handleUpload}
              maxCount={1}
            >
              {fileList.length >= 1 ? null : (
                <div>
                  <UploadOutlined />
                  <div style={{ marginTop: 8 }}>上传</div>
                </div>
              )}
            </Upload>
          </Form.Item>

          <Form.Item label="文件类型">
            <Input disabled value="图片" />
          </Form.Item>

          <Form.Item label="尺寸">
            <Input.Group compact>
              <Form.Item
                name="width"
                noStyle
                rules={[{ required: true, message: '请输入宽度' }]}
              >
                <InputNumber
                  style={{ width: '50%' }}
                  min={0}
                  placeholder="宽度"
                />
              </Form.Item>
              <span style={{ display: 'inline-block', width: 12, textAlign: 'center' }}>×</span>
              <Form.Item
                name="height"
                noStyle
                rules={[{ required: true, message: '请输入高度' }]}
              >
                <InputNumber
                  style={{ width: '50%' }}
                  min={0}
                  placeholder="高度"
                />
              </Form.Item>
            </Input.Group>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Creatives;
