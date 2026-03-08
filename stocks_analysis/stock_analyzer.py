#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股智能分析器 - 实时监控和智能提醒
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SignalType(Enum):
    """信号类型"""
    BUY = "买入"
    SELL = "卖出"
    HOLD = "持有"
    WATCH = "观望"
    RISK = "风险"


class Trend(Enum):
    """趋势类型"""
    UP = "上升趋势"
    DOWN = "下降趋势"
    SIDEWAYS = "震荡"
    UNKNOWN = "未知"


@dataclass
class StockData:
    """股票数据"""
    code: str
    name: str
    price: float
    change: float  # 涨跌幅 %
    volume: int  # 成交量
    high: float  # 最高价
    low: float  # 最低价
    open_price: float  # 开盘价
    previous_close: float  # 昨收价

    def to_dict(self):
        return asdict(self)


@dataclass
class Position:
    """持仓信息"""
    code: str
    name: str
    shares: int  # 持股数
    buy_price: float  # 买入价
    current_price: float  # 当前价

    @property
    def market_value(self) -> float:
        """市值"""
        return self.shares * self.current_price

    @property
    def profit(self) -> float:
        """盈亏金额"""
        return (self.current_price - self.buy_price) * self.shares

    @property
    def profit_rate(self) -> float:
        """盈亏率"""
        if self.buy_price == 0:
            return 0.0
        return (self.current_price - self.buy_price) / self.buy_price * 100


@dataclass
class TechnicalIndicators:
    """技术指标"""
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma60: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_hist: Optional[float] = None
    kdj_k: Optional[float] = None
    kdj_d: Optional[float] = None
    kdj_j: Optional[float] = None
    rsi: Optional[float] = None


@dataclass
class AnalysisResult:
    """分析结果"""
    code: str
    name: str
    current_price: float
    change: float
    trend: Trend
    signal: SignalType
    reason: str
    risk_level: str  # 低/中/高
    support_price: Optional[float] = None
    resistance_price: Optional[float] = None
    indicators: Optional[TechnicalIndicators] = None


class StockAnalyzer:
    """股票分析器"""

    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.stock_data: Dict[str, StockData] = {}
        self.analysis_history: List[AnalysisResult] = []

    def add_position(self, code: str, name: str, shares: int, buy_price: float):
        """添加持仓"""
        self.positions[code] = Position(
            code=code,
            name=name,
            shares=shares,
            buy_price=buy_price,
            current_price=0.0
        )
        print(f"✅ 已添加持仓: {name}({code}) {shares}股 买入价{buy_price}")

    def update_stock_data(self, code: str, name: str, price: float, change: float,
                         volume: int, high: float, low: float, open_price: float,
                         previous_close: float):
        """更新股票数据"""
        self.stock_data[code] = StockData(
            code=code,
            name=name,
            price=price,
            change=change,
            volume=volume,
            high=high,
            low=low,
            open_price=open_price,
            previous_close=previous_close
        )

        # 更新持仓的当前价
        if code in self.positions:
            self.positions[code].current_price = price

    def analyze_stock(self, code: str) -> AnalysisResult:
        """分析单只股票"""
        if code not in self.stock_data:
            raise ValueError(f"股票 {code} 没有数据")

        stock = self.stock_data[code]

        # 简化分析（实际应该基于历史数据计算技术指标）
        trend = self._determine_trend(stock)
        signal, reason, risk_level = self._generate_signal(stock, trend)
        support, resistance = self._calculate_support_resistance(stock)

        result = AnalysisResult(
            code=code,
            name=stock.name,
            current_price=stock.price,
            change=stock.change,
            trend=trend,
            signal=signal,
            reason=reason,
            risk_level=risk_level,
            support_price=support,
            resistance_price=resistance,
            indicators=TechnicalIndicators()  # 实际应从历史数据计算
        )

        self.analysis_history.append(result)
        return result

    def _determine_trend(self, stock: StockData) -> Trend:
        """判断趋势（简化版，实际应使用MA等指标）"""
        if stock.change > 3:
            return Trend.UP
        elif stock.change < -3:
            return Trend.DOWN
        else:
            return Trend.SIDEWAYS

    def _generate_signal(self, stock: StockData, trend: Trend) -> Tuple[SignalType, str, str]:
        """生成买卖信号"""
        change = stock.change

        if change > 7:
            return SignalType.WATCH, "涨幅过大，追高风险高，建议观望", "高"
        elif change > 5:
            return SignalType.HOLD, "涨幅较大，继续持有，注意止盈", "中"
        elif change > 2:
            return SignalType.HOLD, "上涨趋势良好，继续持有", "低"
        elif change > -2:
            if trend == Trend.UP:
                return SignalType.HOLD, "震荡上升，继续持有", "低"
            else:
                return SignalType.WATCH, "震荡整理，观望为主", "低"
        elif change > -5:
            return SignalType.WATCH, "回调中，关注支撑位，可考虑补仓", "中"
        elif change > -8:
            return SignalType.WATCH, "跌幅较大，谨慎补仓，等待企稳", "高"
        else:
            return SignalType.SELL, "暴跌风险，建议止损或观察", "高"

    def _calculate_support_resistance(self, stock: StockData) -> Tuple[Optional[float], Optional[float]]:
        """计算支撑位和阻力位（简化版）"""
        # 基于当日高低价估算
        mid = (stock.high + stock.low) / 2
        support = stock.low
        resistance = stock.high
        return support, resistance

    def generate_alert(self, result: AnalysisResult) -> str:
        """生成提醒消息"""
        if result.signal == SignalType.SELL:
            return self._format_sell_alert(result)
        elif result.signal == SignalType.BUY:
            return self._format_buy_alert(result)
        elif result.signal == SignalType.HOLD:
            return self._format_hold_alert(result)
        else:
            return self._format_watch_alert(result)

    def _format_sell_alert(self, result: AnalysisResult) -> str:
        """卖出提醒"""
        position = self.positions.get(result.code)
        if position:
            profit = position.profit
            profit_rate = position.profit_rate
            alert = f"""📢 【卖出提醒】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
盈亏：{profit:+.2f} ({profit_rate:+.2f}%)
建议：{result.reason}
风险：{result.risk_level}"""
        else:
            alert = f"""📢 【卖出提醒】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
建议：{result.reason}
风险：{result.risk_level}"""
        return alert

    def _format_buy_alert(self, result: AnalysisResult) -> str:
        """买入提醒"""
        return f"""📢 【买入提醒】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
建议：{result.reason}
支撑位：{result.support_price:.2f}
风险：{result.risk_level}"""

    def _format_hold_alert(self, result: AnalysisResult) -> str:
        """持有提醒"""
        position = self.positions.get(result.code)
        if position:
            profit = position.profit
            profit_rate = position.profit_rate
            alert = f"""📊 【持仓更新】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
盈亏：{profit:+.2f} ({profit_rate:+.2f}%)
趋势：{result.trend.value}
建议：{result.reason}"""
        else:
            alert = f"""📊 【持仓更新】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
趋势：{result.trend.value}
建议：{result.reason}"""
        return alert

    def _format_watch_alert(self, result: AnalysisResult) -> str:
        """观望提醒"""
        return f"""👁️ 【观察提醒】
股票：{result.name}({result.code})
当前价：{result.current_price:.2f} ({result.change:+.2f}%)
趋势：{result.trend.value}
建议：{result.reason}
风险：{result.risk_level}"""

    def get_portfolio_summary(self) -> Dict:
        """获取资产汇总"""
        total_value = 0.0
        total_profit = 0.0
        positions_list = []

        for code, position in self.positions.items():
            total_value += position.market_value
            total_profit += position.profit
            positions_list.append({
                'code': code,
                'name': position.name,
                'shares': position.shares,
                'buy_price': position.buy_price,
                'current_price': position.current_price,
                'market_value': position.market_value,
                'profit': position.profit,
                'profit_rate': position.profit_rate
            })

        return {
            'total_value': total_value,
            'total_profit': total_profit,
            'profit_rate': (total_profit / (total_value - total_profit) * 100) if total_value != total_profit else 0,
            'positions': positions_list
        }

    def find_best_trending(self, top_n: int = 3) -> List[AnalysisResult]:
        """找出趋势最好的股票"""
        # 按涨跌幅排序，取涨幅最大的
        sorted_results = sorted(
            [r for r in self.analysis_history if r.trend == Trend.UP],
            key=lambda x: x.change,
            reverse=True
        )
        return sorted_results[:top_n]


def main():
    """主函数 - 示例用法"""
    analyzer = StockAnalyzer()

    # 添加你的持仓
    analyzer.add_position("002156", "股票名称", 300, 0.0)  # 需要填写名称和买入价
    analyzer.add_position("002837", "股票名称", 200, 0.0)
    analyzer.add_position("002895", "股票名称", 200, 0.0)
    analyzer.add_position("300408", "股票名称", 100, 0.0)

    print("\n" + "="*60)
    print("当前持仓:")
    print("="*60)

    summary = analyzer.get_portfolio_summary()
    for pos in summary['positions']:
        print(f"{pos['name']}({pos['code']}): {pos['shares']}股 "
              f"买入{pos['buy_price']:.2f} 当前{pos['current_price']:.2f} "
              f"市值{pos['market_value']:.2f} 盈亏{pos['profit']:+.2f}({pos['profit_rate']:+.2f}%)")

    print("\n" + "="*60)
    print("资产汇总:")
    print("="*60)
    print(f"总市值: {summary['total_value']:.2f}")
    print(f"总盈亏: {summary['total_profit']:+.2f} ({summary['profit_rate']:+.2f}%)")


if __name__ == "__main__":
    main()
