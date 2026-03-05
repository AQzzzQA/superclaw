"""
自动出价 API
"""
from typing import List, Dict, Any
from fastapi import APIRouter
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
from app.services.auto_bidding import AutoBiddingService

router = APIRouter()
auto_bidding_service = AutoBiddingService()


@router.post("/auto-bidding/update")
async def update_auto_bidding(req: Dict[str, Any]):
    """
    更新单个广告计划的自动出价

    Args:
        req: 请求数据
            {
                "campaign_id": int,
                "historical_data": [
                    {
                        "date": "2026-02-27",
                        "cost": 10000,
                        "revenue": 20000,
                        "bid": 1.5,
                    },
                    ...
                ],
                "current_budget": 10000,
                "current_cost": 5000,
            }
    """
    campaign_id = req.get("campaign_id")
    historical_data = req.get("historical_data", [])
    current_budget = req.get("current_budget")
    current_cost = req.get("current_cost")

    if not campaign_id:
        raise BadRequestException("campaign_id 不能为空")

    if not current_budget:
        raise BadRequestException("current_budget 不能为空")

    result = auto_bidding_service.update_campaign_bid(
        campaign_id, historical_data, current_budget, current_cost
    )

    return APIResponse.success(data=result, message="自动出价更新成功")


@router.post("/auto-bidding/batch-update")
async def batch_update_auto_bidding(req: Dict[str, Any]):
    """
    批量更新自动出价

    Args:
        req: 请求数据
            {
                "campaigns": [
                    {
                        "campaign_id": 1,
                        "historical_data": [...],
                        "current_budget": 10000,
                        "current_cost": 5000,
                    },
                    ...
                ]
            }
    """
    campaigns = req.get("campaigns", [])

    if not campaigns:
        raise BadRequestException("campaigns 不能为空")

    result = auto_bidding_service.batch_update_bids(campaigns)

    return APIResponse.success(
        data=result,
        message=f"批量更新完成：成功 {result['success']} 个，失败 {result['failed']} 个"
    )
