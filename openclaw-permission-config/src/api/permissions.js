/**
 * 权限管理API路由
 * 处理权限级别和权限分配管理
 */

const express = require('express');
const router = express.Router();

// 权限级别定义
const permissionLevels = {
  admin: {
    name: '超级管理员',
    description: '拥有所有权限，可以管理整个系统',
    permissions: ['*'],
    color: '#ff4757',
    icon: 'crown'
  },
  advanced: {
    name: '高级用户',
    description: '可以管理用户和配置',
    permissions: [
      'config:read',
      'config:write',
      'users:read',
      'users:write',
      'templates:read',
      'templates:write',
      'logs:read',
      'system:read'
    ],
    color: '#ffa502',
    icon: 'user-shield'
  },
  normal: {
    name: '普通用户',
    description: '可以读取配置和用户信息',
    permissions: [
      'config:read',
      'users:read',
      'templates:read'
    ],
    color: '#3742fa',
    icon: 'user'
  },
  readonly: {
    name: '只读用户',
    description: '只能读取配置信息',
    permissions: [
      'config:read'
    ],
    color: '#2ed573',
    icon: 'eye'
  }
};

// 获取所有权限级别
router.get('/levels', (req, res) => {
  res.json({
    success: true,
    data: {
      levels: permissionLevels,
      count: Object.keys(permissionLevels).length
    },
    message: '权限级别列表获取成功'
  });
});

// 获取单个权限级别详情
router.get('/levels/:level', (req, res) => {
  const level = req.params.level;
  const permissionLevel = permissionLevels[level];
  
  if (!permissionLevel) {
    return res.status(404).json({
      success: false,
      message: '权限级别不存在'
    });
  }
  
  res.json({
    success: true,
    data: permissionLevel,
    message: '权限级别详情获取成功'
  });
});

// 获取所有可用权限
router.get('/list', (req, res) => {
  const allPermissions = new Set();
  
  // 收集所有权限级别中的权限
  Object.values(permissionLevels).forEach(level => {
    level.permissions.forEach(permission => {
      allPermissions.add(permission);
    });
  });
  
  // 添加自定义权限
  const customPermissions = [
    'config:export',
    'config:import',
    'logs:delete',
    'system:restart',
    'templates:create',
    'templates:delete'
  ];
  
  customPermissions.forEach(permission => {
    allPermissions.add(permission);
  });
  
  const permissionsArray = Array.from(allPermissions).sort();
  
  res.json({
    success: true,
    data: {
      permissions: permissionsArray,
      count: permissionsArray.length,
      groups: groupPermissions(permissionsArray)
    },
    message: '权限列表获取成功'
  });
});

// 检查权限分配的有效性
router.post('/validate', (req, res) => {
  try {
    const { permissions, role } = req.body;
    
    // 验证权限分配
    const validation = validatePermissionAssignment(permissions, role);
    
    res.json({
      success: true,
      data: validation,
      message: '权限验证完成'
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: '权限验证失败',
      error: error.message
    });
  }
});

// 获取权限分配建议
router.post('/suggest', (req, res) => {
  try {
    const { role, context = 'general' } = req.body;
    
    const suggestions = generatePermissionSuggestions(role, context);
    
    res.json({
      success: true,
      data: suggestions,
      message: '权限建议生成成功'
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: '权限建议生成失败',
      error: error.message
    });
  }
});

// 批量权限分配
router.post('/assign', (req, res) => {
  try {
    const { userId, role, customPermissions = [] } = req.body;
    
    // 验证请求
    if (!userId || !role) {
      return res.status(400).json({
        success: false,
        message: '用户ID和角色不能为空'
      });
    }
    
    // 检查角色是否存在
    if (!permissionLevels[role]) {
      return res.status(404).json({
        success: false,
        message: '指定的角色不存在'
      });
    }
    
    // 合并角色权限和自定义权限
    const basePermissions = permissionLevels[role].permissions;
    const finalPermissions = [...new Set([...basePermissions, ...customPermissions])];
    
    // 验证权限分配
    const validation = validatePermissionAssignment(finalPermissions, role);
    
    if (!validation.valid) {
      return res.status(400).json({
        success: false,
        message: '权限分配无效',
        data: validation
      });
    }
    
    res.json({
      success: true,
      data: {
        userId,
        role,
        permissions: finalPermissions,
        validation,
        changes: {
          added: customPermissions,
          removed: getRemovedPermissions(basePermissions, finalPermissions),
          total: finalPermissions.length
        }
      },
      message: '权限分配方案生成成功'
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '权限分配失败',
      error: error.message
    });
  }
});

// 辅助函数：权限分组
function groupPermissions(permissions) {
  const groups = {
    config: [],
    users: [],
    templates: [],
    logs: [],
    system: [],
    custom: []
  };
  
  permissions.forEach(permission => {
    if (permission.startsWith('config:')) {
      groups.config.push(permission);
    } else if (permission.startsWith('users:')) {
      groups.users.push(permission);
    } else if (permission.startsWith('templates:')) {
      groups.templates.push(permission);
    } else if (permission.startsWith('logs:')) {
      groups.logs.push(permission);
    } else if (permission.startsWith('system:')) {
      groups.system.push(permission);
    } else {
      groups.custom.push(permission);
    }
  });
  
  return groups;
}

// 辅助函数：验证权限分配
function validatePermissionAssignment(permissions, role) {
  const validation = {
    valid: true,
    warnings: [],
    errors: [],
    suggestions: []
  };
  
  // 检查权限格式
  permissions.forEach(permission => {
    if (!permission.match(/^[a-zA-Z_]+:[a-zA-Z_]+$/)) {
      validation.errors.push(`权限格式无效: ${permission}`);
      validation.valid = false;
    }
  });
  
  // 检查超级管理员权限
  if (role === 'admin' && !permissions.includes('*')) {
    validation.warnings.push('超级管理员应该拥有所有权限 ( *)');
  }
  
  // 检查权限冲突
  const conflicts = checkPermissionConflicts(permissions);
  if (conflicts.length > 0) {
    validation.warnings.push(...conflicts);
  }
  
  // 检查权限冗余
  const redundancies = checkPermissionRedundancies(permissions);
  if (redundancies.length > 0) {
    validation.suggestions.push(...redundancies);
  }
  
  return validation;
}

// 辅助函数：检查权限冲突
function checkPermissionConflicts(permissions) {
  const conflicts = [];
  
  // 检查读写冲突
  const writePermissions = permissions.filter(p => p.includes(':write'));
  const readPermissions = permissions.filter(p => p.includes(':read'));
  
  writePermissions.forEach(writePerm => {
    const basePerm = writePerm.replace(':write', '');
    const readConflicts = readPermissions.filter(p => p.startsWith(basePerm + ':') && p !== writePerm);
    
    if (readConflicts.length > 0) {
      conflicts.push(`同时存在读写权限可能造成混乱: ${writePerm} 和 ${readConflicts.join(', ')}`);
    }
  });
  
  return conflicts;
}

// 辅助函数：检查权限冗余
function checkPermissionRedundancies(permissions) {
  const redundancies = [];
  const seen = new Set();
  
  permissions.forEach(permission => {
    const basePerm = permission.split(':')[0];
    if (seen.has(basePerm)) {
      redundancies.push(`权限级别存在冗余: ${permission}`);
    }
    seen.add(basePerm);
  });
  
  return redundancies;
}

// 辅助函数：生成权限建议
function generatePermissionSuggestions(role, context) {
  const suggestions = {
    role: role,
    context: context,
    recommended: [],
    optional: [],
    avoid: [],
    explanation: ''
  };
  
  switch (role) {
    case 'admin':
      suggestions.recommended = ['*'];
      suggestions.optional = ['config:export', 'config:import'];
      suggestions.avoid = ['users:readonly'];
      suggestions.explanation = '超级管理员应该拥有所有系统权限';
      break;
      
    case 'advanced':
      suggestions.recommended = permissionLevels.advanced.permissions;
      suggestions.optional = ['config:export', 'templates:create'];
      suggestions.avoid = ['users:delete'];
      suggestions.explanation = '高级用户需要管理用户和配置的权限';
      break;
      
    case 'normal':
      suggestions.recommended = permissionLevels.normal.permissions;
      suggestions.optional = ['templates:read'];
      suggestions.avoid = ['config:write', 'users:write'];
      suggestions.explanation = '普通用户只需要基本的读取权限';
      break;
      
    case 'readonly':
      suggestions.recommended = permissionLevels.readonly.permissions;
      suggestions.optional = [];
      suggestions.avoid = ['config:write', 'users:write', 'templates:write'];
      suggestions.explanation = '只读用户只能查看配置信息';
      break;
  }
  
  // 根据上下文调整建议
  if (context === 'development') {
    suggestions.recommended.push('logs:read');
  } else if (context === 'production') {
    suggestions.avoid.push('logs:delete');
  }
  
  return suggestions;
}

// 辅助函数：获取移除的权限
function getRemovedPermissions(originalPermissions, newPermissions) {
  const originalSet = new Set(originalPermissions);
  const newSet = new Set(newPermissions);
  
  return Array.from(originalSet).filter(perm => !newSet.has(perm));
}

module.exports = router;