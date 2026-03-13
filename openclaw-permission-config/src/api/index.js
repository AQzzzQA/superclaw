/**
 * API路由主入口
 * 包含所有权限配置相关的API路由
 */

const express = require('express');
const router = express.Router();

// 导入各个API路由模块
const indexRoutes = require('./index');
const userRoutes = require('./users');
const permissionRoutes = require('./permissions');
const configRoutes = require('./config');
const templateRoutes = require('./templates');

// API版本信息
router.get('/version', (req, res) => {
  res.json({
    success: true,
    data: {
      version: '1.0.0',
      name: 'OpenClaw Permission Config API',
      description: 'OpenClaw权限配置可视化工具API',
      build_date: '2026-03-13',
      api_version: 'v1'
    },
    message: 'API版本信息获取成功'
  });
});

// API根路由
router.use('/', indexRoutes);
router.use('/users', userRoutes);
router.use('/permissions', permissionRoutes);
router.use('/config', configRoutes);
router.use('/templates', templateRoutes);

// API统计信息
router.get('/stats', (req, res) => {
  res.json({
    success: true,
    data: {
      uptime: process.uptime(),
      memory_usage: {
        used: process.memoryUsage().heapUsed,
        total: process.memoryUsage().heapTotal,
        percentage: (process.memoryUsage().heapUsed / process.memoryUsage().heapTotal * 100).toFixed(2) + '%'
      },
      request_count: global.requestCount || 0,
      api_routes: {
        users: 7,
        permissions: 8,
        config: 9,
        templates: 11,
        total: 35
      }
    },
    message: 'API统计信息获取成功'
  });
});

module.exports = router;