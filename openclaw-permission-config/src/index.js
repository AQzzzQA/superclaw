/**
 * OpenClaw 权限配置可视化工具 - 主要入口
 * 提供用户权限配置管理和配置文件生成功能
 */

const express = require('express');
const router = express.Router();

// 导入API路由
const userRoutes = require('./api/users');
const permissionRoutes = require('./api/permissions');
const configRoutes = require('./api/config');
const templateRoutes = require('./api/templates');

// 健康检查
router.get('/health', (req, res) => {
  res.json({
    success: true,
    message: 'OpenClaw Permission Config API运行正常',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    uptime: process.uptime()
  });
});

// API路由
router.use('/users', userRoutes);
router.use('/permissions', permissionRoutes);
router.use('/config', configRoutes);
router.use('/templates', templateRoutes);

// 获取系统状态
router.get('/system/status', (req, res) => {
  res.json({
    success: true,
    data: {
      status: 'running',
      current_user: 'root',
      is_admin: true,
      protection_enabled: true,
      features: {
        user_management: true,
        permission_templates: true,
        config_generation: true,
        backup_restore: true,
        audit_log: true
      },
      permissions: {
        super_admin: true,
        config_edit: true,
        user_management: true,
        template_management: true
      }
    },
    message: '系统状态正常'
  });
});

// 获取权限配置信息
router.get('/config/info', async (req, res) => {
  try {
    // 读取当前openclaw配置
    const configPath = '/root/.openclaw/openclaw.json';
    const config = await fs.readJson(configPath);
    
    res.json({
      success: true,
      data: {
        config_path: configPath,
        has_config: true,
        config_type: 'openclaw_json',
        user_count: config.channels?.qqbot ? Object.keys(config.channels.qqbot.users || {}).length : 0,
        templates_available: 4,
        protection_status: 'enabled'
      },
      message: '配置信息获取成功'
    });
  } catch (error) {
    res.json({
      success: false,
      data: {
        config_path: '/root/.openclaw/openclaw.json',
        has_config: false,
        error: error.message
      },
      message: '配置文件读取失败'
    });
  }
});

module.exports = router;