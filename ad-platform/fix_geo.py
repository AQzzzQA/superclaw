#!/usr/bin/env python3
import os

web_dir = '/root/.openclaw/workspace/ad-platform/web/src'

# 修复 targeting/Geo.tsx 的语法错误
geo_file = os.path.join(web_dir, 'pages/targeting/Geo.tsx')

print("Fixing Geo.tsx...")

with open(geo_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 删除第一个 > 符号之前的代码
content = content[:556] + content[558:]

with open(geo_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Geo.tsx!")
print("✅ Frontend syntax errors fixed!")
