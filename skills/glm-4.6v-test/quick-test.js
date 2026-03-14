#!/usr/bin/env node

/**
 * GLM-4.6V 快速测试
 */

const https = require('https');

const GLM_API_KEY = 'c2e9c086c6af40b6b27e568a95b4d097.YKcM2eGMTGdp8plZ';
const MODEL_ID = 'glm-4.6v';

console.log('\n🚀 GLM-4.6V 模型快速测试');
console.log('=' .repeat(50));

// 测试 1: 基础对话
async function test1() {
  console.log('\n测试 1: 基础对话');
  const response = await callAPI([{ role: 'user', content: '你好，请自我介绍' }], 500);
  console.log('✅ 成功');
  console.log('回复:', response.content.substring(0, 100));
}

// 测试 2: 简单数学
async function test2() {
  console.log('\n测试 2: 简单数学');
  const response = await callAPI([{ role: 'user', content: '2 + 2 等于几？' }], 100);
  console.log('✅ 成功');
  console.log('回复:', response.content);
}

// 测试 3: 简短代码
async function test3() {
  console.log('\n测试 3: 简短代码');
  const response = await callAPI([{ role: 'user', content: '用 Python 写一个 Hello World' }], 300);
  console.log('✅ 成功');
  console.log('回复:', response.content.substring(0, 100));
}

async function callAPI(messages, maxTokens) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: MODEL_ID,
      messages: messages,
      max_tokens: maxTokens,
      temperature: 0.7
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
      timeout: 10000
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
              content: json.choices[0].message.content || '',
              usage: json.usage
            });
          } else {
            reject(new Error('Invalid response'));
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

async function main() {
  try {
    await test1();
    await new Promise(r => setTimeout(r, 1000));
    await test2();
    await new Promise(r => setTimeout(r, 1000));
    await test3();

    console.log('\n📊 测试结果');
    console.log('=' .repeat(50));
    console.log('✅ 所有测试通过！');
    console.log('🎉 GLM-4.6V 模型工作正常！\n');
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    process.exit(1);
  }
}

main();
