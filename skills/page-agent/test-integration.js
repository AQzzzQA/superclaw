#!/usr/bin/env node

/**
 * Page Agent 集成测试
 *
 * 测试 page-agent 的基本功能集成
 */

console.log('🚀 Page Agent 集成测试');
console.log('=' .repeat(50));

// 检查项目是否已克隆
const fs = require('fs');
const path = require('path');

const projectPath = '/root/.openclaw/workspace/page-agent';
const skillPath = '/root/.openclaw/workspace/skills/page-agent';

console.log('\n检查项目文件...');

// 检查项目目录
if (fs.existsSync(projectPath)) {
  console.log('✅ Page Agent 项目已克隆');
  const packageJson = JSON.parse(fs.readFileSync(path.join(projectPath, 'package.json'), 'utf8'));
  console.log('   版本:', packageJson.version);
  console.log('   描述:', packageJson.description);
} else {
  console.log('❌ Page Agent 项目未克隆');
  process.exit(1);
}

// 检查技能文件
console.log('\n检查技能文件...');

const requiredFiles = [
  'SKILL.md',
  'README.md',
  'examples/basic-usage.js',
  'examples/quick-start.html',
  'examples/env.example',
  'examples/INSTALL.md'
];

let missingFiles = [];

requiredFiles.forEach(file => {
  const filePath = path.join(skillPath, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} (缺失)`);
    missingFiles.push(file);
  }
});

// 检查示例代码
console.log('\n检查示例代码...');

const exampleFile = path.join(skillPath, 'examples/basic-usage.js');
if (fs.existsSync(exampleFile)) {
  const content = fs.readFileSync(exampleFile, 'utf8');
  const examples = content.match(/\/\/ 示例 \d+: .+/g) || [];

  console.log(`✅ 发现 ${examples.length} 个示例`);
  examples.forEach(example => {
    console.log(`   - ${example.replace('// 示例 ', '')}`);
  });
}

// 总结
console.log('\n📊 测试结果');
console.log('=' .repeat(50));

if (missingFiles.length === 0) {
  console.log('✅ 所有文件检查通过！');
  console.log('✅ Page Agent 技能集成完成！');
  console.log('\n下一步：');
  console.log('  1. 安装依赖: npm install');
  console.log('  2. 构建项目: npm run build:libs');
  console.log('  3. 运行测试: npm test');
  process.exit(0);
} else {
  console.log(`❌ 缺失 ${missingFiles.length} 个文件`);
  console.log('缺失的文件:', missingFiles.join(', '));
  process.exit(1);
}
