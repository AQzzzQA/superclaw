#!/usr/bin/env node

/**
 * GLM-4.6V 集成测试
 *
 * 测试 GLM-4.6V 模型的配置和连接
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

console.log('🚀 GLM-4.6V 集成测试');
console.log('=' .repeat(50));

// 检查模型配置
console.log('\n检查模型配置...');

const modelsPath = '/root/.openclaw/agents/main/agent/models.json';

if (fs.existsSync(modelsPath)) {
  const models = JSON.parse(fs.readFileSync(modelsPath, 'utf8'));
  const glm4_6v = models.find(m => m.id === 'glm-4.6v');

  if (glm4_6v) {
    console.log('✅ GLM-4.6V 模型配置存在');
    console.log('   名称:', glm4_6v.name);
    console.log('   上下文窗口:', glm4_6v.contextWindow);
    console.log('   最大输出:', glm4_6v.maxTokens);
    console.log('   API 协议:', glm4_6v.api);
  } else {
    console.log('❌ GLM-4.6V 模型配置不存在');
    process.exit(1);
  }
} else {
  console.log('❌ 模型配置文件不存在');
  process.exit(1);
}

// 检查测试文件
console.log('\n检查测试文件...');

const testPath = '/root/.openclaw/workspace/skills/glm-4.6v-test';
const testFiles = [
  'test-glm-4.6v.js',
  'test-glm-4.6v-fixed.js',
  'simple-test.js',
  'quick-test.js',
  'README.md',
  'TEST-RESULTS.md'
];

testFiles.forEach(file => {
  const filePath = path.join(testPath, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} (缺失)`);
  }
});

// API 连接测试（简化版）
console.log('\n测试 API 连接...');

const GLM_API_KEY = 'c2e9c086c6af40b6b27e568a95b4d097.YKcM2eGMTGdp8plZ';
const MODEL_ID = 'glm-4.6v';

function testConnection() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: MODEL_ID,
      messages: [{ role: 'user', content: '你好' }],
      max_tokens: 50
    });

    const options = {
      hostname: 'open.bigmodel.cn',
      port: 443,
      path: '/api/paas/v4/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 15000
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);
          if (json.choices && json.choices[0]) {
            resolve({
              status: res.statusCode,
              model: json.model,
              content: json.choices[0].message.content?.substring(0, 50) || ''
            });
          } else {
            reject(new Error('Invalid response format'));
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });

    req.write(data);
    req.end();
  });
}

testConnection()
  .then(result => {
    console.log('✅ API 连接成功');
    console.log('   状态码:', result.status);
    console.log('   模型:', result.model);
    console.log('   回复:', result.content);

    console.log('\n📊 测试结果');
    console.log('=' .repeat(50));
    console.log('✅ 所有检查通过！');
    console.log('✅ GLM-4.6V 模型集成完成！');
    process.exit(0);
  })
  .catch(error => {
    console.log('❌ API 连接失败');
    console.log('   错误:', error.message);

    console.log('\n📊 测试结果');
    console.log('=' .repeat(50));
    console.log('⚠️ 部分检查通过，但 API 连接失败');
    console.log('建议: 检查网络连接和 API Key');
    process.exit(1);
  });
