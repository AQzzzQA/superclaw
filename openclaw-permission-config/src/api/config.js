/**
 * 配置管理API路由
 * 处理openclaw.json配置文件的生成、验证和管理
 */

const express = require('express');
const router = express.Router();
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const Joi = require('joi');

// 配置验证schema
const configSchema = Joi.object({
  channels: Joi.object({
    qqbot: Joi.object({
      enabled: Joi.boolean().default(true),
      appId: Joi.string().required(),
      clientSecret: Joi.string().required(),
      users: Joi.object().pattern(
        Joi.string().pattern(/^[1-9]\d{4,10}$/),
        Joi.object({
          nickname: Joi.string().max(50).required(),
          role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').required(),
          permissions: Joi.array().items(Joi.string()).optional(),
          is_active: Joi.boolean().default(true),
          created_at: Joi.string().isoDate().optional(),
          updated_at: Joi.string().isoDate().optional()
        })
      )
    }).optional()
  }).optional(),
  gateway: Joi.object({
    port: Joi.number().port().default(18789),
    mode: Joi.string().valid('local', 'remote').default('local'),
    bind: Joi.string().default('auto'),
    controlUi: Joi.object({
      allowedOrigins: Joi.array().items(Joi.string()).default(['http://127.0.0.1:18789', 'http://localhost:18789']),
      dangerouslyAllowHostHeaderOriginFallback: Joi.boolean().default(false),
      allowInsecureAuth: Joi.boolean().default(false),
      dangerouslyDisableDeviceAuth: Joi.boolean().default(false)
    }).optional()
  }).optional()
});

// 备份配置文件
router.post('/backup', (req, res) => {
  try {
    const backupPath = '/root/.openclaw/openclaw.json';
    const backupDir = path.join(__dirname, '../../config/backups');
    
    // 确保备份目录存在
    fs.ensureDirSync(backupDir);
    
    // 生成备份文件名
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFilename = `openclaw-config-${timestamp}.json`;
    const backupFilePath = path.join(backupDir, backupFilename);
    
    // 读取并复制配置文件
    const config = require(backupPath);
    fs.writeJsonSync(backupFilePath, config, { spaces: 2 });
    
    res.json({
      success: true,
      data: {
        backup_id: uuidv4(),
        filename: backupFilename,
        path: backupFilePath,
        timestamp: timestamp,
        size: fs.statSync(backupFilePath).size
      },
      message: '配置文件备份成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '配置文件备份失败',
      error: error.message
    });
  }
});

// 获取配置文件列表
router.get('/backups', (req, res) => {
  try {
    const backupDir = path.join(__dirname, '../../config/backups');
    const backups = fs.readdirSync(backupDir).filter(file => file.startsWith('openclaw-config-') && file.endsWith('.json'));
    
    const backupList = backups.map(file => {
      const filePath = path.join(backupDir, file);
      const stats = fs.statSync(filePath);
      return {
        filename: file,
        path: filePath,
        timestamp: stats.birthtime.toISOString(),
        size: stats.size
      };
    });
    
    res.json({
      success: true,
      data: {
        backups: backupList.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)),
        total: backupList.length
      },
      message: '备份列表获取成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取备份列表失败',
      error: error.message
    });
  }
});

// 恢复配置文件
router.post('/restore/:backupId', (req, res) => {
  try {
    const backupId = req.params.backupId;
    const backupDir = path.join(__dirname, '../../config/backups');
    const backupFiles = fs.readdirSync(backupDir);
    
    // 查找对应的备份文件
    const backupFile = backupFiles.find(file => file.includes(backupId));
    if (!backupFile) {
      return res.status(404).json({
        success: false,
        message: '备份文件不存在'
      });
    }
    
    const backupPath = path.join(backupDir, backupFile);
    const config = require(backupPath);
    
    // 验证配置文件
    const { error, value } = configSchema.validate(config);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '备份文件格式无效',
        error: error.details[0].message
      });
    }
    
    // 创建备份
    await router.post('/backup')(req, res);
    
    // 恢复配置
    const configPath = '/root/.openclaw/openclaw.json';
    fs.writeJsonSync(configPath, value, { spaces: 2 });
    
    res.json({
      success: true,
      data: {
        backup_id: backupId,
        restored_from: backupFile,
        restored_at: new Date().toISOString()
      },
      message: '配置文件恢复成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '配置文件恢复失败',
      error: error.message
    });
  }
});

// 生成配置文件
router.post('/generate', (req, res) => {
  try {
    const { template = 'default', users = [], customSettings = {} } = req.body;
    
    // 读取基础配置
    const baseConfigPath = '/root/.openclaw/openclaw.json';
    const baseConfig = require(baseConfigPath);
    
    // 创建新的配置
    const newConfig = {
      ...baseConfig,
      meta: {
        ...baseConfig.meta,
        generatedBy: 'permission-config-tool',
        generatedAt: new Date().toISOString(),
        template: template,
        version: '1.0.0'
      },
      channels: {
        ...baseConfig.channels,
        qqbot: {
          enabled: baseConfig.channels?.qqbot?.enabled ?? true,
          appId: baseConfig.channels?.qqbot?.appId || '102855454',
          clientSecret: baseConfig.channels?.qqbot?.clientSecret || 'your-secret-key',
          users: generateUsersConfig(users)
        }
      },
      custom: customSettings
    };
    
    // 验证配置
    const { error, value } = configSchema.validate(newConfig);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '配置文件格式无效',
        error: error.details[0].message
      });
    }
    
    // 返回生成的配置
    res.json({
      success: true,
      data: {
        config: value,
        summary: generateConfigSummary(value),
        validation: {
          valid: true,
          warnings: [],
          errors: []
        }
      },
      message: '配置文件生成成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '配置文件生成失败',
      error: error.message
    });
  }
});

// 应用配置文件
router.post('/apply', (req, res) => {
  try {
    const { config, validateOnly = false } = req.body;
    
    // 验证配置
    const { error, value } = configSchema.validate(config);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '配置文件格式无效',
        error: error.details[0].message
      });
    }
    
    // 预验证
    const validation = preValidateConfig(value);
    
    if (!validation.valid) {
      return res.status(400).json({
        success: false,
        message: '配置文件预验证失败',
        data: validation
      });
    }
    
    if (validateOnly) {
      return res.json({
        success: true,
        data: {
          config: value,
          validation: validation,
          changes: calculateChanges(value)
        },
        message: '配置文件验证成功'
      });
    }
    
    // 创建备份
    const backupResult = await router.post('/backup')(req, res);
    
    // 应用配置
    const configPath = '/root/.openclaw/openclaw.json';
    fs.writeJsonSync(configPath, value, { spaces: 2 });
    
    res.json({
      success: true,
      data: {
        config: value,
        validation: validation,
        changes: calculateChanges(value),
        backup_id: backupResult.data.backup_id,
        applied_at: new Date().toISOString()
      },
      message: '配置文件应用成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '配置文件应用失败',
      error: error.message
    });
  }
});

// 导出配置文件
router.post('/export', (req, res) => {
  try {
    const { format = 'json', includeComments = false } = req.body;
    
    const configPath = '/root/.openclaw/openclaw.json';
    const config = require(configPath);
    
    switch (format) {
      case 'json':
        const exportConfig = {
          ...config,
          export_info: {
            exported_at: new Date().toISOString(),
            exported_by: 'permission-config-tool',
            format: 'json'
          }
        };
        
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Content-Disposition', `attachment; filename=openclaw-config-${Date.now()}.json`);
        res.json(exportConfig);
        break;
        
      case 'yaml':
        const yaml = require('js-yaml');
        const yamlConfig = {
          ...config,
          export_info: {
            exported_at: new Date().toISOString(),
            exported_by: 'permission-config-tool',
            format: 'yaml'
          }
        };
        
        res.setHeader('Content-Type', 'application/x-yaml');
        res.setHeader('Content-Disposition', `attachment; filename=openclaw-config-${Date.now()}.yaml`);
        res.send(yaml.dump(yamlConfig));
        break;
        
      default:
        res.status(400).json({
          success: false,
          message: '不支持的导出格式'
        });
    }
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '配置文件导出失败',
      error: error.message
    });
  }
});

// 获取配置状态
router.get('/status', (req, res) => {
  try {
    const configPath = '/root/.openclaw/openclaw.json';
    const config = require(configPath);
    
    const status = {
      config_exists: true,
      config_path: configPath,
      config_size: JSON.stringify(config).length,
      channels: {
        qqbot: {
          enabled: config.channels?.qqbot?.enabled || false,
          user_count: config.channels?.qqbot?.users ? Object.keys(config.channels.qqbot.users).length : 0,
          app_id: config.channels?.qqbot?.appId || null
        }
      },
      permissions: analyzePermissions(config),
      last_modified: fs.statSync(configPath).mtime.toISOString()
    };
    
    res.json({
      success: true,
      data: status,
      message: '配置状态获取成功'
    });
  } catch (error) {
    res.json({
      success: true,
      data: {
        config_exists: false,
        error: error.message
      },
      message: '配置文件不存在或无法读取'
    });
  }
});

// 辅助函数：生成用户配置
function generateUsersConfig(users) {
  const userConfig = {};
  
  users.forEach(user => {
    userConfig[user.qq_number] = {
      nickname: user.nickname,
      role: user.role,
      permissions: user.permissions || getDefaultPermissions(user.role),
      is_active: user.is_active !== false,
      created_at: user.created_at || new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
  });
  
  return userConfig;
}

// 辅助函数：获取默认权限
function getDefaultPermissions(role) {
  const rolePermissions = {
    admin: ['*'],
    advanced: ['config:read', 'config:write', 'users:read', 'users:write', 'templates:read', 'templates:write'],
    normal: ['config:read', 'users:read', 'templates:read'],
    readonly: ['config:read']
  };
  return rolePermissions[role] || ['basic'];
}

// 辅助函数：生成配置摘要
function generateConfigSummary(config) {
  return {
    total_users: config.channels?.qqbot?.users ? Object.keys(config.channels.qqbot.users).length : 0,
    admin_users: config.channels?.qqbot?.users ? Object.values(config.channels.qqbot.users).filter(u => u.role === 'admin').length : 0,
    permission_templates: 4,
    custom_settings: !!config.custom
  };
}

// 辅助函数：预验证配置
function preValidateConfig(config) {
  const validation = {
    valid: true,
    warnings: [],
    errors: []
  };
  
  // 检查必需字段
  if (!config.channels?.qqbot?.appId) {
    validation.warnings.push('缺少 appId，将使用默认值');
  }
  
  if (!config.channels?.qqbot?.clientSecret) {
    validation.warnings.push('缺少 clientSecret，将使用默认值');
  }
  
  // 检查用户配置
  if (config.channels?.qqbot?.users) {
    Object.entries(config.channels.qqbot.users).forEach(([qqNumber, userData]) => {
      if (!userData.role) {
        validation.errors.push(`用户 ${qqNumber} 缺少角色配置`);
      }
      
      if (!userData.nickname) {
        validation.errors.push(`用户 ${qqNumber} 缺少昵称配置`);
      }
    });
  }
  
  // 检查超级管理员数量
  const adminUsers = Object.values(config.channels?.qqbot?.users || {}).filter(u => u.role === 'admin');
  if (adminUsers.length === 0) {
    validation.warnings.push('没有超级管理员用户');
  }
  
  if (adminUsers.length > 1) {
    validation.warnings.push(`发现 ${adminUsers.length} 个超级管理员，建议只有一个`);
  }
  
  validation.valid = validation.errors.length === 0;
  
  return validation;
}

// 辅助函数：计算变更
function calculateChanges(newConfig) {
  try {
    const configPath = '/root/.openclaw/openclaw.json';
    const oldConfig = require(configPath);
    
    const changes = {
      added_users: [],
      removed_users: [],
      modified_users: [],
      added_permissions: [],
      removed_permissions: []
    };
    
    const oldUsers = oldConfig.channels?.qqbot?.users || {};
    const newUsers = newConfig.channels?.qqbot?.users || {};
    
    // 计算用户变更
    Object.keys(newUsers).forEach(qqNumber => {
      if (!oldUsers[qqNumber]) {
        changes.added_users.push(qqNumber);
      } else if (JSON.stringify(oldUsers[qqNumber]) !== JSON.stringify(newUsers[qqNumber])) {
        changes.modified_users.push(qqNumber);
      }
    });
    
    Object.keys(oldUsers).forEach(qqNumber => {
      if (!newUsers[qqNumber]) {
        changes.removed_users.push(qqNumber);
      }
    });
    
    return changes;
  } catch (error) {
    return { error: '无法计算变更：' + error.message };
  }
}

// 辅助函数：分析权限
function analyzePermissions(config) {
  const analysis = {
    total_users: config.channels?.qqbot?.users ? Object.keys(config.channels.qqbot.users).length : 0,
    role_distribution: {
      admin: 0,
      advanced: 0,
      normal: 0,
      readonly: 0
    },
    unique_permissions: new Set(),
    most_common_permissions: {}
  };
  
  if (config.channels?.qqbot?.users) {
    Object.values(config.channels.qqbot.users).forEach(user => {
      analysis.role_distribution[user.role] = (analysis.role_distribution[user.role] || 0) + 1;
      
      if (user.permissions) {
        user.permissions.forEach(permission => {
          analysis.unique_permissions.add(permission);
          analysis.most_common_permissions[permission] = (analysis.most_common_permissions[permission] || 0) + 1;
        });
      }
    });
  }
  
  analysis.unique_permissions = Array.from(analysis.unique_permissions);
  
  return analysis;
}

module.exports = router;