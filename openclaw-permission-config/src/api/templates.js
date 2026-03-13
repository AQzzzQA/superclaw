/**
 * 权限模板管理API路由
 * 处理权限模板的创建、管理和应用
 */

const express = require('express');
const router = express.Router();
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const Joi = require('joi');

// 模板数据存储路径
const templatesPath = path.join(__dirname, '../../config/templates.json');

// 预定义的权限模板
const defaultTemplates = [
  {
    id: 'admin-full',
    name: '完整管理员',
    description: '拥有所有权限，包括配置管理、用户管理、系统控制等',
    icon: 'crown',
    color: '#ff4757',
    category: 'administration',
    permissions: ['*'],
    role: 'admin',
    is_system: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 'manager-limited',
    name: '有限管理员',
    description: '可以管理用户和配置，但不能修改核心系统设置',
    icon: 'user-shield',
    color: '#ffa502',
    category: 'administration',
    permissions: [
      'config:read',
      'config:write',
      'users:read',
      'users:write',
      'templates:read',
      'templates:write',
      'logs:read'
    ],
    role: 'advanced',
    is_system: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 'editor',
    name: '编辑者',
    description: '可以查看和编辑配置，但不能管理用户',
    icon: 'edit',
    color: '#3742fa',
    category: 'content',
    permissions: [
      'config:read',
      'config:write',
      'templates:read',
      'templates:write'
    ],
    role: 'normal',
    is_system: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 'viewer',
    name: '观察者',
    description: '只能查看配置和日志，不能进行修改',
    icon: 'eye',
    color: '#2ed573',
    category: 'content',
    permissions: [
      'config:read',
      'logs:read'
    ],
    role: 'readonly',
    is_system: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
];

// 获取所有模板
router.get('/', (req, res) => {
  try {
    const templates = loadTemplates();
    res.json({
      success: true,
      data: {
        templates: templates,
        total: templates.length,
        categories: getTemplateCategories(templates),
        system_count: templates.filter(t => t.is_system).length,
        custom_count: templates.filter(t => !t.is_system).length
      },
      message: '模板列表获取成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取模板列表失败',
      error: error.message
    });
  }
});

// 获取单个模板详情
router.get('/:templateId', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    res.json({
      success: true,
      data: template,
      message: '模板详情获取成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取模板详情失败',
      error: error.message
    });
  }
});

// 创建模板
router.post('/', (req, res) => {
  try {
    const templateSchema = Joi.object({
      name: Joi.string().min(2).max(50).required(),
      description: Joi.string().max(200).required(),
      icon: Joi.string().default('template'),
      color: Joi.string().default('#007bff'),
      category: Joi.string().valid('administration', 'content', 'development', 'custom').required(),
      permissions: Joi.array().items(Joi.string()).min(1).required(),
      role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').required(),
      is_system: Joi.boolean().default(false)
    });
    
    const { error, value } = templateSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '模板数据格式错误',
        error: error.details[0].message
      });
    }
    
    // 检查模板名称是否重复
    const templates = loadTemplates();
    if (templates.some(t => t.name === value.name && !t.is_system)) {
      return res.status(409).json({
        success: false,
        message: '模板名称已存在'
      });
    }
    
    // 创建新模板
    const newTemplate = {
      id: uuidv4(),
      name: value.name,
      description: value.description,
      icon: value.icon,
      color: value.color,
      category: value.category,
      permissions: value.permissions,
      role: value.role,
      is_system: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    templates.push(newTemplate);
    saveTemplates(templates);
    
    res.json({
      success: true,
      data: newTemplate,
      message: '模板创建成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '创建模板失败',
      error: error.message
    });
  }
});

// 更新模板
router.put('/:templateId', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    // 不能修改系统模板
    if (template.is_system) {
      return res.status(403).json({
        success: false,
        message: '不能修改系统模板'
      });
    }
    
    const templateSchema = Joi.object({
      name: Joi.string().min(2).max(50).optional(),
      description: Joi.string().max(200).optional(),
      icon: Joi.string().optional(),
      color: Joi.string().optional(),
      category: Joi.string().valid('administration', 'content', 'development', 'custom').optional(),
      permissions: Joi.array().items(Joi.string()).min(1).optional(),
      role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').optional()
    });
    
    const { error, value } = templateSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '模板数据格式错误',
        error: error.details[0].message
      });
    }
    
    // 检查模板名称是否重复
    if (value.name && templates.some(t => t.name === value.name && t.id !== templateId)) {
      return res.status(409).json({
        success: false,
        message: '模板名称已存在'
      });
    }
    
    // 更新模板
    Object.assign(template, value, { updated_at: new Date().toISOString() });
    saveTemplates(templates);
    
    res.json({
      success: true,
      data: template,
      message: '模板更新成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '更新模板失败',
      error: error.message
    });
  }
});

// 删除模板
router.delete('/:templateId', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    // 不能删除系统模板
    if (template.is_system) {
      return res.status(403).json({
        success: false,
        message: '不能删除系统模板'
      });
    }
    
    // 删除模板
    const filteredTemplates = templates.filter(t => t.id !== templateId);
    saveTemplates(filteredTemplates);
    
    res.json({
      success: true,
      message: '模板删除成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '删除模板失败',
      error: error.message
    });
  }
});

// 复制模板
router.post('/:templateId/copy', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    // 创建副本
    const newTemplate = {
      ...template,
      id: uuidv4(),
      name: `${template.name} (副本)`,
      is_system: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    templates.push(newTemplate);
    saveTemplates(templates);
    
    res.json({
      success: true,
      data: newTemplate,
      message: '模板复制成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '复制模板失败',
      error: error.message
    });
  }
});

// 导出模板
router.post('/:templateId/export', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    const exportData = {
      template: {
        ...template,
        export_info: {
          exported_at: new Date().toISOString(),
          exported_by: 'permission-config-tool',
          version: '1.0.0'
        }
      }
    };
    
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', `attachment; filename=template-${templateId}-${Date.now()}.json`);
    res.json(exportData);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '导出模板失败',
      error: error.message
    });
  }
});

// 导入模板
router.post('/import', (req, res) => {
  try {
    const { template_data } = req.body;
    
    if (!template_data) {
      return res.status(400).json({
        success: false,
        message: '缺少模板数据'
      });
    }
    
    // 验证导入数据
    const templateSchema = Joi.object({
      name: Joi.string().min(2).max(50).required(),
      description: Joi.string().max(200).required(),
      icon: Joi.string().default('template'),
      color: Joi.string().default('#007bff'),
      category: Joi.string().valid('administration', 'content', 'development', 'custom').required(),
      permissions: Joi.array().items(Joi.string()).min(1).required(),
      role: Joi.string().valid('admin', 'advanced', 'normal', 'readonly').required()
    });
    
    const { error, value } = templateSchema.validate(template_data);
    if (error) {
      return res.status(400).json({
        success: false,
        message: '模板数据格式错误',
        error: error.details[0].message
      });
    }
    
    // 检查模板名称是否重复
    const templates = loadTemplates();
    if (templates.some(t => t.name === value.name && !t.is_system)) {
      return res.status(409).json({
        success: false,
        message: '模板名称已存在'
      });
    }
    
    // 创建新模板
    const newTemplate = {
      id: uuidv4(),
      ...value,
      is_system: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    templates.push(newTemplate);
    saveTemplates(templates);
    
    res.json({
      success: true,
      data: newTemplate,
      message: '模板导入成功'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '导入模板失败',
      error: error.message
    });
  }
});

// 应用模板到用户
router.post('/:templateId/apply', (req, res) => {
  try {
    const templateId = req.params.templateId;
    const { user_ids = [] } = req.body;
    
    const templates = loadTemplates();
    const template = templates.find(t => t.id === templateId);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        message: '模板不存在'
      });
    }
    
    // 这里可以调用用户API来应用模板
    // 由于是示例，我们返回模拟的应用结果
    const result = {
      template_id: templateId,
      template_name: template.name,
      applied_users: user_ids.length,
      permissions: template.permissions,
      role: template.role,
      success: true
    };
    
    res.json({
      success: true,
      data: result,
      message: `模板 ${template.name} 应用成功，已应用到 ${user_ids.length} 个用户`
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '应用模板失败',
      error: error.message
    });
  }
});

// 辅助函数：加载模板
function loadTemplates() {
  try {
    if (!fs.existsSync(templatesPath)) {
      saveTemplates(defaultTemplates);
    }
    return fs.readJsonSync(templatesPath);
  } catch (error) {
    return defaultTemplates;
  }
}

// 辅助函数：保存模板
function saveTemplates(templates) {
  fs.writeJsonSync(templatesPath, templates, { spaces: 2 });
}

// 辅助函数：获取模板分类
function getTemplateCategories(templates) {
  const categories = {};
  
  templates.forEach(template => {
    if (!categories[template.category]) {
      categories[template.category] = [];
    }
    categories[template.category].push(template);
  });
  
  return categories;
}

module.exports = router;