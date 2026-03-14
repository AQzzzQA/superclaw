#!/usr/bin/env node

/**
 * GLM-4.6V 模型测试脚本
 *
 * 这个脚本用于测试 GLM-4.6V 模型的基本功能
 */

const https = require('https');

const GLM_API_KEY = 'c2e9c086c6af40b6b27e568a95b4d097.YKcM2eGMTGdp8plZ';
const GLM_BASE_URL = 'open.bigmodel.cn';
const MODEL_ID = 'glm-4.6v';

/**
 * 发送请求到 GLM API
 */
async function chatWithGLM(messages) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: MODEL_ID,
      messages: messages,
      max_tokens: 2000,
      temperature: 0.7
    });

    const options = {
      hostname: GLM_BASE_URL,
      port: 443,
      path: '/api/paas/v4/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Length': Buffer.byteLength(data)
      }
    };

    console.log('发送请求到:', `https://${GLM_BASE_URL}${options.path}`);
    console.log('请求数据:', data.substring(0, 200) + '...');

    const req = https.request(options, (res) => {
      console.log('响应状态码:', res.statusCode);
      console.log('响应头:', JSON.stringify(res.headers, null, 2));

      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          console.log('响应数据:', responseData.substring(0, 500) + '...');
          const json = JSON.parse(responseData);
          if (json.error) {
            reject(new Error(`API Error: ${json.error.message}`));
          } else {
            resolve(json);
          }
        } catch (error) {
          reject(new Error(`Parse Error: ${error.message}\nResponse: ${responseData.substring(0, 200)}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.write(data);
    req.end();
  });
}

/**
 * 测试 1: 基础对话
 */
async function testBasicChat() {
  console.log('\n📝 测试 1: 基础对话');
  console.log('=' .repeat(50));

  const messages = [
    {
      role: 'user',
      content: '你好！请用一句话自我介绍。'
    }
  ];

  try {
    const response = await chatWithGLM(messages);
    const content = response.choices[0].message.content;
    console.log('✅ 成功！');
    console.log('回复:', content);
    return true;
  } catch (error) {
    console.log('❌ 失败！');
    console.error('错误:', error.message);
    return false;
  }
}

/**
 * 测试 2: 代码生成
 */
async function testCodeGeneration() {
  console.log('\n💻 测试 2: 代码生成');
  console.log('=' .repeat(50));

  const messages = [
    {
      role: 'user',
      content: '请写一个 Python 函数，计算斐波那契数列的第 n 项。'
    }
  ];

  try {
    const response = await chatWithGLM(messages);
    const content = response.choices[0].message.content;
    console.log('✅ 成功！');
    console.log('生成的代码:');
    console.log(content);
    return true;
  } catch (error) {
    console.log('❌ 失败！');
    console.error('错误:', error.message);
    return false;
  }
}

/**
 * 测试 3: 逻辑推理
 */
async function testLogicalReasoning() {
  console.log('\n🧠 测试 3: 逻辑推理');
  console.log('=' .repeat(50));

  const messages = [
    {
      role: 'user',
      content: '如果今天是星期五，后天是星期几？请说明推理过程。'
    }
  ];

  try {
    const response = await chatWithGLM(messages);
    const content = response.choices[0].message.content;
    console.log('✅ 成功！');
    console.log('推理结果:', content);
    return true;
  } catch (error) {
    console.log('❌ 失败！');
    console.error('错误:', error.message);
    return false;
  }
}

/**
 * 测试 4: 多轮对话
 */
async function testMultiTurnChat() {
  console.log('\n💬 测试 4: 多轮对话');
  console.log('=' .repeat(50));

  const messages = [
    {
      role: 'user',
      content: '我想了解 JavaScript 的箭头函数。'
    },
    {
      role: 'assistant',
      content: '箭头函数是 ES6 引入的一种新的函数语法，它提供了更简洁的函数写法。'
    },
    {
      role: 'user',
      content: '能给我一个例子吗？'
    }
  ];

  try {
    const response = await chatWithGLM(messages);
    const content = response.choices[0].message.content;
    console.log('✅ 成功！');
    console.log('回复:', content);
    return true;
  } catch (error) {
    console.log('❌ 失败！');
    console.error('错误:', error.message);
    return false;
  }
}

/**
 * 测试 5: 创意写作
 */
async function testCreativeWriting() {
  console.log('\n✍️  测试 5: 创意写作');
  console.log('=' .repeat(50));

  const messages = [
    {
      role: 'user',
      content: '请写一首关于春天的 4 行短诗。'
    }
  ];

  try {
    const response = await chatWithGLM(messages);
    const content = response.choices[0].message.content;
    console.log('✅ 成功！');
    console.log('诗歌:');
    console.log(content);
    return true;
  } catch (error) {
    console.log('❌ 失败！');
    console.error('错误:', error.message);
    return false;
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('\n🚀 GLM-4.6V 模型测试');
  console.log('=' .repeat(50));
  console.log('模型 ID:', MODEL_ID);
  console.log('时间:', new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));

  const tests = [
    testBasicChat,
    testCodeGeneration,
    testLogicalReasoning,
    testMultiTurnChat,
    testCreativeWriting
  ];

  let successCount = 0;
  let failCount = 0;

  for (const test of tests) {
    const result = await test();
    if (result) {
      successCount++;
    } else {
      failCount++;
    }

    // 等待 1 秒，避免请求过快
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  console.log('\n📊 测试结果汇总');
  console.log('=' .repeat(50));
  console.log(`总测试数: ${tests.length}`);
  console.log(`成功: ${successCount} ✅`);
  console.log(`失败: ${failCount} ❌`);
  console.log(`成功率: ${(successCount / tests.length * 100).toFixed(1)}%`);

  if (successCount === tests.length) {
    console.log('\n🎉 所有测试通过！GLM-4.6V 模型工作正常。');
    process.exit(0);
  } else {
    console.log('\n⚠️  部分测试失败，请检查错误信息。');
    process.exit(1);
  }
}

// 运行测试
main().catch(error => {
  console.error('测试运行出错:', error);
  process.exit(1);
});
