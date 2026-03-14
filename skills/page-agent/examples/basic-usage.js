/**
 * Page Agent 基础使用示例
 *
 * 这个示例展示了如何使用 Page Agent 来自动化网页操作
 */

import { PageAgent } from 'page-agent'

// 示例 1: 基础初始化
async function basicExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
  })

  await agent.execute('点击登录按钮')
}

// 示例 2: 批量执行
async function batchExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
  })

  await agent.execute([
    '点击登录按钮',
    '输入用户名',
    '输入密码',
    '点击提交'
  ])
}

// 示例 3: 事件监听
async function eventExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
  })

  agent.on('step', (step) => {
    console.log('执行步骤:', step)
  })

  agent.on('error', (error) => {
    console.error('错误:', error)
  })

  await agent.execute('填写注册表单')
}

// 示例 4: 自定义系统提示词
async function customPromptExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
    systemPrompt: '你是一个专业的自动化测试助手，专注于测试表单功能'
  })

  await agent.execute('测试登录表单的所有验证规则')
}

// 示例 5: OpenAI 配置
async function openaiExample() {
  const agent = new PageAgent({
    model: 'gpt-4o',
    baseURL: 'https://api.openai.com/v1',
    apiKey: process.env.OPENAI_API_KEY,
    language: 'zh-CN',
  })

  await agent.execute('导航到设置页面并更新用户偏好')
}

// 示例 6: 英文指令
async function englishExample() {
  const agent = new PageAgent({
    model: 'gpt-4o',
    baseURL: 'https://api.openai.com/v1',
    apiKey: process.env.OPENAI_API_KEY,
    language: 'en-US',
  })

  await agent.execute('Click the submit button and wait for the response')
}

// 示例 7: 错误处理
async function errorHandlingExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
  })

  try {
    await agent.execute('执行一个不存在的操作')
  } catch (error) {
    console.error('执行失败:', error)
    // 处理错误，比如重试或回退
  }
}

// 示例 8: 表单自动化（ERP/CRM 场景）
async function erpFormExample() {
  const agent = new PageAgent({
    model: 'qwen-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: process.env.DASHSCOPE_API_KEY,
    language: 'zh-CN',
  })

  // 原本需要 20+ 步的操作，现在一句话完成
  await agent.execute('创建新的销售订单：客户选择"ABC公司"，添加3个产品，总价计算正确，然后保存订单')
}

export {
  basicExample,
  batchExample,
  eventExample,
  customPromptExample,
  openaiExample,
  englishExample,
  errorHandlingExample,
  erpFormExample,
}
