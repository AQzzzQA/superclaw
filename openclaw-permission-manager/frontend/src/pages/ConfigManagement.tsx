import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  Space, 
  Tag, 
  message,
  Popconfirm,
  Typography,
  Row,
  Col,
  Statistic,
  Descriptions,
  Tabs,
  Alert,
  JSONView
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SettingOutlined,
  DownloadOutlined,
  EyeOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import { configService } from '../services/configService';
import { userService } from '../services/userService';

const { Title } = Typography;
const { TextArea } = Input;
const { TabPane } = Tabs;

const ConfigManagement: React.FC = () => {
  const [configs, setConfigs] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [previewConfig, setPreviewConfig] = useState<any>(null);
  const [generateConfigModal, setGenerateConfigModal] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState<string>('');
  const [generatedConfig, setGeneratedConfig] = useState<any>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadConfigs();
    loadUsers();
  }, []);

  const loadConfigs = async () => {
    setLoading(true);
    try {
      const response = await configService.getAllConfigs();
      setConfigs(response.data);
    } catch (error) {
      message.error('加载配置失败');
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await userService.getAllUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to load users:', error);
    }
  };

  const handleAdd = () => {
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (config: any) => {
    form.setFieldsValue({
      config_name: config.config_name,
      config_data: JSON.stringify(config.config_data, null, 2),
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await configService.deleteConfig(id);
      message.success('删除成功');
      loadConfigs();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handlePreview = (config: any) => {
    setPreviewConfig(config);
  };

  const handleDownload = (config: any) => {
    const dataStr = JSON.stringify(config.config_data, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${config.config_name}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const handleGenerateConfig = async () => {
    if (!selectedUserId) {
      message.error('请选择用户');
      return;
    }

    try {
      const response = await configService.generateOpenClawConfig(selectedUserId);
      setGeneratedConfig(response.data);
      setGenerateConfigModal(true);
    } catch (error) {
      message.error('生成配置失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      const configData = JSON.parse(values.config_data);
      if (editingConfig) {
        await configService.updateConfig(editingConfig.id, {
          config_name: values.config_name,
          config_data: configData,
        });
        message.success('更新成功');
      } else {
        await configService.createConfig({
          config_name: values.config_name,
          config_data: configData,
        });
        message.success('创建成功');
      }
      setModalVisible(false);
      loadConfigs();
    } catch (error) {
      message.error(editingConfig ? '更新失败' : '创建失败');
    }
  };

  const handleCopyConfig = () => {
    if (generatedConfig) {
      navigator.clipboard.writeText(JSON.stringify(generatedConfig, null, 2));
      message.success('配置已复制到剪贴板');
    }
  };

  let editingConfig: any = null;

  const columns = [
    {
      title: '配置名称',
      dataIndex: 'config_name',
      key: 'config_name',
    },
    {
      title: '版本',
      dataIndex: 'version',
      key: 'version',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: '创建者',
      dataIndex: 'created_by',
      key: 'created_by',
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
          <Button 
            type="link" 
            icon={<DownloadOutlined />} 
            onClick={() => handleDownload(record)}
          >
            下载
          </Button>
          <Button 
            type="link" 
            icon={<EditOutlined />} 
            onClick={() => {
              editingConfig = record;
              handleEdit(record);
            }}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定删除这个配置吗？"
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
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>配置管理</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="配置总数"
              value={configs.length}
              prefix={<SettingOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="用户数量"
              value={users.length}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card>
            <Space>
              <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={handleAdd}
              >
                添加配置
              </Button>
              <Button 
                type="default" 
                icon={<DownloadOutlined />}
                onClick={handleGenerateConfig}
              >
                生成用户配置
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>

      <Card title="配置列表">
        <Table
          columns={columns}
          dataSource={configs}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="编辑配置"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="config_name"
            label="配置名称"
            rules={[{ required: true, message: '请输入配置名称' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="config_data"
            label="配置数据"
            rules={[{ required: true, message: '请输入配置数据' }]}
          >
            <TextArea 
              rows={10} 
              placeholder="请输入JSON格式的配置数据"
            />
          </Form.Item>
          
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingConfig ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="配置预览"
        open={!!previewConfig}
        onCancel={() => setPreviewConfig(null)}
        footer={null}
        width={800}
      >
        {previewConfig && (
          <div>
            <Descriptions column={1} bordered style={{ marginBottom: 16 }}>
              <Descriptions.Item label="配置名称">
                {previewConfig.config_name}
              </Descriptions.Item>
              <Descriptions.Item label="版本">
                {previewConfig.version}
              </Descriptions.Item>
              <Descriptions.Item label="创建时间">
                {new Date(previewConfig.created_at).toLocaleString()}
              </Descriptions.Item>
              {previewConfig.created_by && (
                <Descriptions.Item label="创建者">
                  {previewConfig.created_by}
                </Descriptions.Item>
              )}
            </Descriptions>
            
            <Tabs defaultActiveKey="1">
              <TabPane tab="JSON格式" key="1">
                <pre style={{ 
                  backgroundColor: '#f5f5f5', 
                  padding: 16, 
                  borderRadius: 4,
                  maxHeight: 400,
                  overflow: 'auto'
                }}>
                  {JSON.stringify(previewConfig.config_data, null, 2)}
                </pre>
              </TabPane>
              <TabPane tab="美化格式" key="2">
                <JSONView 
                  style={{ 
                    backgroundColor: '#f5f5f5', 
                    padding: 16, 
                    borderRadius: 4,
                    maxHeight: 400,
                    overflow: 'auto'
                  }} 
                  src={previewConfig.config_data} 
                />
              </TabPane>
            </Tabs>
          </div>
        )}
      </Modal>

      <Modal
        title="生成用户配置"
        open={generateConfigModal}
        onCancel={() => {
          setGenerateConfigModal(false);
          setGeneratedConfig(null);
          setSelectedUserId('');
        }}
        footer={null}
        width={800}
      >
        <Form layout="vertical">
          <Form.Item
            label="选择用户"
            rules={[{ required: true, message: '请选择用户' }]}
          >
            <Select
              placeholder="请选择用户"
              value={selectedUserId}
              onChange={setSelectedUserId}
              style={{ width: '100%' }}
            >
              {users.map(user => (
                <Select.Option key={user.id} value={user.id}>
                  {user.nickname} ({user.qq_number})
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Space>
              <Button 
                type="primary" 
                onClick={handleGenerateConfig}
                disabled={!selectedUserId}
              >
                生成配置
              </Button>
              <Button onClick={() => {
                setGenerateConfigModal(false);
                setGeneratedConfig(null);
                setSelectedUserId('');
              }}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>

        {generatedConfig && (
          <div>
            <Alert
              message="配置已生成"
              description="您可以复制配置或下载为JSON文件"
              type="success"
              style={{ marginBottom: 16 }}
            />
            
            <Tabs defaultActiveKey="1">
              <TabPane tab="配置预览" key="1">
                <pre style={{ 
                  backgroundColor: '#f5f5f5', 
                  padding: 16, 
                  borderRadius: 4,
                  maxHeight: 300,
                  overflow: 'auto'
                }}>
                  {JSON.stringify(generatedConfig, null, 2)}
                </pre>
              </TabPane>
              <TabPane tab="配置详情" key="2">
                <Descriptions column={1} bordered>
                  <Descriptions.Item label="版本">
                    {generatedConfig.version}
                  </Descriptions.Item>
                  <Descriptions.Item label="生成时间">
                    {new Date(generatedConfig.generated_at).toLocaleString()}
                  </Descriptions.Item>
                  <Descriptions.Item label="用户">
                    {generatedConfig.user.nickname} ({generatedConfig.user.qq_number})
                  </Descriptions.Item>
                  <Descriptions.Item label="角色">
                    <Tag color={generatedConfig.user.role === 'admin' ? 'red' : 'blue'}>
                      {generatedConfig.user.role}
                    </Tag>
                  </Descriptions.Item>
                </Descriptions>
              </TabPane>
            </Tabs>
            
            <div style={{ marginTop: 16 }}>
              <Space>
                <Button 
                  type="primary" 
                  icon={<DownloadOutlined />}
                  onClick={() => {
                    const dataStr = JSON.stringify(generatedConfig, null, 2);
                    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
                    const exportFileDefaultName = `openclaw-config-${generatedConfig.user.qq_number}.json`;
                    
                    const linkElement = document.createElement('a');
                    linkElement.setAttribute('href', dataUri);
                    linkElement.setAttribute('download', exportFileDefaultName);
                    linkElement.click();
                  }}
                >
                  下载配置
                </Button>
                <Button 
                  icon={<FileTextOutlined />}
                  onClick={handleCopyConfig}
                >
                  复制配置
                </Button>
              </Space>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ConfigManagement;