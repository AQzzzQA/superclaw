/**
 * 用户管理API路由
 * 处理QQ用户权限配置和管理
 */

const express = require('express');
const router = express.Router();
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const Joi = require('joi');

// 验证schemas
const userSchema = Joi.object({
  qq_number: Joi.string().pattern(/^[1-9]\d{4,10}$/).required(),
  nickname: Joi.string().max(50).required(),
  role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').required(),
  permissions: Joi.array().items(Joi.string()).optional(),
  is_active: Joi.boolean().default(true)
});

const updateUserSchema = Joi.object({
  nickname: Joi.string().max(50).optional(),
  role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').optional(),
  permissions: Joi.array().items(Joi.string()).optional(),
  is_active: Joi.boolean().optional()
});

// 模拟用户数据库
let users = [
  {
    id: '1',
    qq_number: '1234567890',
    nickname: '超级管理员',
    role: 'admin',
    permissions: ['*'],
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
];

// 获取所有用户
router.get('/', (req, res) => {
  try {
    // 读取当前QQ用户列表
    const configPath = '/root/.openclaw/openclaw.json';
    const config = require(configPath);
    const qqUsers = config.channels?.qqbot?.users || {};
    
    // 合并模拟数据
    const allUsers = [...users, ...Object.entries(qqUsers).map(([qqId, userData]) => ({
      id: qqId,
      qq_number: qqId,
      nickname: userData.nickname || `用户_${qqId}`,
      role: userData.role || 'normal',
      permissions: userData.permissions || ['basic'],
      is_active: userData.is_active !== false,
      is_system: true,
      created_at: userData.created_at || new Date().toISOString(),
      updated_at: userData.updated_at || new Date().toISOString()
    }))];
    
    res.json({
      success: true,
      data: {
        users: allUsers,
        total: allUsers.length,
        count: allUsers.length
      },
      message: '用户列表获取成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取用户列表失败',
      error: error.message
    });
  }
});

// 获取单个用户信息
router.get('/:userId', (req, res) => {
  try {
    const userId = req.params.userId;
    const user = users.find(u => u.id === userId);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: '用户不存在'
      });
    }
    
    res.json({
      success: true,
      data: user,
      message: '用户信息获取成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取用户信息失败',
      error: error.message
    });
  }
});

// 创建用户
router.post('/', (req, res) => {
  try {
    // 验证请求数据
    const { error, value } = userSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '数据验证失败',
        error: error.details[0].message
      });
    }
    
    // 检查是否是超级管理员
    if (value.role === 'admin') {
      return res.status(403).json({
        success: false,
        message: '不能创建超级管理员用户，请联系系统管理员'
      });
    }
    
    // 检查QQ号是否已存在
    if (users.some(u => u.qq_number === value.qq_number)) {
      return res.status(409).json({
        success: false,
        message: '该QQ号已存在'
      });
    }
    
    // 创建新用户
    const newUser = {
      id: uuidv4(),
      qq_number: value.qq_number,
      nickname: value.nickname,
      role: value.role,
      permissions: value.permissions || getDefaultPermissions(value.role),
      is_active: value.is_active,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    users.push(newUser);
    
    // 同时更新openclaw配置
    updateOpenClawConfig(value.qq_number, value.role, value.permissions);
    
    res.json({
      success: true,
      data: newUser,
      message: '用户创建成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '创建用户失败',
      error: error.message
    });
  }
});

// 更新用户
router.put('/:userId', (req, res) => {
  try {
    const userId = req.params.userId;
    const user = users.find(u => u.id === userId);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: '用户不存在'
      });
    }
    
    // 验证请求数据
    const { error, value } = updateUserSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '数据验证失败',
        error: error.details[0].message
      });
    }
    
    // 检查是否要修改超级管理员
    if (user.role === 'admin' && value.role && value.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: '不能修改超级管理员角色'
      });
    }
    
    // 更新用户信息
    const updates = { ...value };
    if (updates.permissions && updates.permissions.length > 0) {
      updates.permissions = updates.permissions;
    } else {
      updates.permissions = getDefaultPermissions(updates.role || user.role);
    }
    
    Object.assign(user, updates, { updated_at: new Date().toISOString() });
    
    // 同时更新openclaw配置
    if (updates.role || updates.permissions) {
      updateOpenClawConfig(user.qq_number, updates.role || user.role, updates.permissions);
    }
    
    res.json({
      success: true,
      data: user,
      message: '用户更新成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '更新用户失败',
      error: error.message
    });
  }
});

// 删除用户
router.delete('/:userId', (req, res) => {
  try {
    const userId = req.params.userId;
    const user = users.find(u => u.id === userId);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: '用户不存在'
      });
    }
    
    // 不能删除超级管理员
    if (user.role === 'admin') {
      return res.status(403).json({
        success: false,
        message: '不能删除超级管理员用户'
      });
    }
    
    // 删除用户
    users = users.filter(u => u.id !== userId);
    
    // 同时从openclaw配置中移除
    removeUserFromOpenClawConfig(user.qq_number);
    
    res.json({
      success: true,
      message: '用户删除成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '删除用户失败',
      error: error.message
    });
  }
});

// 批量导入用户
router.post('/import', (req, res) => {
  try {
    const { users: importUsers } = req.body;
    
    if (!Array.isArray(importUsers)) {
      return res.status(400).json({
        success: false,
        message: '用户数据格式不正确'
      });
    }
    
    const results = {
      success: 0,
      failed: 0,
      errors: []
    };
    
    importUsers.forEach(userData => {
      try {
        const { error, value } = userSchema.validate(userData);
        if (error) {
          results.failed++;
          results.errors.push({
            qq_number: userData.qq_number,
            error: error.details[0].message
          });
          return;
        }
        
        // 检查是否已存在
        if (users.some(u => u.qq_number === value.qq_number)) {
          results.failed++;
          results.errors.push({
            qq_number: value.qq_number,
            error: '该QQ号已存在'
          });
          return;
        }
        
        // 创建用户
        const newUser = {
          id: uuidv4(),
          qq_number: value.qq_number,
          nickname: value.nickname,
          role: value.role,
          permissions: value.permissions || getDefaultPermissions(value.role),
          is_active: value.is_active,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        
        users.push(newUser);
        results.success++;
        
        // 更新配置
        updateOpenClawConfig(value.qq_number, value.role, value.permissions);
        
      } catch (error) {
        results.failed++;
        results.errors.push({
          qq_number: userData.qq_number,
          error: error.message
        });
      }
    });
    
    res.json({
      success: true,
      data: results,
      message: `批量导入完成：成功 ${results.success} 个，失败 ${results.failed} 个`
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '批量导入失败',
      error: error.message
    });
  }
});

// 辅助函数：获取默认权限
function getDefaultPermissions(role) {
  const rolePermissions = {
    admin: ['*'],
    advanced: ['config:read', 'users:read', 'users:write', 'templates:read', 'templates:write'],
    normal: ['config:read', 'users:read', 'templates:read'],
    readonly: ['config:read', 'users:read']
  };
  return rolePermissions[role] || ['basic'];
}

// 辅助函数：更新openclaw配置
function updateOpenClawConfig(qqNumber, role, permissions) {
  try {
    const configPath = '/root/.openclaw/openclaw.json';
    const config = require(configPath);
    
    // 初始化配置结构
    if (!config.channels) config.channels = {};
    if (!config.channels.qqbot) config.channels.qqbot = {};
    if (!config.channels.qqbot.users) config.channels.qqbot.users = {};
    
    // 更新用户配置
    config.channels.qqbot.users[qqNumber] = {
      nickname: `用户_${qqNumber}`,
      role: role,
      permissions: permissions || getDefaultPermissions(role),
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    // 保存配置
    fs.writeJsonSync(configPath, config, { spaces: 2 });
    
  } catch (error) {
    console.error('更新openclaw配置失败:', error);
  }
}

// 辅助函数：从openclaw配置中移除用户
function removeUserFromOpenClawConfig(qqNumber) {
  try {
    const configPath = '/root/.openclaw/openclaw.json';
    const config = require(configPath);
    
    if (config.channels?.qqbot?.users) {
      delete config.channels.qqbot.users[qqNumber];
      
      // 如果用户列表为空，清理配置
      if (Object.keys(config.channels.qqbot.users).length === 0) {
        delete config.channels.qqbot.users;
      }
      
      // 保存配置
      fs.writeJsonSync(configPath, config, { spaces: 2 });
    }
    
  } catch (error) {
    console.error('从openclaw配置中移除用户失败:', error);
  }
}

module.exports = router;