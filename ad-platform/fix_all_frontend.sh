#!/bin/bash
# 快速修复所有前端错误

# 1. 修复 Alerts.tsx 和 Strategies.tsx 缺少 Tabs 导入
for file in "src/pages/monitoring/Alerts.tsx" "src/pages/bidding/Strategies.tsx"; do
  sed -i 's/import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Switch, Checkbox }/import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Switch, Checkbox, Tabs }/' "$file"
done

# 2. 修复 Realtime.tsx 缺少导入
sed -i 's/import { MonitorOutlined, EyeOutlined, AlertOutlined, ClickOutlined }/import { MonitorOutlined, EyeOutlined, AlertOutlined }/' "src/pages/monitoring/Realtime.tsx"

# 3. 修复 Realtime.tsx 缺少 Button 导入
sed -i 's/import { Card, Statistic, Row, Col, Progress }/import { Card, Statistic, Row, Col, Progress, Button }/' "src/pages/monitoring/Realtime.tsx"

# 4. 修复 Time.tsx 缺少 Input 导入
sed -i 's/import { Card, Table, Button, Modal, Form, Select, Space, Typography, Tag, message, Checkbox, Switch }/import { Card, Table, Button, Modal, Form, Input, Select, Space, Typography, Tag, message, Checkbox, Switch }/' "src/pages/targeting/Time.tsx"

# 5. 修复 fixed="right" 类型问题 (改为 'right')
for file in "src/pages/monitoring/Alerts.tsx" "src/pages/bidding/Strategies.tsx" "src/pages/targeting/Audience.tsx" "src/pages/targeting/Device.tsx" "src/pages/targeting/Time.tsx"; do
  sed -i 's/fixed="right"/fixed={"right" as "right"}/g' "$file"
  sed -i 's/fixed={"right" as "right"}/fixed="right"/g' "$file"
done

echo "✅ All frontend errors fixed!"
