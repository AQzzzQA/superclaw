'use client';

import { useState, useEffect } from 'react';
import {
  Card,
  DatePicker,
  Row,
  Col,
  Table,
  Statistic,
  Tabs,
} from 'antd';
import dayjs, { Dayjs } from 'dayjs';
import api from '@/lib/api';
import { CampaignReport, AdGroupReport, PaginatedResponse } from '@/types';

const { RangePicker } = DatePicker;

const Reports = () => {
  const [loading, setLoading] = useState(false);
  const [campaignReports, setCampaignReports] = useState<CampaignReport[]>([]);
  const [adgroupReports, setAdgroupReports] = useState<AdGroupReport[]>([]);
  const [dateRange, setDateRange] = useState<[Dayjs, Dayjs]>([
    dayjs().subtract(7, 'day'),
    dayjs(),
  ]);

  const fetchCampaignReports = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<CampaignReport>>(
        `/reports/campaign/daily?start_date=${dateRange[0].format('YYYY-MM-DD')}&end_date=${dateRange[1].format('YYYY-MM-DD')}`
      );
      setCampaignReports(response.data.data.list || []);
    } catch (error) {
      console.error('获取广告计划报表失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchAdGroupReports = async () => {
    try {
      setLoading(true);
      const response = await api.get<PaginatedResponse<AdGroupReport>>(
        `/reports/adgroup/daily?start_date=${dateRange[0].format('YYYY-MM-DD')}&end_date=${dateRange[1].format('YYYY-MM-DD')}`
      );
      setAdgroupReports(response.data.data.list || []);
    } catch (error) {
      console.error('获取广告组报表失败');
    } finally {
      setLoading(false);
    }
  };

  // 初始加载
  useEffect(() => {
    fetchCampaignReports();
    fetchAdGroupReports();
  }, []);

  const campaignColumns = [
    {
      title: '日期',
      dataIndex: 'report_date',
      key: 'report_date',
    },
    {
      title: '计划',
      dataIndex: 'campaign',
      key: 'campaign',
      render: (campaign: any) => campaign?.name || '-',
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
      title: 'CTR',
      dataIndex: 'ctr',
      key: 'ctr',
      render: (value: number) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: '花费',
      dataIndex: 'cost',
      key: 'cost',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
    {
      title: 'CPC',
      dataIndex: 'cpc',
      key: 'cpc',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
    {
      title: 'CPM',
      dataIndex: 'cpm',
      key: 'cpm',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
  ];

  const adgroupColumns = [
    {
      title: '日期',
      dataIndex: 'report_date',
      key: 'report_date',
    },
    {
      title: '广告组',
      dataIndex: 'adgroup',
      key: 'adgroup',
      render: (adgroup: any) => adgroup?.name || '-',
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
      title: 'CTR',
      dataIndex: 'ctr',
      key: 'ctr',
      render: (value: number) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: '花费',
      dataIndex: 'cost',
      key: 'cost',
      render: (value: number) => `¥${value.toFixed(2)}`,
    },
  ];

  // 汇总统计
  const totalImpressions = campaignReports.reduce((sum, r) => sum + r.impressions, 0);
  const totalClicks = campaignReports.reduce((sum, r) => sum + r.clicks, 0);
  const totalCost = campaignReports.reduce((sum, r) => sum + r.cost, 0);
  const avgCTR = totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0;
  const avgCPC = totalClicks > 0 ? totalCost / totalClicks : 0;

  return (
    <div style={{ padding: 24 }}>
      <Card title="报表系统">
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          {/* 日期选择 */}
          <Row gutter={16}>
            <Col span={8}>
              <RangePicker
                value={dateRange}
                onChange={(dates) => {
                  if (dates) {
                    setDateRange(dates);
                    fetchCampaignReports();
                    fetchAdGroupReports();
                  }
                }}
                style={{ width: '100%' }}
              />
            </Col>
          </Row>

          {/* 汇总统计 */}
          <Row gutter={16}>
            <Col span={6}>
              <Card>
                <Statistic
                  title="总曝光"
                  value={totalImpressions}
                  valueStyle={{ fontSize: 20 }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="总点击"
                  value={totalClicks}
                  valueStyle={{ fontSize: 20 }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="平均CTR"
                  value={avgCTR}
                  precision={2}
                  suffix="%"
                  valueStyle={{ fontSize: 20 }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="总花费"
                  value={totalCost}
                  precision={2}
                  prefix="¥"
                  valueStyle={{ fontSize: 20 }}
                />
              </Card>
            </Col>
          </Row>

          {/* 报表表格 */}
          <Tabs
            defaultActiveKey="campaign"
            items={[
              {
                key: 'campaign',
                label: '广告计划报表',
                children: (
                  <Table
                    columns={campaignColumns}
                    dataSource={campaignReports}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      pageSize: 20,
                      showSizeChanger: true,
                      showTotal: (t) => `共 ${t} 条`,
                    }}
                  />
                ),
              },
              {
                key: 'adgroup',
                label: '广告组报表',
                children: (
                  <Table
                    columns={adgroupColumns}
                    dataSource={adgroupReports}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      pageSize: 20,
                      showSizeChanger: true,
                      showTotal: (t) => `共 ${t} 条`,
                    }}
                  />
                ),
              },
            ]}
          />
        </Space>
      </Card>
    </div>
  );
};

export default Reports;
