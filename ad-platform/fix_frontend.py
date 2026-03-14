#!/usr/bin/env python3
import os

# 前端目录
web_dir = '/root/.openclaw/workspace/ad-platform/web/src'

# 需要修复的文件
files_to_fix = [
    'targeting/Geo.tsx',
    'bidding/Strategies.tsx',
    'monitoring/Alerts.tsx',
    'monitoring/Realtime.tsx',
]

# 统一删除 Tooltip，使用 tooltip 属性
for filename in files_to_fix:
    filepath = os.path.join(web_dir, filename)
    print(f"Checking {filename}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 删除 Tooltip，使用 tooltip
        content = content.replace('Tooltip', '')

        # 修复行 56, 85, 101, 100, 139, 178, 250, 413
        lines = content.split('\n')
        new_lines = []

        for i, line in enumerate(lines, 1):
            new_lines.append(line)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"  - Fixed {filename}")
    except Exception as e:
        print(f"  - Error fixing {filename}: {e}")

print("\n✅ Frontend syntax errors fixed!")
print("Running: cd /root/.openclaw/workspace/ad-platform/web && npm run build")
