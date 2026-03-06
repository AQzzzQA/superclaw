# Playwright 手机模拟器配置指南

## 📱 支持的设备

Playwright 可以模拟以下移动设备：

### Android 设备
```javascript
const { devices } = require('playwright');

// Galaxy S21 Ultra
const galaxyS21 = devices['Galaxy S21 Ultra'];
// iPhone 13 Pro Max
const iPhone13 = devices['iPhone 13 Pro Max'];
// iPad Pro
const iPadPro = devices['iPad Pro'];
// Pixel 6
const pixel6 = devices['Pixel 6'];
```

### 设备配置对比

| 设备 | 屏幕分辨率 | User-Agent | 平台 |
|------|------------|-----------|------|
| Galaxy S21 Ultra | 1080x2400 | Mozilla/5.0 (Linux; Android 12) | Android |
| iPhone 13 Pro Max | 1284x2778 | Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) | iOS |
| iPad Pro 12.9 | 1024x1366 | Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) | iOS |
| Pixel 6 | 1080x2400 | Mozilla/5.0 (Linux; Android 13) | Android |

## 🚀 快速开始

### 1. 基础 Android 模拟

```javascript
const { chromium } = require('playwright');

async function runAndroidBot() {
  // 1. 启动浏览器
  const browser = await chromium.launch({
    headless: false,  // 显示浏览器
    args: [
      '--window-size=375,812',  // Android 视口大小
      '--user-agent=Mozilla/5.0 (Linux; Android 12; SM-S908L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    ],
  });

  // 2. 创建页面上下文
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    userAgent: 'Mozilla/5.0 (Linux; Android 12; SM-S908L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    // 3. 设置地理位置（模拟北京）
    geolocation: {
      latitude: 39.9042,
      longitude: 116.4074,
      accuracy: 100,
    },
    permissions: ['geolocation'],
  });

  const page = await context.newPage();

  // 4. 访问目标网站
  await page.goto('https://www.zhipin.com/web/geek/job', {
    waitUntil: 'networkidle',
  });

  // 5. 执行操作...
  await page.click('.job-card');
  // ... 更多操作
}
```

### 2. iOS 模拟

```javascript
const { chromium, devices } = require('playwright');

async function runIOSBot() {
  // 1. 启动浏览器
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--window-size=414,896',
      '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    ],
  });

  // 2. 使用 iOS 设备配置
  const iPhone13 = devices['iPhone 13 Pro Max'];

  const context = await browser.newContext({
    ...iPhone13,  // 使用预配置的设备参数
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    geolocation: {
      latitude: 31.2304,
      longitude: 121.4737,
      accuracy: 100,
    },
    permissions: ['geolocation'],
  });

  const page = await context.newPage();

  // 3. 访问网站
  await page.goto('https://www.zhipin.com', {
    waitUntil: 'networkidle',
  });

  // 4. 执行操作
  await page.click('.search-button');
  // ... 更多操作
}
```

## 📋 Boss 直聘专用配置

### Boss 直聘移动端适配

```javascript
// Boss 直聘移动端 User-Agent
const BOSS_MOBILE_UA = 'Mozilla/5.0 (Linux; Android 12; SM-G988B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 MicroMessenger/4.3.4.2100';

// Boss 直聘 iOS 端 User-Agent
const BOSS_IOS_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1';

// 视口大小（模拟 iPhone 13 Pro Max）
const IPHONE_VIEWPORT = {
  width: 414,
  height: 896,
};

// 视口大小（模拟常见 Android）
const ANDROID_VIEWPORT = {
  width: 375,
  height: 812,
};

// 移动端特征
const MOBILE_FEATURES = {
  touchSupport: true,
  hasTouchScreen: true,
  isMobile: true,
  deviceScaleFactor: 3,  // iPhone Retina 屏缩放
};

async function runBossMobileBot() {
  const { chromium } = require('playwright');

  const browser = await chromium.launch({
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-features=VizDisplayCompositor',
    ],
  });

  // 创建移动端上下文
  const context = await browser.newContext({
    viewport: ANDROID_VIEWPORT,
    userAgent: BOSS_MOBILE_UA,
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    geolocation: {
      latitude: 39.9042,  // 北京
      longitude: 116.4074,
      accuracy: 100,
    },
    permissions: ['geolocation'],
    // 关键：设置移动端特征
    hasTouchScreen: true,
    isMobile: true,
    deviceScaleFactor: 3,
  });

  const page = await context.newPage();

  // 注入移动端脚本（模拟触摸操作）
  await page.addInitScript(`
    Object.defineProperty(navigator, 'userAgent', {
      get: () => '${BOSS_MOBILE_UA}',
    });
    Object.defineProperty(navigator, 'maxTouchPoints', {
      get: () => 5,
    });
    Object.defineProperty(navigator, 'touchStart', {
      value: function() {},
      writable: false,
    });
  `);

  // 访问 Boss 直聘
  await page.goto('https://m.zhipin.com/', {
    waitUntil: 'networkidle',
  });

  // 模拟触摸点击
  await page.tap('.job-card');
  
  // 执行其他操作...
}
```

### 完整示例：自动投递简历

```javascript
const { chromium } = require('playwright');

async function autoApplyJobs() {
  console.log('启动 Boss 直聘自动投递机器人...');

  const browser = await chromium.launch({
    headless: false,
    args: [
      '--window-size=375,812',
      '--disable-blink-features=AutomationControlled',
    ],
  });

  const context = await browser.newContext({
    viewport: ANDROID_VIEWPORT,
    userAgent: BOSS_MOBILE_UA,
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    geolocation: {
      latitude: randomLocation().lat,
      longitude: randomLocation().lon,
      accuracy: 100,
    },
    permissions: ['geolocation'],
  });

  const page = await context.newPage();

  try {
    // 1. 登录
    await page.goto('https://m.zhipin.com/user/login', {
      waitUntil: 'networkidle',
    });
    await randomDelay(2000, 4000);

    // 2. 输入手机号（需要替换）
    await page.fill('#mobile', '13800138000');
    await randomDelay(1000, 2000);

    // 3. 输入密码
    await page.fill('#password', 'your_password');
    await randomDelay(1000, 2000);

    // 4. 点击登录
    await page.tap('.login-btn');
    await randomDelay(3000, 5000);

    // 5. 浏览职位（模拟正常行为）
    console.log('开始浏览职位...');
    for (let i = 0; i < 5; i++) {
      await browseJobDetails(page);
      await randomDelay(5000, 10000);  // 每个职位看 5-10 秒
    }

    // 6. 开始投递
    console.log('开始投递...');
    await startApplications(page, {
      dailyLimit: 3,  // 每天投递 3 份
      interval: 1800000,  // 每份投递间隔 30 分钟
    });

  } catch (error) {
    console.error('操作失败:', error);
    await page.screenshot({ path: 'error.png' });
  } finally {
    await context.close();
    await browser.close();
  }
}

// 辅助函数
async function browseJobDetails(page) {
  await page.goto('https://m.zhipin.com/web/geek/job', {
    waitUntil: 'networkidle',
  });
  await randomDelay(3000, 6000);  // 模拟阅读时间

  // 随机滚动
  await page.evaluate(() => window.scrollBy(0, Math.random() * 300));
  await randomDelay(1000, 2000);
}

async function startApplications(page, options) {
  const { dailyLimit, interval } = options;

  for (let i = 0; i < dailyLimit; i++) {
    console.log(`投递第 ${i + 1} 份简历...`);

    // 查找职位
    await page.goto('https://m.zhipin.com/web/geek/job', {
      waitUntil: 'networkidle',
    });

    // 点击投递按钮
    await page.tap('.apply-button');
    await randomDelay(2000, 3000);

    // 等待随机间隔
    if (i < dailyLimit - 1) {
      console.log(`等待 ${interval / 60000} 分钟后继续...`);
      await randomDelay(interval - 20000, interval + 20000);
    }
  }

  console.log(`今日投递完成，共 ${dailyLimit} 份`);
}

// 地理位置随机化
function randomLocation() {
  const locations = [
    { lat: 39.9042, lon: 116.4074 },  // 北京
    { lat: 31.2304, lon: 121.4737 },  // 上海
    { lat: 23.1291, lon: 113.2644 },  // 广州
    { lat: 22.5431, lon: 114.0579 },  // 深圳
    { lat: 30.2741, lon: 120.1551 },  // 杭州
  ];
  return locations[Math.floor(Math.random() * locations.length)];
}

// 随机延迟
function randomDelay(min, max) {
  const delay = Math.random() * (max - min) + min;
  return new Promise(resolve => setTimeout(resolve, delay));
}

// 启动
autoApplyJobs().catch(console.error);
```

## 🎯 触摸事件模拟

### 点击
```javascript
// 使用 Playwright 的 tap 方法（模拟触摸）
await page.tap('.apply-button');
```

### 滑动
```javascript
// 模拟手指滑动
await page.touchscreen.swipe(startX, startY, endX, endY);
```

### 长按
```javascript
// 模拟长按操作
await page.touchscreen.tap(x, y);
await page.waitForTimeout(2000);  // 按住 2 秒
await page.touchscreen.tapUp(x, y);
```

## 🔍 设备检测技巧

### 检测是否为移动端
```javascript
async function checkIfMobile(page) {
  const isMobile = await page.evaluate(() => {
    return /Mobi|Android/i.test(navigator.userAgent) ||
           'ontouchstart' in window ||
           window.innerWidth < 768;
  });

  console.log('是否移动端:', isMobile);
  return isMobile;
}
```

### 获取设备信息
```javascript
async function getDeviceInfo(page) {
  const deviceInfo = await page.evaluate(() => {
    return {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language,
      screen: {
        width: window.screen.width,
        height: window.screen.height,
        pixelRatio: window.devicePixelRatio,
      },
      touch: 'ontouchstart' in window,
      orientation: window.screen.orientation?.type,
    };
  });

  console.log('设备信息:', JSON.stringify(deviceInfo, null, 2));
  return deviceInfo;
}
```

## 📊 完整项目示例

### boss-mobile-bot.js

```javascript
/**
 * Boss 直聘移动端自动化脚本
 * 使用 Playwright 模拟 Android/iOS 设备
 */

const { chromium } = require('playwright');
const fs = require('fs');

// 配置
const CONFIG = {
  // 设备选择
  device: 'android',  // 'android' | 'ios'
  
  // 操作配置
  operations: {
    applyLimit: 3,  // 每天投递份数
    browseCount: 5,   // 每天浏览职位数
    browseInterval: 1800000,  // 浏览间隔 30 分钟
    applyInterval: 1800000, // 投递间隔 30 分钟
  },
  
  // 地理位置
  location: {
    mode: 'random',  // 'fixed' | 'random'
    fixed: { lat: 39.9042, lon: 116.4074 },  // 北京
  },
  
  // 账号配置
  account: {
    phone: '13800138000',
    password: 'your_password',
  },
};

// 主函数
async function main() {
  console.log('🚀 Boss 直聘移动端自动化机器人启动');
  console.log('📱 设备:', CONFIG.device);
  console.log('📊 配置:', JSON.stringify(CONFIG, null, 2));

  const browser = await chromium.launch({
    headless: false,
    args: [
      '--window-size=375,812',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
    ],
  });

  const context = await browser.newContext({
    viewport: CONFIG.device === 'ios' ? 
      { width: 414, height: 896, deviceScaleFactor: 3 } :
      { width: 375, height: 812 },
    userAgent: CONFIG.device === 'ios' ? 
      'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1' :
      'Mozilla/5.0 (Linux; Android 12; SM-S908L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 MicroMessenger/4.3.4.2100',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    geolocation: getLocation(),
    permissions: ['geolocation'],
    hasTouchScreen: true,
    isMobile: true,
  });

  const page = await context.newPage();

  // 隐藏自动化特征
  await hideAutomationDetection(page);

  try {
    // 1. 登录
    await login(page);

    // 2. 浏览阶段
    await browsePhase(page);

    // 3. 投递阶段
    await applyPhase(page);

  } catch (error) {
    console.error('❌ 错误:', error);
    await page.screenshot({ path: 'error.png' });
  } finally {
    await context.close();
    await browser.close();
  }
}

// 辅助函数
async function hideAutomationDetection(page) {
  await page.addInitScript(`
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });
    Object.defineProperty(navigator, 'automation', {
      get: () => false,
    });
  `);
}

async function login(page) {
  console.log('🔐 登录中...');
  await page.goto('https://m.zhipin.com/user/login', {
    waitUntil: 'networkidle',
  });

  await randomDelay(2000, 3000);
  await page.fill('#mobile', CONFIG.account.phone);
  await randomDelay(1000, 2000);
  await page.fill('#password', CONFIG.account.password);
  await randomDelay(1000, 2000);

  await page.tap('.login-btn');
  await randomDelay(3000, 5000);
  console.log('✅ 登录成功');
}

async function browsePhase(page) {
  console.log('📖 浏览职位阶段...');
  
  for (let i = 0; i < CONFIG.operations.browseCount; i++) {
    await page.goto('https://m.zhipin.com/web/geek/job', {
      waitUntil: 'networkidle',
    });

    await randomDelay(3000, 8000);  // 阅读时间

    // 随机滚动
    await page.evaluate(() => {
      window.scrollBy(0, Math.random() * 500);
    });

    await randomDelay(1000, 2000);
  }

  console.log('✅ 浏览完成');
}

async function applyPhase(page) {
  console.log('📤 投递阶段...');
  
  for (let i = 0; i < CONFIG.operations.applyLimit; i++) {
    await page.goto('https://m.zhipin.com/web/geek/job', {
      waitUntil: 'networkidle',
    });

    // 点击投递按钮
    await page.tap('.apply-button');
    await randomDelay(2000, 3000);

    // 等待间隔
    if (i < CONFIG.operations.applyLimit - 1) {
      await randomDelay(
        CONFIG.operations.applyInterval - 10000,
        CONFIG.operations.applyInterval + 10000
      );
    }
  }

  console.log('✅ 投递完成');
}

function getLocation() {
  if (CONFIG.location.mode === 'fixed') {
    return CONFIG.location.fixed;
  } else {
    return {
      latitude: 39.9042 + (Math.random() - 0.5) * 2,
      longitude: 116.4074 + (Math.random() - 0.5) * 2,
      accuracy: 100 + Math.random() * 50,
    };
  }
}

function randomDelay(min, max) {
  const delay = Math.random() * (max - min) + min;
  return new Promise(resolve => setTimeout(resolve, delay));
}

// 启动
main().catch(console.error);
```

## 🎯 运行步骤

### 1. 安装依赖

```bash
npm install -g playwright
```

### 2. 运行脚本

```bash
node boss-mobile-bot.js
```

### 3. 配置说明

修改脚本中的 `CONFIG` 对象：

- `device`: 设备类型
  - `android`: 模拟 Android 设备
  - `ios`: 模拟 iOS 设备

- `operations`: 操作配置
  - `applyLimit`: 每天投递份数（推荐 3）
  - `browseCount`: 每天浏览职位数（推荐 5-10）

- `account`: 账号信息
  - `phone`: 手机号
  - `password`: 密码

## ⚠️ 注意事项

1. **合规性**: 确保遵守 Boss 直聘服务条款
2. **频率控制**: 不要过于频繁，建议每天 3-5 次投递
3. **账号安全**: 定期更换手机号和密码
4. **模拟真实**: 添加人类行为，不要机械化
5. **监控**: 及时检查账号状态，避免封禁

## 📊 效果对比

| 指标 | PC 自动化 | 移动端模拟 |
|------|-----------|-------------|
| 风控检测难度 | 高 | 低 |
| 账号存活率 | 低 | 高 |
| 操作成功率 | 中 | 高 |
| 适合场景 | 批量操作 | 真实求职 |

---

**创建时间**: 2026-03-06
**版本**: 1.0
**状态**: 移动端自动化配置
