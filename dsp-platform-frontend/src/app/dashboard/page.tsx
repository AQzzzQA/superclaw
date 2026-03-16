'use client';

import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table, message } from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import api from '@/lib/api';
import { DashboardData } from '@/types';
import { useAuthStore } from '@/store/auth';

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<DashboardData | null>(null);
  const { user } = useAuthStore();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await api.get<DashboardData>('/reports/dashboard');
      setData(response.data.data);
    } catch (error) {
      message.error('获取仪表盘数据失败');
    } finally {
      setLoading(false);
    }
  };

  const trendColumns = [
    {
      title: '日期',
      dataIndex: 'report_date',
      key: 'report_date',
    },
    {
      title: '曝光',
      dataIndex: 'impressions',
      key: 'impressions',
      render: (value: number) => value.toLocaleString(),
    },
    {
      title: '点击',
      dataIndex: 'clicks',
      key: 'clicks',
      render: (value: number) => value.toLocaleString(),
    },
    {
      title: '花费',
      dataIndex: 'cost',
      key: 'cost',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h1>仪表盘</h1>
      <p style={{ color: '#666', marginBottom: 24 }}>
        欢迎回来，{user?.username}！
      </p>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic
              title="今日曝光"
              value={data?.today.impressions || 0}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic
              title="今日点击"
              value={data?.today.clicks || 0}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic
              title="今日花费"
              value={data?.today.cost || 0}
              precision={2}
              prefix="¥"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic
              title="今日CTR"
              value={data?.today.ctr || 0}
              precision={4}
              suffix="%"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="30天趋势" style={{ marginBottom: 24 }}>
        <Table
          columns={trendColumns}
          dataSource={data?.trend || []}
          rowKey="report_date"
          pagination={{ pageSize: 10 }}
          loading={loading}
        />
      </Card>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="活跃广告计划" loading={loading}>
            <Statistic
              value={data?.active_campaigns || 0}
              suffix="个"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="昨日数据" loading={loading}>
            <Statistic
              title="曝光"
              value={data?.yesterday.impressions || 0}
              valueStyle={{ fontSize: 16 }}
            />
            <Statistic
              title="点击"
              value={data?.yesterday.clicks || 0}
              valueStyle={{ fontSize: 16 }}
            />
            <Statistic
              title="花费"
              value={data?.yesterday.cost || 0}
              precision={2}
              prefix="¥"
              valueStyle={{ fontSize: 16 }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
