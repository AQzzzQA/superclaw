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
  Tooltip,
  Divider,
  Upload
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  ImportOutlined,
  ExportOutlined,
  UserOutlined,
  TeamOutlined,
  ShieldCheckOutlined,
  EyeOutlined
} from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';

const { Option } = Select;
const { TextArea } = Input;

interface User {
  id: string;
  qq_number: string;
  nickname: string;
  role: 'admin' | 'advanced' | 'normal' | 'readonly';
  permissions: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [importVisible, setImportVisible] = useState(false);

  // 角色颜色映射
  const roleColors = {
    admin: 'red',
    advanced: 'orange',
    normal: 'blue',
    readonly: 'green'
  };

  // 角色显示名称
  const roleNames = {
    admin: '超级管理员',
    advanced: '高级用户',
    normal: '普通用户',
    readonly: '只读用户'
  };

  // 初始化用户数据
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setUsers([
          {
            id: '1',
            qq_number: '1234567890',
            nickname: '超级管理员',
            role: 'admin',
            permissions: ['*'],
            is_active: true,
            created_at: '2026-03-01T00:00:00Z',
            updated_at: '2026-03-01T00:00:00Z'
          },
          {
            id: '2',
            qq_number: '0987654321',
            nickname: '高级用户',
            role: 'advanced',
            permissions: ['config:read', 'config:write', 'users:read'],
            is_active: true,
            created_at: '2026-03-02T00:00:00Z',
            updated_at: '2026-03-02T00:00:00Z'
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      message.error('获取用户列表失败');
      setLoading(false);
    }
  };

  const handleAddUser = () => {
    setEditingUser(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    form.setFieldsValue(user);
    setModalVisible(true);
  };

  const handleDeleteUser = (user: User) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除用户 "${user.nickname}" 吗？此操作不可撤销。`,
      onOk: () => {
        // 模拟删除操作
        setUsers(users.filter(u => u.id !== user.id));
        message.success('用户删除成功');
      }
    });
  };

  const handleImportUsers = (file: UploadFile) => {
    try {
      // 模拟导入操作
      const newUsers: User[] = [
        {
          id: '3',
          qq_number: '555666777',
          nickname: '新用户',
          role: 'normal',
          permissions: ['config:read', 'users:read'],
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ];
      setUsers([...users, ...newUsers]);
      message.success('导入成功');
      setImportVisible(false);
    } catch (error) {
      message.error('导入失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingUser) {
        // 更新用户
        const updatedUsers = users.map(user => 
          user.id === editingUser.id 
            ? { ...user, ...values, updated_at: new Date().toISOString() }
            : user
        );
        setUsers(updatedUsers);
        message.success('用户更新成功');
      } else {
        // 添加用户
        const newUser: User = {
          id: Date.now().toString(),
          ...values,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        setUsers([...users, newUser]);
        message.success('用户添加成功');
      }
      
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const columns = [
    {
      title: 'QQ号',
      dataIndex: 'qq_number',
      key: 'qq_number',
      render: (text: string) => <span style={{ fontFamily: 'monospace' }}>{text}</span>
    },
    {
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname',
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role: string) => (
        <Tag color={roleColors[role as keyof typeof roleColors]}>
          {roleNames[role as keyof typeof roleNames]}
        </Tag>
      )
    },
    {
      title: '权限数量',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: string[]) => permissions.length
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => (
        <Tag color={active ? 'green' : 'red'}>
          {active ? '激活' : '停用'}
        </Tag>
      )
    },
    {
      title: '操作',
      key: 'actions',
      render: (record: User) => (
        <Space>
          <Tooltip title="查看详情">
            <Button 
              type="text" 
              icon={<EyeOutlined />}
              onClick={() => handleEditUser(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button 
              type="text" 
              icon={<EditOutlined />}
              onClick={() => handleEditUser(record)}
            />
          </Tooltip>
          <Tooltip title="删除">
            <Button 
              type="text" 
              danger 
              icon={<DeleteOutlined />}
              onClick={() => handleDeleteUser(record)}
            />
          </Tooltip>
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2>用户管理</h2>
        <p style={{ color: '#666', marginTop: 8 }}>
          管理QQ用户的权限配置和角色分配
        </p>
      </div>

      <Card>
        <div style={{ marginBottom: 16 }}>
          <Space>
            <Button 
              type="primary" 
              icon={<PlusOutlined />}
              onClick={handleAddUser}
            >
              添加用户
            </Button>
            <Button 
              icon={<ImportOutlined />}
              onClick={() => setImportVisible(true)}
            >
              批量导入
            </Button>
            <Button 
              icon={<ExportOutlined />}
            >
              导出用户
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={users}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个用户`
          }}
          scroll={{ x: true }}
        />
      </Card>

      {/* 添加/编辑用户模态框 */}
      <Modal
        title={editingUser ? '编辑用户' : '添加用户'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="qq_number"
            label="QQ号"
            rules={[
              { required: true, message: '请输入QQ号' },
              { pattern: /^[1-9]\d{4,10}$/, message: 'QQ号格式不正确' }
            ]}
          >
            <Input placeholder="请输入QQ号" disabled={!!editingUser} />
          </Form.Item>

          <Form.Item
            name="nickname"
            label="昵称"
            rules={[{ required: true, message: '请输入昵称' }]}
          >
            <Input placeholder="请输入昵称" />
          </Form.Item>

          <Form.Item
            name="role"
            label="角色"
            rules={[{ required: true, message: '请选择角色' }]}
          >
            <Select placeholder="请选择角色">
              <Option value="admin">超级管理员</Option>
              <Option value="advanced">高级用户</Option>
              <Option value="normal">普通用户</Option>
              <Option value="readonly">只读用户</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="is_active"
            label="状态"
            valuePropName="checked"
          >
            <Switch checkedChildren="激活" unCheckedChildren="停用" defaultChecked />
          </Form.Item>
        </Form>
      </Modal>

      {/* 批量导入模态框 */}
      <Modal
        title="批量导入用户"
        open={importVisible}
        onCancel={() => setImportVisible(false)}
        footer={null}
      >
        <Upload.Dragger
          beforeUpload={() => false}
          onChange={(info) => {
            if (info.file.status === 'done') {
              handleImportUsers(info.file);
            }
          }}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持JSON格式的用户列表文件
          </p>
        </Upload.Dragger>
      </Modal>
    </div>
  );
};

export default UserManagement;