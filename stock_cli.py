#!/usr/bin/env python3
"""
股票分析工具 - 命令行版本
无需网络请求，使用本地数据
"""

import json
import sys
from datetime import datetime

# 数据文件
STOCK_DATA_FILE = "/root/.openclaw/workspace/stock_data.json"

def load_stocks():
    """加载股票数据"""
    try:
        with open(STOCK_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：数据文件不存在 {STOCK_DATA_FILE}")
        return None

def save_stocks(stocks):
    """保存股票数据"""
    with open(STOCK_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

def update_price(code, price):
    """更新单只股票价格"""
    stocks = load_stocks()
    if not stocks:
        return False
    
    if code in stocks:
        stocks[code]['current_price'] = float(price)
        stocks[code]['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_stocks(stocks)
        print(f"✅ 已更新 {code} 价格为 {price}")
        return True
    else:
        print(f"❌ 股票代码 {code} 不存在")
        return False

def calculate_profit(code, stocks):
    """计算单只股票盈亏"""
    stock = stocks[code]
    
    if stock['current_price'] is None:
        return {
            'code': code,
            'name': stock['name'],
            'status': 'waiting'
        }
    
    profit = (stock['current_price'] - stock['buy_price']) * stock['quantity']
    profit_rate = (stock['current_price'] - stock['buy_price']) / stock['buy_price'] * 100
    
    return {
        'code': code,
        'name': stock['name'],
        'quantity': stock['quantity'],
        'buy_price': stock['buy_price'],
        'current_price': stock['current_price'],
        'profit': round(profit, 2),
        'profit_rate': round(profit_rate, 2)
    }

def generate_report():
    """生成分析报告"""
    stocks = load_stocks()
    if not stocks:
        return None
    
    print(f"\n{'='*70}")
    print(f"{' '*20}股票持仓分析报告")
    print(f"{'='*70}")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*70}")
    print(f"{' '*20}持仓明细")
    print(f"{'='*70}")
    print(f"{'代码':<10} {'名称':<15} {'数量':>6} {'买入价':>10} {'当前价':>10} {'盈亏':>12} {'盈亏率':>10}")
    print(f"{'-'*70}")
    
    total_profit = 0
    total_cost = 0
    total_market = 0
    waiting_count = 0
    
    for code, stock in stocks.items():
        result = calculate_profit(code, stocks)
        
        if result['status'] == 'waiting':
            line = f"{code:<10} {stock['name']:<15} {stock['quantity']:>6} {stock['buy_price']:>10.2f} {'待更新':>10} {'---':>12} {'---':>10}"
            waiting_count += 1
        else:
            profit_str = f"+{result['profit']:.2f}" if result['profit'] > 0 else f"{result['profit']:.2f}"
            profit_rate_str = f"+{result['profit_rate']:.2f}%" if result['profit_rate'] > 0 else f"{result['profit_rate']:.2f}%"
            
            line = f"{code:<10} {result['name']:<15} {result['quantity']:>6} {result['buy_price']:>10.2f} {result['current_price']:>10.2f} {profit_str:>12} {profit_rate_str:>10}"
            
            total_profit += result['profit']
            total_cost += result['buy_price'] * result['quantity']
            total_market += result['current_price'] * result['quantity']
        
        print(line)
    
    print(f"\n{'='*70}")
    print(f"{' '*20}汇总统计")
    print(f"{'='*70}")
    print(f"持仓股票数: {len(stocks)}")
    print(f"待更新股票: {waiting_count}")
    print(f"总成本: {total_cost:.2f} 元")
    print(f"总市值: {total_market:.2f} 元")
    print(f"总盈亏: {total_profit:+.2f} 元")
    
    if total_profit > 0:
        print(f"\n✅ 整体盈利，可以考虑适当止盈")
    elif total_profit < 0:
        print(f"\n⚠️  整体亏损，建议分析原因")
    else:
        print(f"\n➖  整体持平")
    
    print(f"{'='*70}\n")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("股票分析工具 - 使用方法")
        print("")
        print("命令:")
        print("  python3 stock_cli.py report              # 生成分析报告")
        print("  python3 stock_cli.py update <代码> <价格>  # 更新单只股票价格")
        print("")
        print("批量更新:")
        print("  echo '002156 60.50' | python3 stock_cli.py batch")
        print("")
        print("示例:")
        print("  python3 stock_cli.py update 002156 60.50")
        print("  python3 stock_cli.py report")
        return
    
    command = sys.argv[1]
    
    if command == 'report':
        generate_report()
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("用法: python3 stock_cli.py update <代码> <价格>")
            return
        code = sys.argv[2]
        price = sys.argv[3]
        update_price(code, price)
    
    elif command == 'batch':
        # 从标准输入批量更新
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                update_price(parts[0], parts[1])
        print("\n批量更新完成，运行 'python3 stock_cli.py report' 查看报告")
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
