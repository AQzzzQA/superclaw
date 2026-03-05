#!/usr/bin/env python3
# 添加出价策略路由
with open('/root/.openclaw/workspace/ad-platform/web/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 在菜单项中添加出价策略
content = content.replace(
    '''{ key: '/conversions', label: '转化追踪', icon: <SwapOutlined />, onClick: () => navigate('/conversions') },''',
    '''{ key: '/conversions', label: '转化追踪', icon: <SwapOutlined />, onClick: () => navigate('/conversions') },
    { type: 'divider' as const },
    { key: '/bidding', label: '出价策略', icon: <PartitionOutlined />, onClick: () => navigate('/bidding') },
    { type: 'divider' as const },'''
)

with open('/root/.openclaw/workspace/ad-platform/web/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added bidding route to App.tsx")
