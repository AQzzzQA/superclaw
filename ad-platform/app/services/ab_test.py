"""
A/B 测试服务
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import uuid
import json

logger = logging.getLogger(__name__)


class ABTestService:
    """A/B 测试服务"""

    def __init__(self):
        # 模拟数据库存储
        self.tests: Dict[str, Dict] = {}

    def create_ab_test(
        self,
        name: str,
        description: str,
        test_type: str,
        variants: List[Dict],
        duration_days: int = 7,
        sample_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        创建 A/B 测试

        Args:
            name: 测试名称
            description: 测试描述
            test_type: 测试类型 (bid | creative | targeting)
            variants: 变体列表
                [
                    {
                        "name": "变体 A",
                        "config": {...},
                    },
                    {
                        "name": "变体 B",
                        "config": {...},
                    },
                ]
            duration_days: 测试持续天数
            sample_size: 样本大小（可选）

        Returns:
            dict: 创建结果
        """
        try:
            test_id = str(uuid.uuid4())

            # 验证变体
            if len(variants) < 2:
                raise ValueError("至少需要 2 个变体")

            # 创建测试
            test = {
                "test_id": test_id,
                "name": name,
                "description": description,
                "test_type": test_type,
                "variants": variants,
                "duration_days": duration_days,
                "sample_size": sample_size,
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "traffic_allocation": self._allocate_traffic(variants),
                "results": None,
                "created_at": datetime.now().isoformat(),
            }

            self.tests[test_id] = test
            logger.info(f"创建 A/B 测试: {name} ({test_id})")

            return {
                "test_id": test_id,
                "status": "success",
                "message": "A/B 测试创建成功",
                "test": test,
            }

        except Exception as e:
            logger.error(f"创建 A/B 测试失败: {str(e)}")
            raise

    def start_ab_test(self, test_id: str) -> Dict[str, Any]:
        """
        启动 A/B 测试

        Args:
            test_id: 测试 ID

        Returns:
            dict: 启动结果
        """
        try:
            if test_id not in self.tests:
                raise ValueError("测试不存在")

            test = self.tests[test_id]

            if test["status"] != "pending":
                raise ValueError("测试状态不正确，只能启动 pending 状态的测试")

            # 更新测试状态
            test["status"] = "running"
            test["start_time"] = datetime.now().isoformat()
            test["end_time"] = (
                datetime.now() + timedelta(days=test["duration_days"])
            ).isoformat()

            logger.info(f"启动 A/B 测试: {test_id}")
            return {
                "test_id": test_id,
                "status": "success",
                "message": "A/B 测试已启动",
            }

        except Exception as e:
            logger.error(f"启动 A/B 测试失败: {str(e)}")
            raise

    def stop_ab_test(self, test_id: str) -> Dict[str, Any]:
        """
        停止 A/B 测试

        Args:
            test_id: 测试 ID

        Returns:
            dict: 停止结果
        """
        try:
            if test_id not in self.tests:
                raise ValueError("测试不存在")

            test = self.tests[test_id]

            if test["status"] != "running":
                raise ValueError("测试状态不正确，只能停止 running 状态的测试")

            # 更新测试状态
            test["status"] = "stopped"
            test["end_time"] = datetime.now().isoformat()

            logger.info(f"停止 A/B 测试: {test_id}")
            return {
                "test_id": test_id,
                "status": "success",
                "message": "A/B 测试已停止",
            }

        except Exception as e:
            logger.error(f"停止 A/B 测试失败: {str(e)}")
            raise

    def analyze_ab_test(self, test_id: str) -> Dict[str, Any]:
        """
        分析 A/B 测试结果

        Args:
            test_id: 测试 ID

        Returns:
            dict: 分析结果
        """
        try:
            if test_id not in self.tests:
                raise ValueError("测试不存在")

            test = self.tests[test_id]

            # 模拟分析结果
            analysis_result = {
                "test_id": test_id,
                "winner": test["variants"][0]["name"],
                "confidence": 0.95,
                "improvement": 15.5,
                "significance": True,
                "variants": [
                    {
                        "name": variant["name"],
                        "conversions": 100 + hash(variant["name"]) % 50,
                        "impressions": 1000 + hash(variant["name"]) % 500,
                        "ctr": (2.0 + hash(variant["name"]) % 100 / 100),
                        "conversion_rate": (10.0 + hash(variant["name"]) % 50 / 10),
                    }
                    for variant in test["variants"]
                ],
                "recommendation": "建议采用变体 A",
                "analyzed_at": datetime.now().isoformat(),
            }

            # 更新测试结果
            test["results"] = analysis_result

            logger.info(f"分析 A/B 测试: {test_id}")
            return analysis_result

        except Exception as e:
            logger.error(f"分析 A/B 测试失败: {str(e)}")
            raise

    def get_ab_test(self, test_id: str) -> Dict[str, Any]:
        """
        获取 A/B 测试详情

        Args:
            test_id: 测试 ID

        Returns:
            dict: 测试详情
        """
        if test_id not in self.tests:
            raise ValueError("测试不存在")

        return self.tests[test_id]

    def list_ab_tests(self, status: Optional[str] = None) -> List[Dict]:
        """
        列出所有 A/B 测试

        Args:
            status: 状态过滤 (pending | running | stopped | completed)

        Returns:
            list: 测试列表
        """
        tests = list(self.tests.values())

        if status:
            tests = [t for t in tests if t["status"] == status]

        return tests

    def _allocate_traffic(self, variants: List[Dict]) -> Dict[str, float]:
        """
        分配流量

        Args:
            variants: 变体列表

        Returns:
            dict: 流量分配
                {
                    "variant_1": 0.5,
                    "variant_2": 0.5,
                }
        """
        # 平均分配流量
        allocation = 1.0 / len(variants)

        return {variant["name"]: allocation for variant in variants}
