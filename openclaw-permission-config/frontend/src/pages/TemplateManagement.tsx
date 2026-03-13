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
  Tree,
  Switch,
  Divider,
  Alert,
  Tooltip,
  Badge,
  Drawer
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  CopyOutlined,
  UploadOutlined,
  DownloadOutlined,
  EyeOutlined,
  SafetyCertificateOutlined,
  UserSwitchOutlined,
  FileTextOutlined
} from '@ant-design/icons';

const { Option } = Select;
const { TextArea } = Input;

interface Template {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  category: 'administration' | 'content' | 'development' | 'custom';
  permissions: string[];
  role: 'admin' | 'advanced' | 'normal' | 'readonly';
  is_system: boolean;
  created_at: string;
  updated_at: string;
}

const TemplateManagement: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [viewVisible, setViewVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null);
  const [viewingTemplate, setViewingTemplate] = useState<Template | null>(null);

  // 权限树形结构
  const permissionTree = [
    {
      title: '配置管理',
      key: 'config',
      children: [
        { title: '读取配置', key: 'config:read' },
        { title: '写入配置', key: 'config:write' },
        { title: '删除配置', key: 'config:delete' },
        { title: '导出配置', key: 'config:export' },
        { title: '导入配置', key: 'config:import' },
      ]
    },
    {
      title: '用户管理',
      key: 'users',
      children: [
        { title: '查看用户', key: 'users:read' },
        { title: '创建用户', key: 'users:create' },
        { title: '编辑用户', key: 'users:write' },
        { title: '删除用户', key: 'users:delete' },
      ]
    },
    {
      title: '模板管理',
      key: 'templates',
      children: [
        { title: '查看模板', key: 'templates:read' },
        { title: '创建模板', key: 'templates:create' },
        { title: '编辑模板', key: 'templates:write' },
        { title: '删除模板', key: 'templates:delete' },
      ]
    },
    {
      title: '系统管理',
      key: 'system',
      children: [
        { title: '查看状态', key: 'system:read' },
        { title: '重启服务', key: 'system:restart' },
        { title: '查看日志', key: 'system:logs' },
        { title: '备份配置', key: 'system:backup' },
      ]
    }
  ];

  // 初始化模板数据
  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = () => {
    setLoading(true);
    // 模拟API调用
    setTimeout(() => {
      setTemplates([
        {
          id: 'admin-full',
          name: '完整管理员',
          description: '拥有所有权限，包括配置管理、用户管理、系统控制等',
          icon: 'crown',
          color: '#ff4757',
          category: 'administration',
          permissions: ['*'],
          role: 'admin',
          is_system: true,
          created_at: '2026-03-01T00:00:00Z',
          updated_at: '2026-03-01T00:00:00Z'
        },
        {
          id: 'manager-limited',
          name: '有限管理员',
          description: '可以管理用户和配置，但不能修改核心系统设置',
          icon: 'user-shield',
          color: '#ffa502',
          category: 'administration',
          permissions: ['config:read', 'config:write', 'users:read', 'users:write', 'templates:read', 'templates:write'],
          role: 'advanced',
          is_system: true,
          created_at: '2026-03-01T00:00:00Z',
          updated_at: '2026-03-01T00:00:00Z'
        },
        {
          id: 'editor',
          name: '编辑者',
          description: '可以查看和编辑配置，但不能管理用户',
          icon: 'edit',
          color: '#3742fa',
          category: 'content',
          permissions: ['config:read', 'config:write', 'templates:read'],
          role: 'normal',
          is_system: true,
          created_at: '2026-03-01T00:00:00Z',
          updated_at: '2026-03-01T00:00:00Z'
        },
        {
          id: 'viewer',
          name: '观察者',
          description: '只能查看配置和日志，不能进行修改',
          icon: 'eye',
          color: '#2ed573',
          category: 'content',
          permissions: ['config:read', 'logs:read'],
          role: 'readonly',
          is_system: true,
          created_at: '2026-03-01T00:00:00Z',
          updated_at: '2026-03-01T00:00:00Z'
        }
      ]);
      setLoading(false);
    }, 1000);
  };

  const handleAddTemplate = () => {
    setEditingTemplate(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditTemplate = (template: Template) => {
    setEditingTemplate(template);
    form.setFieldsValue({
      name: template.name,
      description: template.description,
      icon: template.icon,
      color: template.color,
      category: template.category,
      permissions: template.permissions,
      role: template.role
    });
    setModalVisible(true);
  };

  const handleDeleteTemplate = (template: Template) => {
    if (template.is_system) {
      message.error('不能删除系统模板');
      return;
    }
    
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除模板 "${template.name}" 吗？`,
      onOk: () => {
        setTemplates(prev => prev.filter(t => t.id !== template.id));
        message.success('模板删除成功');
      }
    });
  };

  const handleCopyTemplate = (template: Template) => {
    const newTemplate: Template = {
      ...template,
      id: `copy-${Date.now()}`,
      name: `${template.name} (副本)`,
      is_system: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    setTemplates([...templates, newTemplate]);
    message.success('模板复制成功');
  };

  const handleViewTemplate = (template: Template) => {
    setViewingTemplate(template);
    setViewVisible(true);
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingTemplate) {
        // 更新模板
        const updatedTemplates = templates.map(template =>
          template.id === editingTemplate.id
            ? { ...template, ...values, permissions: values.permissions || [] }
            : template
        );
        setTemplates(updatedTemplates);
        message.success('模板更新成功');
      } else {
        // 添加新模板
        const newTemplate: Template = {
          id: `custom-${Date.now()}`,
          ...values,
          is_system: false,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        setTemplates([...templates, newTemplate]);
        message.success('模板添加成功');
      }
      
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const columns = [
    {
      title: '模板名称',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: Template) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div 
            style={{ 
              width: 24, 
              height: 24, 
              borderRadius: 4, 
              background: record.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: 12
            }}
          >
            {record.icon}
          </div>
          <span>{name}</span>
          {record.is_system && <Tag color="blue">系统</Tag>}
        </div>
      )
    },
    {
      title: '类别',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => {
        const categoryNames = {
          administration: '管理',
          content: '内容',
          development: '开发',
          custom: '自定义'
        };
        return categoryNames[category as keyof typeof categoryNames];
      }
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role: string) => {
        const roleNames = {
          admin: '超级管理员',
          advanced: '高级用户',
          normal: '普通用户',
          readonly: '只读用户'
        };
        return roleNames[role as keyof typeof roleNames];
      }
    },
    {
      title: '权限数量',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: string[]) => permissions.length
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '操作',
      key: 'actions',
      render: (record: Template) => (
        <Space>
          <Tooltip title="查看详情">
            <Button 
              type="text" 
              icon={<EyeOutlined />}
              onClick={() => handleViewTemplate(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button 
              type="text" 
              icon={<EditOutlined />}
              onClick={() => handleEditTemplate(record)}
            />
          </Tooltip>
          {!record.is_system && (
            <>
              <Tooltip title="复制">
                <Button 
                  type="text" 
                  icon={<CopyOutlined />}
                  onClick={() => handleCopyTemplate(record)}
                />
              </Tooltip>
              <Tooltip title="删除">
                <Button 
                  type="text" 
                  danger 
                  icon={<DeleteOutlined />}
                  onClick={() => handleDeleteTemplate(record)}
                />
              </Tooltip>
            </>
          )}
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2>模板管理</h2>
        <p style={{ color: '#666', marginTop: 8 }}>
          创建和管理权限配置模板，快速应用到用户权限设置
        </p>
      </div>

      {/* 模板统计 */}
      <div style={{ marginBottom: 24 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Card>
              <Statistic
                title="模板总数"
                value={templates.length}
                prefix={<FileTextOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="系统模板"
                value={templates.filter(t => t.is_system).length}
                prefix={<SafetyCertificateOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="自定义模板"
                value={templates.filter(t => !t.is_system).length}
                prefix={<UserSwitchOutlined />}
                valueStyle={{ color: '#faad14' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="类别数量"
                value={4}
                prefix={<FolderOpenOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
        </Row>
      </div>

      <Card 
        title="权限模板列表" 
        extra={
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleAddTemplate}
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
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个模板`
          }}
        />
      </Card>

      {/* 添加/编辑模板模态框 */}
      <Modal
        title={editingTemplate ? '编辑模板' : '添加模板'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="模板名称"
            rules={[{ required: true, message: '请输入模板名称' }]}
          >
            <Input placeholder="请输入模板名称" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea 
              placeholder="请输入模板描述" 
              rows={3}
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="icon"
                label="图标"
                rules={[{ required: true, message: '请选择图标' }]}
              >
                <Select placeholder="请选择图标">
                  <Option value="crown">皇冠</Option>
                  <Option value="shield">盾牌</Option>
                  <Option value="user">用户</Option>
                  <Option value="edit">编辑</Option>
                  <Option value="eye">眼睛</Option>
                  <Option value="settings">设置</Option>
                  <Option value="template">模板</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="color"
                label="颜色"
                rules={[{ required: true, message: '请选择颜色' }]}
              >
                <Select placeholder="请选择颜色">
                  <Option value="#ff4757">红色</Option>
                  <Option value="#ffa502">橙色</Option>
                  <Option value="#3742fa">蓝色</Option>
                  <Option value="#2ed573">绿色</Option>
                  <Option value="#a55eea">紫色</Option>
                  <Option value="#26de81">青色</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="category"
            label="类别"
            rules={[{ required: true, message: '请选择类别' }]}
          >
            <Select placeholder="请选择类别">
              <Option value="administration">管理</Option>
              <Option value="content">内容</Option>
              <Option value="development">开发</Option>
              <Option value="custom">自定义</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="role"
            label="角色类型"
            rules={[{ required: true, message: '请选择角色类型' }]}
          >
            <Select placeholder="请选择角色类型">
              <Option value="admin">超级管理员</Option>
              <Option value="advanced">高级用户</Option>
              <Option value="normal">普通用户</Option>
              <Option value="readonly">只读用户</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="permissions"
            label="权限列表"
          >
            <Tree
              checkable
              multiple
              treeData={permissionTree}
              height={200}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 模板详情抽屉 */}
      <Drawer
        title="模板详情"
        width={600}
        open={viewVisible}
        onClose={() => setViewVisible(false)}
        extra={
          <Button 
            type="primary" 
            icon={<ApplyTemplateOutlined />}
            onClick={() => {
              message.success('模板应用成功');
              setViewVisible(false);
            }}
          >
            应用模板
          </Button>
        }
      >
        {viewingTemplate && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <h3>{viewingTemplate.name}</h3>
              <p style={{ color: '#666' }}>{viewingTemplate.description}</p>
            </div>

            <div style={{ marginBottom: 16 }}>
              <strong>类别：</strong>
              <Tag color="blue" style={{ marginLeft: 8 }}>
                {viewingTemplate.category}
              </Tag>
            </div>

            <div style={{ marginBottom: 16 }}>
              <strong>角色类型：</strong>
              <Tag color="orange" style={{ marginLeft: 8 }}>
                {viewingTemplate.role}
              </Tag>
            </div>

            <div style={{ marginBottom: 16 }}>
              <strong>权限列表：</strong>
              <div style={{ marginTop: 8 }}>
                {viewingTemplate.permissions.map(permission => (
                  <Tag key={permission} color="green" style={{ margin: 2 }}>
                    {permission}
                  </Tag>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: 16 }}>
              <strong>创建时间：</strong>
              <span>{new Date(viewingTemplate.created_at).toLocaleString()}</span>
            </div>

            <div style={{ marginBottom: 16 }}>
              <strong>更新时间：</strong>
              <span>{new Date(viewingTemplate.updated_at).toLocaleString()}</span>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
};

export default TemplateManagement;