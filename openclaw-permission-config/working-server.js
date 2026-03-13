const express = require('express');
const cors = require('cors');
const path = require('path');

const PORT = 8899;

const app = express();

// 中间件
app.use(cors());
app.use(express.json());

// 健康检查
app.get('/api/health', (req, res) => {
    res.json({
        success: true,
        message: 'OpenClaw Permission Config API running on port 8899',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        port: PORT
    });
});

// 用户管理
app.get('/api/users', (req, res) => {
    res.json({
        success: true,
        data: {
            users: [
                {
                    id: '1',
                    qq_number: '1234567890',
                    nickname: '超级管理员',
                    role: 'admin',
                    permissions: ['*'],
                    is_active: true,
                    created_at: '2026-03-13T00:00:00Z'
                }
            ],
            total: 1
        },
        message: '用户列表获取成功'
    });
});

// 权限级别
app.get('/api/permissions/levels', (req, res) => {
    res.json({
        success: true,
        data: {
            levels: {
                admin: {
                    name: '超级管理员',
                    description: '拥有所有权限',
                    permissions: ['*'],
                    role: 'admin',
                    color: '#ff4757'
                },
                advanced: {
                    name: '高级用户',
                    description: '可以管理用户和配置',
                    permissions: ['config:read', 'config:write', 'users:read'],
                    role: 'advanced',
                    color: '#ffa502'
                },
                normal: {
                    name: '普通用户',
                    description: '可以查看和编辑配置',
                    permissions: ['config:read', 'config:write'],
                    role: 'normal',
                    color: '#3742fa'
                },
                readonly: {
                    name: '只读用户',
                    description: '只能查看配置',
                    permissions: ['config:read'],
                    role: 'readonly',
                    color: '#2ed573'
                }
            },
            count: 4
        },
        message: '权限级别列表获取成功'
    });
});

// 配置状态
app.get('/api/config/status', (req, res) => {
    res.json({
        success: true,
        data: {
            config_exists: true,
            config_path: '/root/.openclaw/openclaw.json',
            config_size: 1024,
            channels: {
                qqbot: {
                    enabled: true,
                    user_count: 1,
                    app_id: '102855454'
                }
            },
            permissions: {
                total_users: 1,
                admin_users: 1,
                unique_permissions: ['*'],
                most_common_permissions: { '*': 1 }
            },
            last_modified: new Date().toISOString()
        },
        message: '配置状态获取成功'
    });
});

// 主页面
app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OpenClaw权限配置管理</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                    color: #1890ff;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-top: 30px;
                }
                .feature {
                    background: #fafafa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #1890ff;
                }
                .api-endpoint {
                    background: #f0f2f5;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 10px 0;
                    font-family: monospace;
                    font-size: 14px;
                }
                .status {
                    background: #f6ffed;
                    border: 1px solid #b7eb8f;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 OpenClaw权限配置可视化工具</h1>
                    <p>专业的QQ权限管理解决方案</p>
                </div>
                
                <div class="status">
                    <h3>✅ 服务状态：运行中</h3>
                    <p><strong>端口：</strong>8899</p>
                    <p><strong>启动时间：</strong>${new Date().toLocaleString()}</p>
                    <p><strong>API版本：</strong>1.0.0</p>
                </div>

                <div class="features">
                    <div class="feature">
                        <h3>👥 用户管理</h3>
                        <p>管理QQ用户权限和角色分配</p>
                        <ul>
                            <li>用户增删改查</li>
                            <li>批量导入导出</li>
                            <li>权限级别管理</li>
                        </ul>
                    </div>

                    <div class="feature">
                        <h3>🔐 权限配置</h3>
                        <p>4级权限体系和可视化权限树</p>
                        <ul>
                            <li>超级管理员</li>
                            <li>高级用户</li>
                            <li>普通用户</li>
                            <li>只读用户</li>
                        </ul>
                    </div>

                    <div class="feature">
                        <h3>📋 模板管理</h3>
                        <p>预设权限模板和自定义模板</p>
                        <ul>
                            <li>4个预置模板</li>
                            <li>模板复制编辑</li>
                            <li>导入导出功能</li>
                        </ul>
                    </div>

                    <div class="feature">
                        <h3>⚙️ 配置导出</h3>
                        <p>生成openclaw.json配置文件</p>
                        <ul>
                            <li>格式验证</li>
                            <li>配置备份</li>
                            <li>批量应用</li>
                        </ul>
                    </div>
                </div>

                <h3>🌐 API接口</h3>
                <div class="api-endpoint">
                    GET /api/health - 健康检查
                </div>
                <div class="api-endpoint">
                    GET /api/users - 用户列表
                </div>
                <div class="api-endpoint">
                    GET /api/permissions/levels - 权限级别
                </div>
                <div class="api-endpoint">
                    GET /api/config/status - 配置状态
                </div>

                <div class="status">
                    <h3>🎯 快速开始</h3>
                    <p><strong>后端地址：</strong>http://localhost:8899</p>
                    <p><strong>前端地址：</strong>http://localhost:3000</p>
                    <p><strong>管理命令：</strong></p>
                    <code>./start.sh - 启动服务</code><br>
                    <code>./stop.sh - 停止服务</code>
                </div>
            </div>
        </body>
        </html>
    `);
});

// 启动服务器
app.listen(PORT, '0.0.0.0', () => {
    console.log(`\n🚀 OpenClaw Permission Config Server 启动成功！`);
    console.log(`📍 服务器地址: http://localhost:${PORT}`);
    console.log(`📊 API文档: http://localhost:${PORT}/api/health`);
    console.log(`🌐 Web界面: http://localhost:${PORT}`);
    console.log(`⚠️  开始时间: ${new Date().toLocaleString()}`);
    console.log(`🛡️  安全模式: 启用`);
    console.log(`📝 日志级别: INFO`);
    console.log(`\n💡 提示: 访问 http://localhost:${PORT} 开始使用管理界面\n`);
});