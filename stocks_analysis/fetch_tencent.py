#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取实时股票数据（腾讯财经API）
"""
import requests
import json
from datetime import datetime

def get_stock_realtime(code: str) -> dict:
    """
    从腾讯财经获取实时股票数据
    code: 股票代码，如 "002156"
    """
    # 腾讯财经API格式：sh600519, sz000002
    if code.startswith('6'):
        market = 'sh'
    else:
        market = 'sz'

    url = f"https://qt.gtimg.cn/q={market}{code}"

    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'gbk'
        text = response.text.strip()

        # 解析腾讯返回的数据格式
        # v_sh600519="1~贵州茅台~..."
        if text.startswith(f'v_{market}{code}="') and text.endswith('";'):
            data_str = text[len(f'v_{market}{code}="'):-2]
            fields = data_str.split('~')

            if len(fields) > 40:
                return {
                    'code': code,
                    'name': fields[1],  # 股票名称
                    'price': float(fields[3]),  # 当前价
                    'previous_close': float(fields[4]),  # 昨收价
                    'open': float(fields[5]),  # 开盘价
                    'high': float(fields[33]),  # 最高价
                    'low': float(fields[34]),  # 最低价
                    'volume': int(fields[6]),  # 成交量（手）
                    'turnover': float(fields[37]),  # 成交额
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        return None
    except Exception as e:
        print(f"获取 {code} 数据失败: {e}")
        return None


def main():
    """主函数"""
    # 你的持仓
    positions = [
        {"code": "002156", "name": "通富微电", "shares": 300, "buy_price": 54.0},
        {"code": "002837", "name": "英维克", "shares": 200, "buy_price": 101.7},
        {"code": "002895", "name": "双汇发展", "shares": 200, "buy_price": 41.95},
        {"code": "300408", "name": "三环集团", "shares": 100, "buy_price": 58.96},
    ]

    print("="*80)
    print("📊 实时股票行情")
    print("="*80)

    total_value = 0.0
    total_profit = 0.0
    total_cost = 0.0
    success_count = 0

    for pos in positions:
        data = get_stock_realtime(pos['code'])

        if data:
            success_count += 1
            price = data['price']
            previous_close = data['previous_close']
            change = price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close > 0 else 0

            # 计算盈亏
            market_value = price * pos['shares']
            cost = pos['buy_price'] * pos['shares']
            profit = market_value - cost
            profit_rate = (price - pos['buy_price']) / pos['buy_price'] * 100

            total_value += market_value
            total_profit += profit
            total_cost += cost

            # 判断趋势和信号
            if change_percent > 5:
                trend = "📈 强势上涨"
                signal = "⚠️  注意高位风险"
            elif change_percent > 2:
                trend = "📈 上涨"
                signal = "✅ 持有"
            elif change_percent > -2:
                trend = "➡️ 震荡"
                signal = "⏳ 观望"
            elif change_percent > -5:
                trend = "📉 回调"
                signal = "⏳ 观望/补仓"
            else:
                trend = "📉 下跌"
                signal = "⚠️  止损风险"

            print(f"\n{pos['name']} ({pos['code']})")
            print(f"  当前价: {price:.2f} ({change_percent:+.2f}%)")
            print(f"  开盘/最高/最低: {data['open']:.2f} / {data['high']:.2f} / {data['low']:.2f}")
            print(f"  持仓: {pos['shares']}股 买入{pos['buy_price']:.2f}")
            print(f"  市值: {market_value:.2f} 盈亏: {profit:+.2f} ({profit_rate:+.2f}%)")
            print(f"  趋势: {trend}")
            print(f"  建议: {signal}")

        else:
            print(f"\n❌ {pos['name']} ({pos['code']}) 数据获取失败")

    print("\n" + "="*80)
    print("💰 资产汇总")
    print("="*80)
    if success_count > 0:
        print(f"总市值: {total_value:.2f}")
        print(f"总成本: {total_cost:.2f}")
        print(f"总盈亏: {total_profit:+.2f} ({(total_profit/total_cost)*100:+.2f}%)")
    else:
        print("❌ 所有股票数据获取失败，可能是休市时间或网络问题")

    print(f"\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
