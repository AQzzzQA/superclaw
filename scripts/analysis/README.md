# Analysis Scripts

Stock analysis, market data, and financial research tools.

## Scripts

### Stock Analysis
- **stock_analyzer.py**: Main stock analysis engine with technical indicators
- **stock_cli.py**: Command-line interface for stock analysis
- **baidu_news_search.py**: Baidu news search for market sentiment
- **update_prices.sh**: Shell script to update stock prices
- **stock_data.json**: Stock data storage
- **股票分析工具使用说明.md**: Stock analysis tool documentation (Chinese)

## Usage

### Stock Analysis
```bash
python scripts/analysis/stock_analyzer.py --symbol 600519 --days 30
```

### CLI Interface
```bash
python scripts/analysis/stock_cli.py --help
```

### Update Prices
```bash
bash scripts/analysis/update_prices.sh
```

## Features

- Technical indicators (MA, MACD, RSI, KDJ)
- Real-time stock data fetching
- Market sentiment analysis
- Chinese stock market support

## Requirements

- Python 3.11+
- pandas
- numpy
- requests
- tushare (for Chinese market data)

## Notes

- Stock data is cached in `stock_data.json`
- Analysis focuses on Chinese stock market (A-shares)
- Technical analysis based on common indicators
