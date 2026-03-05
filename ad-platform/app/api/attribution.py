"""
归因模型 API
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Query
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
from app.services.attribution import AttributionService

router = APIRouter()
attribution_service = AttributionService()


@router.post("/attribution/attribute")
async def attribute_conversion(req: Dict[str, Any]):
    """
    归因转化

    Args:
        req: 请求数据
            {
                "conversion": {
                    "conversion_id": "string",
                    "conversion_time": "2026-02-27 10:00:00",
                    "value": 100.0,
                },
                "touchpoints": [
                    {
                        "touchpoint_id": "string",
                        "channel": "string",
                        "timestamp": "2026-02-27 09:00:00",
                        "cost": 100.0,
                    },
                    ...
                ],
                "model": "time_decay",  # last_click | first_click | linear | time_decay | position_based
            }
    """
    result = attribution_service.attribute_conversion(
        conversion=req.get("conversion", {}),
        touchpoints=req.get("touchpoints", []),
        model=req.get("model", "time_decay"),
    )

    return APIResponse.success(data=result, message="归因完成")


@router.post("/attribution/batch-attribute")
async def batch_attribute_conversions(req: Dict[str, Any]):
    """
    批量归因转化

    Args:
        req: 请求数据
            {
                "conversions": [...],
                "touchpoints_map": {
                    "conversion_id_1": [...],
                    "conversion_id_2": [...],
                },
                "model": "time_decay",
            }
    """
    result = attribution_service.batch_attribute_conversions(
        conversions=req.get("conversions", []),
        touchpoints_map=req.get("touchpoints_map", {}),
        model=req.get("model", "time_decay"),
    )

    return APIResponse.success(
        data=result,
        message=f"批量归因完成：成功 {result['success']} 个，失败 {result['failed']} 个"
    )


@router.post("/attribution/compare")
async def compare_attribution_models(req: Dict[str, Any]):
    """
    比较不同归因模型

    Args:
        req: 请求数据
            {
                "conversion": {
                    "conversion_id": "string",
                    "conversion_time": "2026-02-27 10:00:00",
                    "value": 100.0,
                },
                "touchpoints": [...],
            }
    """
    result = attribution_service.compare_models(
        conversion=req.get("conversion", {}),
        touchpoints=req.get("touchpoints", []),
    )

    return APIResponse.success(data=result, message="模型比较完成")


@router.get("/attribution/models")
async def list_attribution_models():
    """
    列出所有支持的归因模型
    """
    models = [
        {
            "name": "last_click",
            "description": "最后点击归因 - 将 100% 价值分配给最后一次点击",
        },
        {
            "name": "first_click",
            "description": "首次点击归因 - 将 100% 价值分配给第一次点击",
        },
        {
            "name": "linear",
            "description": "线性归因 - 将价值平均分配给所有触点",
        },
        {
            "name": "time_decay",
            "description": "时间衰减归因 - 越接近转化的触点获得更多价值",
        },
        {
            "name": "position_based",
            "description": "位置基础归因 - 首次和最后一次点击获得更多价值（各 40%，中间触点 20%）",
        },
    ]

    return APIResponse.success(data={"models": models})
