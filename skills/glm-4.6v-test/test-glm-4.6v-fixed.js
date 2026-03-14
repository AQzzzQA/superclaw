#!/usr/bin/env node

/**
 * GLM-4.6V 模型测试脚本（修复版）
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
async function chatWithGLM(messages, maxTokens = 2000) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: MODEL_ID,
      messages: messages,
      max_tokens: maxTokens,
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

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);

          if (json.error) {
            reject(new Error(`API Error: ${json.error.message || JSON.stringify(json.error)}`));
          } else if (json.choices && json.choices.length > 0) {
            const choice = json.choices[0];
            const content = choice.message.content || '';
            const reasoningContent = choice.message.reasoning_content || '';

            resolve({
              content: content,
              reasoningContent: reasoningContent,
              finishReason: choice.finish_reason,
              usage: json.usage,
              model: json.model,
              id: json.id
            });
          } else {
            reject(new Error('No choices in response'));
          }
        } catch (error) {
          reject(new Error(`Parse Error: ${error.message}\nResponse: ${responseData.substring(0, 500)}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
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
    const content = response.content || response.reasoningContent || '(无内容)';
    console.log('✅ 成功！');
    console.log('回复:', content);
    console.log('使用 tokens:', response.usage.total_tokens);
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
    const response = await chatWithGLM(messages, 1000);
    const content = response.content || response.reasoningContent || '(无内容)';
    console.log('✅ 成功！');
    console.log('生成的代码:');
    console.log(content);
    console.log('使用 tokens:', response.usage.total_tokens);
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
    const content = response.content || response.reasoningContent || '(无内容)';
    console.log('✅ 成功！');
    console.log('推理结果:', content);
    console.log('使用 tokens:', response.usage.total_tokens);
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
    const content = response.content || response.reasoningContent || '(无内容)';
    console.log('✅ 成功！');
    console.log('回复:', content);
    console.log('使用 tokens:', response.usage.total_tokens);
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
    const content = response.content || response.reasoningContent || '(无内容)';
    console.log('✅ 成功！');
    console.log('诗歌:');
    console.log(content);
    console.log('使用 tokens:', response.usage.total_tokens);
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
  console.log('API 地址:', `https://${GLM_BASE_URL}/api/paas/v4/chat/completions`);
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
  const errors = [];

  for (const test of tests) {
    try {
      const result = await test();
      if (result) {
        successCount++;
      } else {
        failCount++;
      }
    } catch (error) {
      console.error('测试异常:', error.message);
      errors.push(error.message);
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

  if (errors.length > 0) {
    console.log('\n错误信息:');
    errors.forEach((error, index) => {
      console.log(`  ${index + 1}. ${error}`);
    });
  }

  if (successCount === tests.length) {
    console.log('\n🎉 所有测试通过！GLM-4.6V 模型工作正常。');
    process.exit(0);
  } else if (successCount > 0) {
    console.log('\n⚠️  部分测试通过，模型基本可用。');
    process.exit(0);
  } else {
    console.log('\n❌ 所有测试失败，请检查配置和网络。');
    process.exit(1);
  }
}

// 运行测试
main().catch(error => {
  console.error('测试运行出错:', error);
  process.exit(1);
});
