"""
归因模型服务
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AttributionModel:
    """归因模型基类"""

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """
        归因

        Args:
            conversion: 转化数据
            touchpoints: 触点数据
                [
                    {
                        "touchpoint_id": "string",
                        "channel": "string",
                        "timestamp": "2026-02-27 10:00:00",
                        "cost": 100.0,
                    },
                    ...
                ]

        Returns:
            dict: 归因结果
                {
                    "touchpoint_id": 0.5,
                    ...
                }
        """
        raise NotImplementedError


class LastClickAttribution(AttributionModel):
    """最后点击归因模型"""

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """最后点击归因 - 将 100% 价值分配给最后一次点击"""
        if not touchpoints:
            return {}

        # 按时间排序，获取最后一次点击
        sorted_touchpoints = sorted(
            touchpoints, key=lambda x: x["timestamp"], reverse=True
        )
        last_touchpoint = sorted_touchpoints[0]

        return {last_touchpoint["touchpoint_id"]: 1.0}


class FirstClickAttribution(AttributionModel):
    """首次点击归因模型"""

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """首次点击归因 - 将 100% 价值分配给第一次点击"""
        if not touchpoints:
            return {}

        # 按时间排序，获取第一次点击
        sorted_touchpoints = sorted(touchpoints, key=lambda x: x["timestamp"])
        first_touchpoint = sorted_touchpoints[0]

        return {first_touchpoint["touchpoint_id"]: 1.0}


class LinearAttribution(AttributionModel):
    """线性归因模型"""

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """线性归因 - 将价值平均分配给所有触点"""
        if not touchpoints:
            return {}

        # 平均分配
        attribution_value = 1.0 / len(touchpoints)

        return {
            touchpoint["touchpoint_id"]: attribution_value
            for touchpoint in touchpoints
        }


class TimeDecayAttribution(AttributionModel):
    """时间衰减归因模型"""

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """时间衰减归因 - 越接近转化的触点获得更多价值"""
        if not touchpoints:
            return {}

        # 转化时间
        conversion_time = datetime.strptime(
            conversion["conversion_time"], "%Y-%m-%d %H:%M:%S"
        )

        # 计算每个触点的时间衰减权重
        weights = []
        for touchpoint in touchpoints:
            touchpoint_time = datetime.strptime(
                touchpoint["timestamp"], "%Y-%m-%d %H:%M:%S"
            )
            time_diff = (conversion_time - touchpoint_time).total_seconds() / 3600  # 小时

            # 衰减函数：越接近转化，权重越高
            weight = 1.0 / (1.0 + time_diff / 24.0)  # 24 小时衰减周期
            weights.append(weight)

        # 归一化权重
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # 分配归因
        return {
            touchpoint["touchpoint_id"]: weight
            for touchpoint, weight in zip(touchpoints, normalized_weights)
        }


class PositionBasedAttribution(AttributionModel):
    """位置基础归因模型"""

    def __init__(self, first_ratio: float = 0.4, last_ratio: float = 0.4):
        """
        初始化位置基础归因模型

        Args:
            first_ratio: 首次点击分配比例（默认 40%）
            last_ratio: 最后点击分配比例（默认 40%）
        """
        self.first_ratio = first_ratio
        self.last_ratio = last_ratio
        self.middle_ratio = 1.0 - first_ratio - last_ratio

    def attribute(self, conversion: Dict, touchpoints: List[Dict]) -> Dict[str, float]:
        """位置基础归因 - 首次和最后一次点击获得更多价值"""
        if not touchpoints:
            return {}

        if len(touchpoints) == 1:
            return {touchpoints[0]["touchpoint_id"]: 1.0}

        # 按时间排序
        sorted_touchpoints = sorted(touchpoints, key=lambda x: x["timestamp"])

        # 分配归因
        attribution = {}
        for i, touchpoint in enumerate(sorted_touchpoints):
            if i == 0:
                # 首次点击
                attribution[touchpoint["touchpoint_id"]] = self.first_ratio
            elif i == len(sorted_touchpoints) - 1:
                # 最后一次点击
                attribution[touchpoint["touchpoint_id"]] = self.last_ratio
            else:
                # 中间触点
                attribution[touchpoint["touchpoint_id"]] = self.middle_ratio / (
                    len(sorted_touchpoints) - 2
                )

        return attribution


class AttributionService:
    """归因服务"""

    def __init__(self):
        # 支持的归因模型
        self.models = {
            "last_click": LastClickAttribution(),
            "first_click": FirstClickAttribution(),
            "linear": LinearAttribution(),
            "time_decay": TimeDecayAttribution(),
            "position_based": PositionBasedAttribution(),
        }

    def attribute_conversion(
        self,
        conversion: Dict,
        touchpoints: List[Dict],
        model: str = "time_decay",
    ) -> Dict[str, Any]:
        """
        归因转化

        Args:
            conversion: 转化数据
            touchpoints: 触点数据
            model: 归因模型
                - last_click: 最后点击
                - first_click: 首次点击
                - linear: 线性
                - time_decay: 时间衰减
                - position_based: 位置基础

        Returns:
            dict: 归因结果
        """
        try:
            if model not in self.models:
                raise ValueError(f"不支持的归因模型: {model}")

            attribution_model = self.models[model]
            attribution_result = attribution_model.attribute(conversion, touchpoints)

            # 计算归因价值
            conversion_value = conversion.get("value", 0.0)
            attributed_value = {
                touchpoint_id: attribution_result[touchpoint_id] * conversion_value
                for touchpoint_id in attribution_result
            }

            result = {
                "conversion_id": conversion.get("conversion_id"),
                "model": model,
                "conversion_value": conversion_value,
                "attribution": attribution_result,
                "attributed_value": attributed_value,
                "analyzed_at": datetime.now().isoformat(),
            }

            logger.info(f"归因完成: {conversion.get('conversion_id')}, 模型: {model}")
            return result

        except Exception as e:
            logger.error(f"归因失败: {str(e)}")
            raise

    def batch_attribute_conversions(
        self,
        conversions: List[Dict],
        touchpoints_map: Dict[str, List[Dict]],
        model: str = "time_decay",
    ) -> Dict[str, Any]:
        """
        批量归因转化

        Args:
            conversions: 转化列表
            touchpoints_map: 触点映射
                {
                    "conversion_id_1": [...],
                    "conversion_id_2": [...],
                }
            model: 归因模型

        Returns:
            dict: 批量归因结果
        """
        results = {
            "total": len(conversions),
            "success": 0,
            "failed": 0,
            "errors": [],
        }

        for conversion in conversions:
            conversion_id = conversion.get("conversion_id")
            try:
                touchpoints = touchpoints_map.get(conversion_id, [])
                result = self.attribute_conversion(conversion, touchpoints, model)
                results["success"] += 1
                results.setdefault("attributions", []).append(result)
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {"conversion_id": conversion_id, "error": str(e)}
                )

        logger.info(
            f"批量归因完成: 成功 {results['success']} 个，失败 {results['failed']} 个"
        )
        return results

    def compare_models(
        self, conversion: Dict, touchpoints: List[Dict]
    ) -> Dict[str, Any]:
        """
        比较不同归因模型

        Args:
            conversion: 转化数据
            touchpoints: 触点数据

        Returns:
            dict: 比较结果
        """
        results = {}

        for model_name, model in self.models.items():
            try:
                attribution = model.attribute(conversion, touchpoints)
                results[model_name] = attribution
            except Exception as e:
                logger.error(f"模型 {model_name} 归因失败: {str(e)}")
                results[model_name] = None

        return {
            "conversion_id": conversion.get("conversion_id"),
            "models": results,
            "compared_at": datetime.now().isoformat(),
        }
