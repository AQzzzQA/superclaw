#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取实时股票数据（东方财富API）
"""
import requests
import json
from datetime import datetime

def get_stock_realtime(code: str) -> dict:
    """
    从东方财富获取实时股票数据
    code: 股票代码，如 "002156"
    """
    # 判断是深市还是沪市
    if code.startswith('6'):
        market = 'sh'  # 沪市
    else:
        market = 'sz'  # 深市

    # 东方财富实时行情API
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f45,f47,f48,f60,f162,f116,f117,f164,f163,f167,f168,f255,f256,f257,f258,f127,f122,f124,f125,f126,f115,f161,f161,f164,f169,f170,f171"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('rc') == 0 and data.get('rt') == 0:
            info = data.get('data', {})
            if info:
                return {
                    'code': code,
                    'name': info.get('f58', ''),  # 股票名称
                    'price': info.get('f43', 0.0) / 100,  # 当前价（单位：分）
                    'change': info.get('f170', 0.0) / 100,  # 涨跌额（单位：分）
                    'change_percent': info.get('f169', 0.0) / 100,  # 涨跌幅（单位：%）
                    'open': info.get('f46', 0.0) / 100,  # 开盘价（单位：分）
                    'high': info.get('f44', 0.0) / 100,  # 最高价（单位：分）
                    'low': info.get('f45', 0.0) / 100,  # 最低价（单位：分）
                    'previous_close': info.get('f60', 0.0) / 100,  # 昨收价（单位：分）
                    'volume': info.get('f47', 0),  # 成交量（手）
                    'turnover': info.get('f48', 0),  # 成交额（元）
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

    for pos in positions:
        data = get_stock_realtime(pos['code'])

        if data:
            price = data['price']
            change_percent = data['change_percent']

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
    print(f"总市值: {total_value:.2f}")
    print(f"总成本: {total_cost:.2f}")
    print(f"总盈亏: {total_profit:+.2f} ({(total_profit/total_cost)*100:+.2f}%)")
    print(f"\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
