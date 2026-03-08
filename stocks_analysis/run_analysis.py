#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股智能分析器 - 运行脚本
"""
from stock_analyzer import StockAnalyzer, SignalType, Trend
import json

def main():
    analyzer = StockAnalyzer()

    # 添加你的持仓（买入价需要你提供，这里先用0占位）
    print("="*60)
    print("📊 添加持仓信息")
    print("="*60)
    analyzer.add_position("002156", "通富微电", 300, 0.0)  # 300股，买入价待定
    analyzer.add_position("002837", "英维克", 200, 0.0)   # 200股，买入价待定
    analyzer.add_position("002895", "双汇发展", 200, 0.0)  # 200股，买入价待定
    analyzer.add_position("300408", "三环集团", 100, 0.0) # 100股，买入价待定

    print("\n⚠️  请提供以下信息以便准确分析：")
    print("1. 每只股票的买入价格")
    print("2. 当前价格（我会帮你监控）")
    print("\n💬 请用格式告诉我：")
    print("002156 买入价 25.50")
    print("002837 买入价 30.20")
    print("...")

    # 模拟当前价格（实际应该从API获取）
    print("\n" + "="*60)
    print("📈 模拟当前价格（实际会实时更新）")
    print("="*60)

    # 这里是模拟数据，实际应该从API获取
    mock_prices = {
        "002156": {"price": 26.80, "change": 5.1},   # 通富微电
        "002837": {"price": 28.50, "change": -5.6},  # 英维克
        "002895": {"price": 42.30, "change": 1.2},   # 双汇发展
        "300408": {"price": 35.60, "change": 3.8}   # 三环集团
    }

    for code, data in mock_prices.items():
        name = analyzer.positions[code].name if code in analyzer.positions else "未知"
        analyzer.update_stock_data(
            code=code,
            name=name,
            price=data["price"],
            change=data["change"],
            volume=1000000,
            high=data["price"] * 1.05,
            low=data["price"] * 0.95,
            open_price=data["price"] * 0.98,
            previous_close=data["price"] / (1 + data["change"]/100)
        )
        print(f"{name}({code}): {data['price']:.2f} ({data['change']:+.2f}%)")

    # 分析每只股票
    print("\n" + "="*60)
    print("🔍 智能分析结果")
    print("="*60)

    results = []
    for code in analyzer.positions.keys():
        try:
            result = analyzer.analyze_stock(code)
            results.append(result)

            # 生成提醒
            alert = analyzer.generate_alert(result)
            print(f"\n{alert}\n")
        except Exception as e:
            print(f"分析 {code} 失败: {e}")

    # 找出趋势最好的股票
    print("="*60)
    print("🏆 趋势最好的股票")
    print("="*60)
    best_stocks = analyzer.find_best_trending(top_n=2)
    for stock in best_stocks:
        position = analyzer.positions.get(stock.code)
        if position:
            print(f"\n📈 {stock.name}({stock.code})")
            print(f"   当前价: {stock.current_price:.2f} ({stock.change:+.2f}%)")
            print(f"   趋势: {stock.trend.value}")
            print(f"   信号: {stock.signal.value}")
            print(f"   原因: {stock.reason}")

    # 资产汇总（假设买入价）
    print("\n" + "="*60)
    print("💰 资产汇总（假设买入价）")
    print("="*60)

    # 假设的买入价
    assumed_buy_prices = {
        "002156": 25.50,
        "002837": 30.20,
        "002895": 41.00,
        "300408": 34.00
    }

    for code, position in analyzer.positions.items():
        position.buy_price = assumed_buy_prices.get(code, 0.0)
        position.current_price = analyzer.stock_data[code].price

    summary = analyzer.get_portfolio_summary()
    for pos in summary['positions']:
        print(f"{pos['name']}({pos['code']}): "
              f"{pos['shares']}股 买入{pos['buy_price']:.2f} "
              f"当前{pos['current_price']:.2f} "
              f"市值{pos['market_value']:.2f} "
              f"盈亏{pos['profit']:+.2f}({pos['profit_rate']:+.2f}%)")

    print(f"\n总市值: {summary['total_value']:.2f}")
    print(f"总盈亏: {summary['total_profit']:+.2f} ({summary['profit_rate']:+.2f}%)")

    # 保存分析结果
    with open('/root/.openclaw/workspace/stocks_analysis/last_analysis.json', 'w') as f:
        json.dump([{
            'code': r.code,
            'name': r.name,
            'price': r.current_price,
            'change': r.change,
            'signal': r.signal.value,
            'reason': r.reason,
            'trend': r.trend.value
        } for r in results], f, ensure_ascii=False, indent=2)

    print("\n✅ 分析结果已保存到 last_analysis.json")


if __name__ == "__main__":
    main()
