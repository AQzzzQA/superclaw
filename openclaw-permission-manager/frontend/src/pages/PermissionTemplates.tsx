import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  Select, 
  Space, 
  Tag, 
  message,
  Popconfirm,
  Typography,
  Row,
  Col,
  Statistic,
  Descriptions
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SettingOutlined,
  CopyOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { permissionService } from '../services/permissionService';

const { Title } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const PermissionTemplates: React.FC = () => {
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<any>(null);
  const [previewTemplate, setPreviewTemplate] = useState<any>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const response = await permissionService.getAllTemplates();
      setTemplates(response.data);
    } catch (error) {
      message.error('加载权限模板失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingTemplate(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (template: any) => {
    setEditingTemplate(template);
    form.setFieldsValue({
      name: template.name,
      description: template.description,
      permissions: template.permissions,
      is_system: template.is_system,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await permissionService.deleteTemplate(id);
      message.success('删除成功');
      loadTemplates();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handlePreview = (template: any) => {
    setPreviewTemplate(template);
  };

  const handleDuplicate = async (template: any) => {
    try {
      await permissionService.createTemplate({
        name: `${template.name} (副本)`,
        description: template.description,
        permissions: template.permissions,
        is_system: false,
      });
      message.success('复制成功');
      loadTemplates();
    } catch (error) {
      message.error('复制失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingTemplate) {
        await permissionService.updateTemplate(editingTemplate.id, values);
        message.success('更新成功');
      } else {
        await permissionService.createTemplate(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadTemplates();
    } catch (error) {
      message.error(editingTemplate ? '更新失败' : '创建失败');
    }
  };

  const columns = [
    {
      title: '模板名称',
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
      title: '权限',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: string[]) => (
        <Space>
          {permissions.map(permission => (
            <Tag key={permission} color="processing">{permission}</Tag>
          ))}
        </Space>
      ),
    },
    {
      title: '类型',
      dataIndex: 'is_system',
      key: 'is_system',
      render: (isSystem: boolean) => (
        <Tag color={isSystem ? 'orange' : 'blue'}>
          {isSystem ? '系统模板' : '自定义模板'}
        </Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: '操作',
      key: 'action',
      render: (record: any) => (
        <Space>
          <Button 
            type="link" 
            icon={<EyeOutlined />} 
            onClick={() => handlePreview(record)}
          >
            预览
          </Button>
          {!record.is_system && (
            <>
              <Button 
                type="link" 
                icon={<EditOutlined />} 
                onClick={() => handleEdit(record)}
              >
                编辑
              </Button>
              <Button 
                type="link" 
                icon={<CopyOutlined />} 
                onClick={() => handleDuplicate(record)}
              >
                复制
              </Button>
              <Popconfirm
                title="确定删除这个模板吗？"
                onConfirm={() => handleDelete(record.id)}
                okText="确定"
                cancelText="取消"
              >
                <Button 
                  type="link" 
                  danger 
                  icon={<DeleteOutlined />}
                >
                  删除
                </Button>
              </Popconfirm>
            </>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>权限模板管理</Title>
      
      <Card
        title="权限模板列表"
        extra={
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={handleAdd}
          >
            添加模板
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={templates}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingTemplate ? '编辑权限模板' : '添加权限模板'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="name"
            label="模板名称"
            rules={[{ required: true, message: '请输入模板名称' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="description"
            label="描述"
          >
            <TextArea rows={3} />
          </Form.Item>
          
          <Form.Item
            name="permissions"
            label="权限列表"
            rules={[{ required: true, message: '请选择权限' }]}
          >
            <Select mode="multiple" placeholder="选择权限">
              <Option value="read">读取</Option>
              <Option value="write">写入</Option>
              <Option value="delete">删除</Option>
              <Option value="manage_users">管理用户</Option>
              <Option value="manage_permissions">管理权限</Option>
              <Option value="system_config">系统配置</Option>
              <Option value="message_send">发送消息</Option>
              <Option value="message_view">查看消息</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="is_system" valuePropName="checked">
            <div>
              <strong>系统模板</strong>
              <div style={{ fontSize: '12px', color: '#666', marginTop: 4 }}>
                系统模板不能被编辑或删除
              </div>
            </div>
          </Form.Item>
          
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingTemplate ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="权限模板预览"
        open={!!previewTemplate}
        onCancel={() => setPreviewTemplate(null)}
        footer={null}
        width={600}
      >
        {previewTemplate && (
          <div>
            <Descriptions column={1} bordered>
              <Descriptions.Item label="模板名称">
                {previewTemplate.name}
              </Descriptions.Item>
              <Descriptions.Item label="描述">
                {previewTemplate.description || '无'}
              </Descriptions.Item>
              <Descriptions.Item label="类型">
                <Tag color={previewTemplate.is_system ? 'orange' : 'blue'}>
                  {previewTemplate.is_system ? '系统模板' : '自定义模板'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="权限列表">
                <Space wrap>
                  {previewTemplate.permissions.map((permission: string) => (
                    <Tag key={permission} color="processing">{permission}</Tag>
                  ))}
                </Space>
              </Descriptions.Item>
              <Descriptions.Item label="创建时间">
                {new Date(previewTemplate.created_at).toLocaleString()}
              </Descriptions.Item>
              {previewTemplate.created_by && (
                <Descriptions.Item label="创建者">
                  {previewTemplate.created_by}
                </Descriptions.Item>
              )}
            </Descriptions>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default PermissionTemplates;