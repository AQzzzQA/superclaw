"""
A/B 测试 API
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
from app.services.ab_test import ABTestService

router = APIRouter()
ab_test_service = ABTestService()


@router.post("/ab-test/create")
async def create_ab_test(req: Dict[str, Any]):
    """
    创建 A/B 测试

    Args:
        req: 请求数据
            {
                "name": "测试名称",
                "description": "测试描述",
                "test_type": "bid | creative | targeting",
                "variants": [
                    {
                        "name": "变体 A",
                        "config": {...},
                    },
                    ...
                ],
                "duration_days": 7,
                "sample_size": 10000,
            }
    """
    result = ab_test_service.create_ab_test(
        name=req.get("name"),
        description=req.get("description"),
        test_type=req.get("test_type"),
        variants=req.get("variants", []),
        duration_days=req.get("duration_days", 7),
        sample_size=req.get("sample_size"),
    )

    return APIResponse.success(data=result, message="A/B 测试创建成功")


@router.post("/ab-test/{test_id}/start")
async def start_ab_test(test_id: str):
    """
    启动 A/B 测试

    Args:
        test_id: 测试 ID
    """
    result = ab_test_service.start_ab_test(test_id)
    return APIResponse.success(data=result, message="A/B 测试已启动")


@router.post("/ab-test/{test_id}/stop")
async def stop_ab_test(test_id: str):
    """
    停止 A/B 测试

    Args:
        test_id: 测试 ID
    """
    result = ab_test_service.stop_ab_test(test_id)
    return APIResponse.success(data=result, message="A/B 测试已停止")


@router.post("/ab-test/{test_id}/analyze")
async def analyze_ab_test(test_id: str):
    """
    分析 A/B 测试结果

    Args:
        test_id: 测试 ID
    """
    result = ab_test_service.analyze_ab_test(test_id)
    return APIResponse.success(data=result, message="分析完成")


@router.get("/ab-test/{test_id}")
async def get_ab_test(test_id: str):
    """
    获取 A/B 测试详情

    Args:
        test_id: 测试 ID
    """
    result = ab_test_service.get_ab_test(test_id)
    return APIResponse.success(data=result)


@router.get("/ab-test")
async def list_ab_tests(status: Optional[str] = Query(None)):
    """
    列出所有 A/B 测试

    Args:
        status: 状态过滤 (pending | running | stopped | completed)
    """
    results = ab_test_service.list_ab_tests(status)
    return APIResponse.success(data={"tests": results, "total": len(results)})
