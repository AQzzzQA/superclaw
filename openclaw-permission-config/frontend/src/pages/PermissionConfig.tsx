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
  Tooltip
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SettingOutlined,
  SafetyOutlined,
  UserCheckOutlined,
  EyeOutlined,
  SaveOutlined
} from '@ant-design/icons';

const { Option } = Select;
const { TextArea } = Input;

interface PermissionLevel {
  id: string;
  name: string;
  description: string;
  permissions: string[];
  role: 'admin' | 'advanced' | 'normal' | 'readonly';
  is_system: boolean;
}

const PermissionConfig: React.FC = () => {
  const [permissionLevels, setPermissionLevels] = useState<PermissionLevel[]>([]);
  const [customPermissions, setCustomPermissions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingLevel, setEditingLevel] = useState<PermissionLevel | null>(null);

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
    },
    {
      title: '日志管理',
      key: 'logs',
      children: [
        { title: '查看日志', key: 'logs:read' },
        { title: '删除日志', key: 'logs:delete' },
        { title: '搜索日志', key: 'logs:search' },
      ]
    }
  ];

  // 初始化权限级别
  useEffect(() => {
    fetchPermissionLevels();
  }, []);

  const fetchPermissionLevels = () => {
    setLoading(true);
    // 模拟API调用
    setTimeout(() => {
      setPermissionLevels([
        {
          id: 'admin-full',
          name: '完整管理员',
          description: '拥有所有权限，包括配置管理、用户管理、系统控制等',
          permissions: ['*'],
          role: 'admin',
          is_system: true
        },
        {
          id: 'manager-limited',
          name: '有限管理员',
          description: '可以管理用户和配置，但不能修改核心系统设置',
          permissions: ['config:read', 'config:write', 'users:read', 'users:write', 'templates:read', 'templates:write'],
          role: 'advanced',
          is_system: true
        },
        {
          id: 'editor',
          name: '编辑者',
          description: '可以查看和编辑配置，但不能管理用户',
          permissions: ['config:read', 'config:write', 'templates:read'],
          role: 'normal',
          is_system: true
        },
        {
          id: 'viewer',
          name: '观察者',
          description: '只能查看配置和日志，不能进行修改',
          permissions: ['config:read', 'logs:read'],
          role: 'readonly',
          is_system: true
        }
      ]);
      setLoading(false);
    }, 1000);
  };

  const handleAddLevel = () => {
    setEditingLevel(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditLevel = (level: PermissionLevel) => {
    setEditingLevel(level);
    form.setFieldsValue({
      name: level.name,
      description: level.description,
      permissions: level.permissions,
      role: level.role
    });
    setModalVisible(true);
  };

  const handleDeleteLevel = (level: PermissionLevel) => {
    if (level.is_system) {
      message.error('不能删除系统权限级别');
      return;
    }
    
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除权限级别 "${level.name}" 吗？`,
      onOk: () => {
        setPermissionLevels(prev => prev.filter(l => l.id !== level.id));
        message.success('权限级别删除成功');
      }
    });
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingLevel) {
        // 更新权限级别
        const updatedLevels = permissionLevels.map(level =>
          level.id === editingLevel.id
            ? { ...level, ...values, permissions: values.permissions || [] }
            : level
        );
        setPermissionLevels(updatedLevels);
        message.success('权限级别更新成功');
      } else {
        // 添加新权限级别
        const newLevel: PermissionLevel = {
          id: `custom-${Date.now()}`,
          name: values.name,
          description: values.description,
          permissions: values.permissions || [],
          role: values.role,
          is_system: false
        };
        setPermissionLevels([...permissionLevels, newLevel]);
        message.success('权限级别添加成功');
      }
      
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const handleCustomPermissionChange = (checked: boolean, permission: string) => {
    if (checked) {
      setCustomPermissions(prev => [...prev, permission]);
    } else {
      setCustomPermissions(prev => prev.filter(p => p !== permission));
    }
  };

  const columns = [
    {
      title: '权限级别',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: PermissionLevel) => (
        <div>
          <strong>{name}</strong>
          {record.is_system && <Tag color="blue" size="small" style={{ marginLeft: 8 }}>系统</Tag>}
        </div>
      )
    },
    {
      title: '角色类型',
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
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '权限数量',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: string[]) => permissions.length
    },
    {
      title: '操作',
      key: 'actions',
      render: (record: PermissionLevel) => (
        <Space>
          <Tooltip title="查看详情">
            <Button 
              type="text" 
              icon={<EyeOutlined />}
              onClick={() => handleEditLevel(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button 
              type="text" 
              icon={<EditOutlined />}
              onClick={() => handleEditLevel(record)}
            />
          </Tooltip>
          {!record.is_system && (
            <Tooltip title="删除">
              <Button 
                type="text" 
                danger 
                icon={<DeleteOutlined />}
                onClick={() => handleDeleteLevel(record)}
              />
            </Tooltip>
          )}
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2>权限配置</h2>
        <p style={{ color: '#666', marginTop: 8 }}>
          管理不同级别的权限配置和用户角色分配
        </p>
      </div>

      {/* 权限说明 */}
      <Alert
        message="权限配置说明"
        description="系统支持4种基本权限级别：超级管理员、高级用户、普通用户、只读用户。系统级别的权限配置不能修改，只能添加自定义权限级别。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <div style={{ display: 'flex', gap: 24 }}>
        {/* 权限级别列表 */}
        <div style={{ flex: 1 }}>
          <Card 
            title="权限级别管理" 
            extra={
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={handleAddLevel}
              >
                添加权限级别
              </Button>
            }
          >
            <Table
              columns={columns}
              dataSource={permissionLevels}
              rowKey="id"
              loading={loading}
              pagination={{
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 个权限级别`
              }}
            />
          </Card>
        </div>

        {/* 权限树 */}
        <div style={{ flex: 1 }}>
          <Card title="权限树">
            <Tree
              checkable
              multiple
              treeData={permissionTree}
              height={400}
              onCheck={(checkedKeys) => {
                setCustomPermissions(checkedKeys as string[]);
              }}
            />
            <div style={{ marginTop: 16 }}>
              <p>选中的权限:</p>
              <div>
                {customPermissions.map(permission => (
                  <Tag key={permission} color="processing">
                    {permission}
                  </Tag>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* 添加/编辑权限级别模态框 */}
      <Modal
        title={editingLevel ? '编辑权限级别' : '添加权限级别'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="权限级别名称"
            rules={[{ required: true, message: '请输入权限级别名称' }]}
          >
            <Input placeholder="请输入权限级别名称" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea 
              placeholder="请输入权限级别描述" 
              rows={3}
            />
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
    </div>
  );
};

export default PermissionConfig;