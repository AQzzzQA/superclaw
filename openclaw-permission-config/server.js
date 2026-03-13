/**
 * OpenClaw 权限配置可视化工具 - 后端服务
 * 专注于安全的QQ权限配置管理
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const path = require('path');
const fs = require('fs-extra');
const moment = require('moment');
const { v4: uuidv4 } = require('uuid');

// 中间件
const app = express();
app.use(helmet());
app.use(compression());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// 限流
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 每个IP最多100次请求
  message: {
    error: '请求过于频繁，请稍后再试'
  }
});
app.use('/api/', limiter);

// 请求体解析
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 日志中间件
app.use((req, res, next) => {
  const startTime = Date.now();
  
  // 记录请求开始
  console.log(`[${moment().format('YYYY-MM-DD HH:mm:ss')}] ${req.method} ${req.path} - IP: ${req.ip}`);
  
  // 监听响应完成
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    console.log(`[${moment().format('YYYY-MM-DD HH:mm:ss')}] ${req.method} ${req.path} - ${res.statusCode} - ${duration}ms`);
  });
  
  next();
});

// 静态文件服务
app.use('/static', express.static(path.join(__dirname, 'frontend/public')));

// 路由导入
const apiRoutes = require('./src/api');
app.use('/api', apiRoutes);

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('服务器错误:', err);
  
  // 记录错误日志
  const errorLog = {
    timestamp: moment().toISOString(),
    error: err.message,
    stack: err.stack,
    request: {
      method: req.method,
      path: req.path,
      ip: req.ip,
      userAgent: req.get('User-Agent')
    }
  };
  
  // 写入错误日志文件
  fs.appendFile(path.join(__dirname, 'logs', 'error.log'), 
    JSON.stringify(errorLog, null, 2) + '\n\n', 
    (writeErr) => {
      if (writeErr) console.error('无法写入错误日志:', writeErr);
    });
  
  res.status(500).json({
    success: false,
    message: '服务器内部错误',
    error: process.env.NODE_ENV === 'development' ? err.message : '请联系管理员'
  });
});

// 404处理
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: '请求的资源不存在'
  });
});

// 启动服务器
const PORT = process.env.PORT || 8899;
const HOST = process.env.HOST || '0.0.0.0';

// 确保日志目录存在
fs.ensureDirSync(path.join(__dirname, 'logs'));

app.listen(PORT, HOST, () => {
  console.log(`\n🚀 OpenClaw 权限配置服务器启动成功`);
  console.log(`📍 服务器地址: http://${HOST}:${PORT}`);
  console.log(`📊 API文档: http://${HOST}:${PORT}/api/health`);
  console.log(`⚠️  开始时间: ${moment().format('YYYY-MM-DD HH:mm:ss')}`);
  console.log(`🛡️  安全模式: 启用`);
  console.log(`📝 日志级别: INFO`);
  console.log(`\n💡 提示: 访问 http://${HOST}:${PORT} 开始使用管理界面\n`);
});

// 优雅关闭
process.on('SIGTERM', () => {
  console.log('🛑 接收到SIGTERM信号，正在关闭服务器...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 接收到SIGINT信号，正在关闭服务器...');
  process.exit(0);
});