#!/usr/bin/env node

/**
 * GLM-4.6V 简单测试
 */

const https = require('https');

const GLM_API_KEY = 'c2e9c086c6af40b6b27e568a95b4d097.YKcM2eGMTGdp8plZ';
const MODEL_ID = 'glm-4.6v';

console.log('开始测试 GLM-4.6V...');

const data = JSON.stringify({
  model: MODEL_ID,
  messages: [
    {
      role: 'user',
      content: '你好'
    }
  ],
  max_tokens: 100
});

console.log('请求数据:', data);

const options = {
  hostname: 'open.bigmodel.cn',
  port: 443,
  path: '/api/paas/v4/chat/completions',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GLM_API_KEY}`
  }
};

const req = https.request(options, (res) => {
  console.log('响应状态码:', res.statusCode);
  console.log('响应头:', JSON.stringify(res.headers, null, 2));

  let responseData = '';

  res.on('data', (chunk) => {
    responseData += chunk;
    process.stdout.write('.');
  });

  res.on('end', () => {
    console.log('\n');
    console.log('完整响应:', responseData);

    try {
      const json = JSON.parse(responseData);
      if (json.error) {
        console.error('API Error:', json.error);
      } else {
        console.log('成功！');
        console.log('回复:', json.choices[0].message.content);
      }
    } catch (error) {
      console.error('Parse Error:', error.message);
      console.log('Raw response:', responseData);
    }
  });
});

req.on('error', (error) => {
  console.error('Request Error:', error.message);
});

req.write(data);
req.end();

console.log('请求已发送...');
