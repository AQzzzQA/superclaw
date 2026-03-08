#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询股票代码
"""

STOCK_DB = {
    "002156": "通富微电",
    "002837": "英维克",
    "002895": "双汇发展",
    "300408": "三环集团"
}

codes = ["002156", "002837", "002895", "300408"]

print("股票代码查询结果：")
print("="*50)
for code in codes:
    name = STOCK_DB.get(code, "未知")
    print(f"{code} -> {name}")
