"""
股票分析工具
解决 web_fetch 禁止问题，使用本地文件存储股票数据
"""

from datetime import datetime
from typing import Dict, List, Optional
import json

class StockAnalyzer:
    def __init__(self):
        self.stock_data_file = "/root/.openclaw/workspace/stock_data.json"
        self.load_stock_data()
    
    def load_stock_data(self):
        """加载股票数据"""
        try:
            with open(self.stock_data_file, 'r', encoding='utf-8') as f:
                self.stock_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.stock_data = {}
    
    def save_stock_data(self):
        """保存股票数据"""
        with open(self.stock_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.stock_data, f, ensure_ascii=False, indent=2)
    
    def add_stock(self, code: str, name: str, quantity: int, buy_price: float):
        """添加股票"""
        self.stock_data[code] = {
            'name': name,
            'quantity': quantity,
            'buy_price': buy_price,
            'buy_date': datetime.now().strftime('%Y-%m-%d'),
            'current_price': None,  # 需要手动更新
            'update_time': None
        }
        self.save_stock_data()
    
    def update_price(self, code: str, current_price: float):
        """更新当前价格"""
        if code in self.stock_data:
            self.stock_data[code]['current_price'] = current_price
            self.stock_data[code]['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_stock_data()
            return True
        return False
    
    def calculate_profit(self, code: str) -> Optional[Dict]:
        """计算盈亏"""
        if code not in self.stock_data:
            return None
        
        stock = self.stock_data[code]
        
        if stock['current_price'] is None:
            return {
                'code': code,
                'name': stock['name'],
                'status': 'waiting_for_price',
                'message': '等待更新价格'
            }
        
        buy_price = stock['buy_price']
        current_price = stock['current_price']
        quantity = stock['quantity']
        
        # 计算盈亏
        profit = (current_price - buy_price) * quantity
        profit_rate = (current_price - buy_price) / buy_price * 100
        
        # 计算市值
        market_value = current_price * quantity
        cost_value = buy_price * quantity
        
        return {
            'code': code,
            'name': stock['name'],
            'quantity': quantity,
            'buy_price': buy_price,
            'current_price': current_price,
            'profit': round(profit, 2),
            'profit_rate': round(profit_rate, 2),
            'market_value': round(market_value, 2),
            'cost_value': round(cost_value, 2),
            'update_time': stock.get('update_time', '-')
        }
    
    def analyze_all(self) -> Dict:
        """分析所有持仓"""
        results = {
            'stocks': [],
            'summary': {
                'total_stocks': 0,
                'total_profit': 0,
                'total_cost': 0,
                'total_market_value': 0,
                'average_profit_rate': 0
            }
        }
        
        profit_stocks = 0
        total_profit_rate = 0
        
        for code in self.stock_data.keys():
            result = self.calculate_profit(code)
            results['stocks'].append(result)
            
            if result.get('status') != 'waiting_for_price':
                results['summary']['total_profit'] += result['profit']
                results['summary']['total_cost'] += result['cost_value']
                results['summary']['total_market_value'] += result['market_value']
                
                if result['profit'] > 0:
                    profit_stocks += 1
                total_profit_rate += result['profit_rate']
        
        results['summary']['total_stocks'] = len(self.stock_data)
        
        if len(self.stock_data) > 0:
            results['summary']['average_profit_rate'] = round(total_profit_rate / len(self.stock_data), 2)
        
        return results
    
    def generate_report(self) -> str:
        """生成分析报告"""
        results = self.analyze_all()
        summary = results['summary']
        
        report = f"""
{'='*60}
                    股票持仓分析报告
{'='*60}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
                        持仓明细
{'='*60}

{'代码':<8} {'名称':<20} {'数量':>6} {'买入价':>8} {'当前价':>8} {'盈亏':>10} {'盈亏率':>8}
{'-'*60}
"""
        
        for stock in results['stocks']:
            if stock.get('status') == 'waiting_for_price':
                buy_price_str = f"{stock.get('buy_price', 0):.2f}" if stock.get('buy_price') else '-'
                line = f"{stock['code']:<8} {stock['name']:<20} {stock.get('quantity', 0):>6} {buy_price_str:>8} {'待更新':>8} {'---':>10} {'---':>8}"
            else:
                profit_str = f"+{stock['profit']:.2f}" if stock['profit'] > 0 else f"{stock['profit']:.2f}"
                profit_rate_str = f"+{stock['profit_rate']:.2f}%" if stock['profit_rate'] > 0 else f"{stock['profit_rate']:.2f}%"
                line = f"{stock['code']:<8} {stock['name']:<20} {stock['quantity']:>6} {stock['buy_price']:>8.2f} {stock['current_price']:>8.2f} {profit_str:>10} {profit_rate_str:>8}"
            
            report += line + "\n"
        
        report += f"""
{'='*60}
                        汇总统计
{'='*60}

持仓股票数: {summary['total_stocks']}
总成本: {summary['total_cost']:.2f} 元
总市值: {summary['total_market_value']:.2f} 元
总盈亏: {summary['total_profit']:+.2f} 元
平均盈亏率: {summary['average_profit_rate']:+.2f}%

{'='*60}
                        操作建议
{'='*60}

"""
        
        # 生成操作建议
        if summary['total_profit'] > 0:
            report += "✅ 整体盈利：可以考虑适当止盈，锁定收益\n"
        elif summary['total_profit'] < 0:
            report += "⚠️  整体亏损：建议分析亏损原因，考虑止损\n"
        else:
            report += "➖  整体持平：可以继续持有，关注市场变化\n"
        
        # 个股建议
        profitable_stocks = [s for s in results['stocks'] if s.get('profit', 0) > 0]
        losing_stocks = [s for s in results['stocks'] if s.get('profit', 0) < 0]
        
        if profitable_stocks:
            report += "\n盈利股票:\n"
            for stock in profitable_stocks[:3]:
                report += f"  - {stock['code']} ({stock['name']}): 盈利 {stock['profit']:+.2f} 元 ({stock['profit_rate']:+.2f}%)\n"
        
        if losing_stocks:
            report += "\n亏损股票:\n"
            for stock in losing_stocks[:3]:
                report += f"  - {stock['code']} ({stock['name']}): 亏损 {stock['profit']:+.2f} 元 ({stock['profit_rate']:+.2f}%)\n"
        
        report += f"\n{'='*60}\n"
        
        return report

# 使用示例
if __name__ == "__main__":
    analyzer = StockAnalyzer()
    
    # 添加持仓
    analyzer.add_stock("002156", "通富微电", 300, 54.00)
    analyzer.add_stock("002837", "英维克", 200, 101.70)
    analyzer.add_stock("002895", "世嘉科技", 200, 41.95)
    analyzer.add_stock("300408", "三环集团", 100, 58.96)
    
    # 模拟：用户输入当前价后调用
    # analyzer.update_price("002156", 60.00)
    
    # 生成报告
    print(analyzer.generate_report())
