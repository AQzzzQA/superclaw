'use client';

import { useState } from 'react';
import { Card, Form, Input, Button, message, Divider } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/store/auth';
import api from '@/lib/api';

const Settings = () => {
  const [loading, setLoading] = useState(false);
  const [passwordForm] = Form.useForm();
  const { user, updateUser } = useAuthStore();

  const handleProfileUpdate = async (values: any) => {
    try {
      setLoading(true);
      await api.put('/user/profile', values);
      message.success('更新成功');
      updateUser(values);
    } catch (error) {
      message.error('更新失败');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (values: any) => {
    try {
      setLoading(true);
      await api.post('/user/change-password', values);
      message.success('密码修改成功');
      passwordForm.resetFields();
    } catch (error) {
      message.error('密码修改失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h1>设置</h1>

      <Card title="个人信息" style={{ marginBottom: 24 }}>
        <Form
          layout="vertical"
          initialValues={user || {}}
          onFinish={handleProfileUpdate}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="请输入用户名" />
          </Form.Item>

          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' },
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="请输入邮箱" />
          </Form.Item>

          <Form.Item
            name="phone"
            label="手机号"
            rules={[
              { required: true, message: '请输入手机号' },
              { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' },
            ]}
          >
            <Input prefix={<PhoneOutlined />} placeholder="请输入手机号" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              更新信息
            </Button>
          </Form.Item>
        </Form>
      </Card>

      <Card title="修改密码">
        <Form
          form={passwordForm}
          layout="vertical"
          onFinish={handlePasswordChange}
        >
          <Form.Item
            name="old_password"
            label="当前密码"
            rules={[{ required: true, message: '请输入当前密码' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请输入当前密码"
            />
          </Form.Item>

          <Form.Item
            name="new_password"
            label="新密码"
            rules={[
              { required: true, message: '请输入新密码' },
              { min: 6, message: '密码至少6位' },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请输入新密码"
            />
          </Form.Item>

          <Form.Item
            name="confirm_password"
            label="确认密码"
            dependencies={['new_password']}
            rules={[
              { required: true, message: '请确认新密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('new_password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请再次输入新密码"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              修改密码
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Settings;
