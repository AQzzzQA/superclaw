#!/bin/bash
# 股票分析工具 - 批量更新价格脚本

STOCK_DATA_FILE="/root/.openclaw/workspace/stock_data.json"

echo "股票价格批量更新工具"
echo "================================"
echo ""

# 检查数据文件是否存在
if [ ! -f "$STOCK_DATA_FILE" ]; then
    echo "错误：股票数据文件不存在"
    echo "请先运行 stock_analyzer.py 添加股票"
    exit 1
fi

# 显示当前持仓
echo "当前持仓："
echo "代码      名称          数量    买入价"
echo "----------------------------------------"
python3 << EOF
import json

with open("$STOCK_DATA_FILE", 'r', encoding='utf-8') as f:
    stock_data = json.load(f)

for code, data in stock_data.items():
    print(f"{code:<10} {data['name']:<15} {data['quantity']:>6} {data['buy_price']:>8.2f}")
EOF

echo ""
echo "================================"
echo "请按以下格式批量更新价格："
echo ""
echo "代码1 当前价1"
echo "代码2 当前价2"
echo "..."
echo ""
echo "例如："
echo "002156 60.50"
echo "002837 105.30"
echo ""
echo "输入完成后按 Ctrl+D 保存"
echo "================================"
echo ""

# 读取用户输入
> /tmp/stock_prices.txt

# 处理输入
python3 << EOF
import json

stock_data_file = "$STOCK_DATA_FILE"
price_file = "/tmp/stock_prices.txt"

# 读取股票数据
with open(stock_data_file, 'r', encoding='utf-8') as f:
    stock_data = json.load(f)

# 读取价格输入
with open(price_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 更新价格
updated_count = 0
for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    
    parts = line.split()
    if len(parts) >= 2:
        code = parts[0]
        try:
            current_price = float(parts[1])
            if code in stock_data:
                stock_data[code]['current_price'] = current_price
                stock_data[code]['update_time'] = "$(date '+%Y-%m-%d %H:%M:%S')"
                updated_count += 1
                print(f"已更新: {code} → {current_price}")
        except ValueError:
            print(f"价格格式错误: {line}")

# 保存更新后的数据
with open(stock_data_file, 'w', encoding='utf-8') as f:
    json.dump(stock_data, f, ensure_ascii=False, indent=2)

print(f"\n共更新 {updated_count} 只股票")
EOF

echo ""
echo "================================"
echo "更新完成！运行以下命令查看分析报告："
echo ""
echo "  python3 /root/.openclaw/workspace/stock_analyzer.py"
echo ""
