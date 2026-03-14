"""
数据导出 API
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
import pandas as pd
import io
from datetime import datetime

router = APIRouter()


@router.get("/report/export")
async def export_report(
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="结束日期 YYYY-MM-DD"),
    format: str = Query("xlsx", description="导出格式: xlsx | csv"),
):
    """导出报表数据"""
    try:
        # 验证日期格式
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise BadRequestException("日期格式错误，请使用 YYYY-MM-DD")

    if format not in ["xlsx", "csv"]:
        raise BadRequestException("格式错误，支持 xlsx 或 csv")

    # 模拟数据（实际应从数据库查询）
    data = [
        {
            "date": "2026-02-27",
            "cost": 10000,
            "show": 50000,
            "click": 1000,
            "ctr": 2.0,
            "convert": 50,
        },
        {
            "date": "2026-02-26",
            "cost": 12000,
            "show": 60000,
            "click": 1200,
            "ctr": 2.0,
            "convert": 60,
        },
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 导出
    output = io.BytesIO()

    if format == "xlsx":
        df.to_excel(output, index=False, engine="openpyxl")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"report_{start_date}_{end_date}.xlsx"
    else:
        df.to_csv(output, index=False)
        mime_type = "text/csv"
        filename = f"report_{start_date}_{end_date}.csv"

    output.seek(0)

    from fastapi.responses import Response

    return Response(
        content=output.getvalue(),
        media_type=mime_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
