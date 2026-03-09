#!/usr/bin/env python3
"""
我的股票监控列表
"""

WATCHLIST = [
    # ===== 大敖的持仓 =====
    {
        "code": "002156",
        "name": "通富微电",
        "market": "sz",
        "type": "individual",
        "cost": 54.00,
        "quantity": 300,
        "alerts": {
            "cost_pct_above": 10.0,    # 盈利10%提醒
            "cost_pct_below": -10.0,   # 亏损10%提醒
            "change_pct_above": 4.0,    # 日内异动 ±4%
            "change_pct_below": -4.0,
            "volume_surge": 2.0
        }
    },
    {
        "code": "002837",
        "name": "英维克",
        "market": "sz",
        "type": "individual",
        "cost": 101.70,
        "quantity": 200,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -10.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0
        }
    },
    {
        "code": "002895",
        "name": "世嘉科技",
        "market": "sz",
        "type": "individual",
        "cost": 41.95,
        "quantity": 200,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -10.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0
        }
    },
    {
        "code": "300408",
        "name": "三环集团",
        "market": "sz",
        "type": "individual",
        "cost": 58.96,
        "quantity": 100,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -10.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0
        }
    },
]
