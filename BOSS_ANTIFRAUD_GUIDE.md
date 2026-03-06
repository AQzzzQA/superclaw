# Boss 直聘风控对抗指南

## 📋 风控检测机制

Boss 直聘平台可能检测以下特征：

1. **浏览器指纹**
   - User-Agent
   - 浏览器版本
   - 屏幕分辨率
   - 时区和语言

2. **自动化特征**
   - Webdriver 属性
   - Automation 控制标识
   - 异常的操作速度

3. **设备指纹**
   - Canvas 指纹
   - WebGL 指纹
   - 字体列表
   - 插件列表

4. **行为模式**
   - 操作间隔过于规律
   - 鼠标移动轨迹
   - 点击速度

5. **网络特征**
   - IP 地址
   - 地理位置
   - TLS 指纹

## 🛡️ 对抗策略

### 1. 浏览器指纹对抗

#### 使用 Playwright-stealth

```bash
npm install playwright-stealth puppeteer-extra-plugin-stealth
```

```javascript
const { chromium } = require('playwright-stealth');
const stealth = require('puppeteer-extra-plugin-stealth')();

const browser = await chromium.launch({
  headless: false, // 使用有头模式
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--disable-features=VizDisplayCompositor',
  ],
});

const context = await browser.newContext({
  // 随机化 User-Agent
  userAgent: randomUserAgent(),
  
  // 随机化视口
  viewport: {
    width: randomInt(1920, 2560),
    height: randomInt(1080, 1440),
  },
  
  // 随机化语言
  locale: randomChoice(['zh-CN', 'en-US', 'zh-TW']),
  timezoneId: 'Asia/Shanghai',
  
  // 设置地理位置
  geolocation: {
    latitude: randomFloat(39.8, 40.0),
    longitude: randomFloat(116.3, 116.5),
  },
  permissions: ['geolocation'],
});
```

#### 注入反检测脚本

```javascript
// 在页面加载前注入
await page.addInitScript(`
  // 1. 隐藏 webdriver
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
  });
  
  // 2. 隐藏 Chrome 对象
  window.chrome = {
    runtime: {
      ...({ OnInstallListener: {}, OnRestartListener: {} })
    },
    loadTimes: {},
    csi: () => {},
    app: {}
  };
  
  // 3. 修复 permissions
  navigator.permissions = new Proxy(navigator.permissions, {
    has: () => true,
    requestPermission: () => Promise.resolve('granted'),
  });
  
  // 4. 随机化插件
  const plugins = [];
  for (let i = 0; i < 5; i++) {
    plugins.push({
      0: { type: 'application/x-google-chrome-pdf', suffixes: 'pdf', description: '' },
      name: 'Chrome PDF Plugin',
      filename: 'internal-pdf-viewer',
      length: 1,
    });
  }
  Object.defineProperty(navigator, 'plugins', {
    get: () => plugins,
  });
  
  // 5. 随机化语言
  Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'en', 'zh'],
  });
  
  // 6. 隐藏自动化标识
  Object.defineProperty(navigator, 'automation', {
    get: () => false,
  });
  
  // 7. 修复 WebGL
  const getParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) {
      return 'Intel Inc.';
    }
    return getParameter.call(this, parameter);
  };
  
  // 8. 修复 Canvas
  const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function(type) {
    if (type === 'image/png') {
      // 添加噪声
      const context = this.getContext('2d');
      const imageData = context.getImageData(0, 0, this.width, this.height);
      for (let i = 0; i < imageData.data.length; i += 4) {
        imageData.data[i] = imageData.data[i] + Math.random() - 0.5;
      }
      context.putImageData(imageData, 0, 0);
    }
    return originalToDataURL.apply(this, arguments);
  };
  
  // 9. 修复 Screen
  const originalScreen = window.screen;
  delete window.screen;
  Object.defineProperty(window, 'screen', {
    get: () => originalScreen,
    set: () => {},
  });
  
  // 10. 修复 Permission
  const originalQuery = window.navigator.permissions.query;
  window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
      Promise.resolve({ state: Notification.permission }) :
      originalQuery(parameters)
  );
`);
```

### 2. 行为模式对抗

#### 随机化操作速度

```javascript
// 工具函数
function randomDelay(min, max) {
  return Math.random() * (max - min) + min;
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 使用示例
await page.goto('https://www.zhipin.com/web/geek/job', {
  waitUntil: 'networkidle',
});

// 随机等待
await randomDelay(2000, 4000);

// 查找元素
const jobCard = await page.locator('.job-card-wrapper').first();
await jobCard.scrollIntoViewIfNeeded();

// 再次随机等待
await randomDelay(500, 1500);

// 模拟鼠标移动
const box = await jobCard.boundingBox();
await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);

await randomDelay(300, 800);

// 点击
await jobCard.click();
```

#### 模拟人类行为

```javascript
// 模拟阅读时间
async function simulateReading() {
  const readingTime = randomInt(3000, 8000); // 3-8 秒阅读时间
  await new Promise(resolve => setTimeout(resolve, readingTime));
}

// 模拟思考时间
async function simulateThinking() {
  const thinkingTime = randomInt(2000, 5000); // 2-5 秒思考时间
  await new Promise(resolve => setTimeout(resolve, thinkingTime));
}

// 使用示例
await simulateReading(); // 阅读职位详情
await simulateThinking(); // 思考是否投递
await page.click('.apply-button');
```

### 3. IP 和地理位置对抗

#### 代理池配置

```javascript
// 使用住宅 IP 代理
const PROXIES = [
  'http://user:pass@proxy1.example.com:8080',
  'http://user:pass@proxy2.example.com:8080',
  // ... 更多代理
];

// 随机选择代理
const randomProxy = PROXIES[Math.floor(Math.random() * PROXIES.length)];

const browser = await chromium.launch({
  proxy: {
    server: randomProxy,
  },
  args: [
    '--proxy-server=' + randomProxy,
  ],
});
```

#### 地理位置随机化

```javascript
// 中国主要城市坐标
const CITIES = [
  { name: '北京', lat: 39.9042, lon: 116.4074 },
  { name: '上海', lat: 31.2304, lon: 121.4737 },
  { name: '广州', lat: 23.1291, lon: 113.2644 },
  { name: '深圳', lat: 22.5431, lon: 114.0579 },
  { name: '杭州', lat: 30.2741, lon: 120.1551 },
  { name: '成都', lat: 30.5728, lon: 104.0668 },
];

function randomLocation() {
  return CITIES[Math.floor(Math.random() * CITIES.length)];
}

// 使用
const location = randomLocation();
const context = await browser.newContext({
  geolocation: {
    latitude: location.lat,
    longitude: location.lon,
  },
  permissions: ['geolocation'],
});
```

### 4. 插件特征对抗

#### 清理 manifest.json

```json
{
  "manifest_version": 3,
  "name": "智能求职助手",
  "version": "1.0.0",
  "description": "帮助用户快速找到心仪的工作机会",
  
  "permissions": [
    "storage",
    "activeTab"
  ],
  
  "host_permissions": [
    "*://*.zhipin.com/*",
    "*://*.bosszhipin.com/*"
  ],
  
  "content_scripts": [
    {
      "matches": ["*://*.zhipin.com/*"],
      "js": ["content.js"],
      "run_at": "document_idle"
    }
  ],
  
  "background": {
    "service_worker": "background.js"
  },
  
  "action": {},
  "default_locale": "zh_CN",
  
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  
  "web_accessible_resources": [
    "icons/*",
    "styles/*"
  ]
}
```

#### 避免可疑行为

```javascript
// 避免在短时间内大量操作
async function rateLimitOperations() {
  const MIN_INTERVAL = 2000; // 最小间隔 2 秒
  const lastOperation = await chrome.storage.local.get('lastOperation');
  
  const now = Date.now();
  if (lastOperation && (now - lastOperation) < MIN_INTERVAL) {
    const delay = MIN_INTERVAL - (now - lastOperation);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  await chrome.storage.local.set({ lastOperation: now });
}

// 避免同时操作多个标签
async function limitActiveTabs() {
  const tabs = await chrome.tabs.query({ active: true });
  if (tabs.length > 3) {
    throw new Error('Too many active tabs');
  }
}

// 避免异常请求频率
async function throttleRequests() {
  const MAX_REQUESTS_PER_MINUTE = 30;
  const requests = await chrome.storage.local.get('requests');
  
  const now = Date.now();
  const oneMinuteAgo = now - 60000;
  
  const recentRequests = requests.filter(r => r > oneMinuteAgo);
  if (recentRequests.length >= MAX_REQUESTS_PER_MINUTE) {
    throw new Error('Rate limit exceeded');
  }
  
  requests.push(now);
  await chrome.storage.local.set({ requests });
}
```

### 5. 完整示例代码

```javascript
const { chromium } = require('playwright');
const stealth = require('puppeteer-extra-plugin-stealth')();

async function runBot() {
  // 1. 启动浏览器
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
    ],
  });

  // 2. 创建上下文
  const location = randomLocation();
  const context = await browser.newContext({
    viewport: {
      width: 1920,
      height: 1080,
    },
    userAgent: randomUserAgent(),
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    geolocation: location,
    permissions: ['geolocation'],
  });

  // 3. 创建页面
  const page = await context.newPage();

  // 4. 注入反检测脚本
  await page.addInitScript(`
    // ... (上面的反检测脚本)
  `);

  try {
    // 5. 访问页面
    await page.goto('https://www.zhipin.com/web/geek/job', {
      waitUntil: 'networkidle',
      timeout: 30000,
    });

    // 6. 模拟人类操作
    await simulateReading();
    await simulateThinking();

    // 7. 执行操作
    const jobCard = await page.locator('.job-card-wrapper').first();
    await jobCard.scrollIntoViewIfNeeded();
    await randomDelay(500, 1500);
    
    const box = await jobCard.boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await randomDelay(300, 800);
    
    await jobCard.click();

    // 8. 等待响应
    await page.waitForLoadState('networkidle');
    await randomDelay(2000, 4000);

  } catch (error) {
    console.error('操作失败:', error);
    await page.screenshot({ path: 'error.png' });
  } finally {
    // 9. 清理
    await context.close();
    await browser.close();
  }
}

// 辅助函数
function randomUserAgent() {
  const userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  ];
  return userAgents[Math.floor(Math.random() * userAgents.length)];
}

function randomLocation() {
  const locations = [
    { lat: 39.9042, lon: 116.4074 },
    { lat: 31.2304, lon: 121.4737 },
  ];
  return locations[Math.floor(Math.random() * locations.length)];
}

async function randomDelay(min, max) {
  const delay = Math.random() * (max - min) + min;
  await new Promise(resolve => setTimeout(resolve, delay));
}

async function simulateReading() {
  await randomDelay(3000, 8000);
}

async function simulateThinking() {
  await randomDelay(2000, 5000);
}

// 启动
runBot().catch(console.error);
```

## 📊 风险评估

### 低风险策略（推荐）
- 随机化 User-Agent
- 模拟人类操作速度
- 适当的延迟

### 中风险策略
- 使用代理池
- 随机化地理位置
- 隐藏自动化特征

### 高风险策略（谨慎使用）
- 修改浏览器指纹
- 绕过验证码
- 大规模自动化

## ⚠️ 注意事项

1. **合规性**: 确保遵守 Boss 直聘的服务条款
2. **频率控制**: 避免频繁操作触发风控
3. **账号安全**: 使用独立账号，避免关联
4. **持续更新**: 风控机制会不断更新，需要持续对抗
5. **测试监控**: 小规模测试，监控封禁情况

## 🔍 监控和调试

```javascript
// 添加日志记录
async function logOperation(operation, status) {
  const log = {
    timestamp: new Date().toISOString(),
    operation: operation,
    status: status,
    userAgent: await page.evaluate(() => navigator.userAgent),
    location: await context.geolocation(),
  };
  
  await chrome.storage.local.get({ logs: [] }, ({ logs }) => {
    logs.push(log);
    chrome.storage.local.set({ logs });
  });
}

// 定期检查风控状态
async function checkRiskStatus() {
  const riskIndicators = await page.evaluate(() => {
    return {
      hasWebdriver: 'webdriver' in navigator,
      automationDetected: navigator.automation === false,
      chromeObject: 'chrome' in window,
    };
  });
  
  console.log('风控指标:', riskIndicators);
  return riskIndicators;
}
```

## 📚 参考资源

- Playwright 反检测: https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth
- 浏览器指纹: https://fingerprintjs.com/
- Boss 直聘 API: https://www.zhipin.com/api/
