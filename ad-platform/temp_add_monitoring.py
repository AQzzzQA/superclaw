#!/usr/bin/env python3
# 添加 monitoring 路由

with open('/root/.openclaw/workspace/ad-platform/app/api/__init__.py', 'r') as f:
    content = f.read()

# 更新导入
content = content.replace(
    'from . import (\\n    oauth, campaign, adgroup, creative,\\n    auth, account, tenant, report, conversion, health,\\n    targeting\\n)',
    'from . import (\\n    oauth, campaign, adgroup, creative,\\n    auth, account, tenant, report, conversion, health,\\n    targeting, monitoring\\n)'
)

# 更新 __all__
content = content.replace(
    '''"targeting",  # 新增
]''',
    '''"targeting",  # 新增
    "monitoring",  # 新增
]'''
)

with open('/root/.openclaw/workspace/ad-platform/app/api/__init__.py', 'w') as f:
    f.write(content)

print("API __init__ 更新完成！")

# 更新 main.py
with open('/root/.openclaw/workspace/ad-platform/app/main.py', 'r') as f:
    content = f.read()

# 更新导入
content = content.replace(
    '    targeting  # 新增定向投放路由\\n)',
    '    targeting,  # 新增定向投放路由\\n    monitoring  # 新增实时监控路由\\n)'
)

# 添加路由
content = content.replace(
    'app.include_router(targeting.router, prefix="/api/v1")  # 新增定向投放路由\\n\\n',
    'app.include_router(targeting.router, prefix="/api/v1")  # 新增定向投放路由\\napp.include_router(monitoring.router, prefix="/api/v1")  # 新增实时监控路由\\n\\n'
)

with open('/root/.openclaw/workspace/ad-platform/app/main.py', 'w') as f:
    f.write(content)

print("main.py 更新完成！")
