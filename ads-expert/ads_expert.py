"""
广告优化专家 - 子代理实现
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from subagent_orchestrator import SubagentTask, AgentRole, CollaborationMode
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class AdsOptimizationExpert:
    """广告优化专家子代理"""

    def __init__(self):
        """初始化广告优化专家"""
        self.name = "广告优化专家"
        self.role = "ADS_OPTIMIZATION_EXPERT"  # 使用字符串而非枚举
        self.capabilities = [
            "数据分析",
            "自动投放",
            "智能优化",
            "A/B 测试",
            "风险控制"
        ]

    def optimize_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """优化广告计划"""
        logger.info(f"{self.name}: 开始优化广告计划")

        # 1. 计算 ROI
        impressions = campaign_data.get('impressions', 0)
        clicks = campaign_data.get('clicks', 0)
        conversions = campaign_data.get('conversions', 0)
        cost = campaign_data.get('cost', 0.0)

        # 计算 CTR
        ctr = (clicks / impressions * 100) if impressions > 0 else 0

        # 计算 CPC
        cpc = (cost / clicks) if clicks > 0 else 0

        # 计算 CPA
        cpa = (cost / conversions) if conversions > 0 else 0

        # 计算 ROI
        roi = (conversions * 50 / cost) if cost > 0 else 0  # 假设每转化价值 50 元

        # 2. 根据 ROI 决策
        if roi > 3.0:
            decision = "increase_bid"
            new_bid = campaign_data.get('bid', 1.0) * 1.2
            reason = f"ROI 高（{roi:.2f}），提高出价 20%"
        elif roi > 2.0:
            decision = "increase_bid"
            new_bid = campaign_data.get('bid', 1.0) * 1.1
            reason = f"ROI 良好（{roi:.2f}），提高出价 10%"
        elif roi > 1.5:
            decision = "maintain_bid"
            new_bid = campaign_data.get('bid', 1.0)
            reason = f"ROI 正常（{roi:.2f}），保持出价"
        elif roi > 1.0:
            decision = "maintain_bid"
            new_bid = campaign_data.get('bid', 1.0)
            reason = f"ROI 及格（{roi:.2f}），保持出价"
        else:
            decision = "decrease_bid"
            new_bid = campaign_data.get('bid', 1.0) * 0.8
            reason = f"ROI 低（{roi:.2f}），降低出价 20%"

        result = {
            "expert": self.name,
            "decision": decision,
            "old_bid": campaign_data.get('bid', 1.0),
            "new_bid": new_bid,
            "reason": reason,
            "metrics": {
                "ctr": f"{ctr:.2f}%",
                "cpc": f"{cpc:.2f}",
                "cpa": f"{cpa:.2f}",
                "roi": f"{roi:.2f}"
            },
            "confidence": 0.85
        }

        logger.info(f"{self.name}: 优化决策 - {decision}")
        logger.info(f"{self.name}: 优化原因 - {reason}")

        return result

    def rank_creatives(self, creatives_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """排序创意"""
        logger.info(f"{self.name}: 开始排序创意")

        # 1. 计算每个创意的得分
        for creative in creatives_data:
            # CTR 得分（0-40 分）
            ctr_score = min(creative.get('ctr', 0) * 1000, 40)

            # 转化率得分（0-30 分）
            conversion_rate = creative.get('conversion_rate', 0)
            conversion_score = min(conversion_rate * 1000, 30)

            # ROI 得分（0-30 分）
            roi_score = min(creative.get('roi', 0) * 10, 30)

            # 总得分
            creative['total_score'] = ctr_score + conversion_score + roi_score

        # 2. 按总得分降序排序
        ranked_creatives = sorted(creatives_data, key=lambda x: x['total_score'], reverse=True)

        # 3. 生成优化建议
        recommendations = []
        for i, creative in enumerate(ranked_creatives):
            if creative['total_score'] < 50:
                # 得分低，建议暂停
                recommendations.append({
                    "action": "pause",
                    "creative_id": creative['id'],
                    "reason": f"得分太低（{creative['total_score']}），建议暂停"
                })
            elif i < len(ranked_creatives) / 2:
                # 前 50%，建议加大预算
                recommendations.append({
                    "action": "increase_budget",
                    "creative_id": creative['id'],
                    "reason": f"表现优秀（得分 {creative['total_score']}），建议加大预算"
                })
            else:
                # 后 50%，建议保持
                recommendations.append({
                    "action": "maintain",
                    "creative_id": creative['id'],
                    "reason": f"表现一般（得分 {creative['total_score']}），建议保持"
                })

        result = {
            "expert": self.name,
            "ranked_creatives": ranked_creatives,
            "recommendations": recommendations,
            "confidence": 0.85
        }

        logger.info(f"{self.name}: 创意排序完成，共 {len(ranked_creatives)} 个创意")

        return result

    def segment_audience(self, audience_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分层定向人群"""
        logger.info(f"{self.name}: 开始分层定向人群")

        # 1. 根据表现分层
        high_performance = []
        medium_performance = []
        low_performance = []

        for audience in audience_data:
            roi = audience.get('roi', 0)

            if roi > 2.5:
                high_performance.append(audience)
            elif roi > 1.5:
                medium_performance.append(audience)
            else:
                low_performance.append(audience)

        # 2. 生成优化建议
        recommendations = []

        # 高性能人群建议加大预算
        for audience in high_performance:
            recommendations.append({
                "action": "increase_budget",
                "audience_id": audience['id'],
                "reason": f"ROI 高（{audience['roi']}），建议加大预算"
            })

        # 低性能人群建议暂停
        for audience in low_performance:
            recommendations.append({
                "action": "pause",
                "audience_id": audience['id'],
                "reason": f"ROI 低（{audience['roi']}），建议暂停"
            })

        # 中性能人群建议优化
        for audience in medium_performance:
            recommendations.append({
                "action": "optimize",
                "audience_id": audience['id'],
                "reason": f"ROI 中等（{audience['roi']}），建议优化"
            })

        result = {
            "expert": self.name,
            "segments": {
                "high_performance": high_performance,
                "medium_performance": medium_performance,
                "low_performance": low_performance
            },
            "recommendations": recommendations,
            "confidence": 0.85
        }

        logger.info(f"{self.name}: 人群分层完成 - 高性能 {len(high_performance)}，中性能 {len(medium_performance)}，低性能 {len(low_performance)}")

        return result

    def check_risks(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查风险"""
        logger.info(f"{self.name}: 开始检查风险")

        risks = []

        # 1. 检查 ROI 风险
        roi = campaign_data.get('roi', 0)
        if roi < 1.0:
            risks.append({
                "type": "low_roi",
                "severity": "high",
                "description": f"ROI 低（{roi:.2f}），低于目标 1.5",
                "recommendation": "建议降低出价或优化定向"
            })

        # 2. 检查预算风险
        budget_remaining = campaign_data.get('budget_remaining', 0)
        budget_total = campaign_data.get('budget_total', 0)
        if budget_remaining < budget_total * 0.1:
            risks.append({
                "type": "budget_low",
                "severity": "high",
                "description": f"预算剩余不足（{budget_remaining:.2f} / {budget_total:.2f}）",
                "recommendation": "建议暂停低效广告，释放预算"
            })

        # 3. 检查 CTR 异常
        ctr = campaign_data.get('ctr', 0)
        if ctr < 1.0:
            risks.append({
                "type": "low_ctr",
                "severity": "medium",
                "description": f"CTR 低（{ctr:.2f}%），低于行业平均 2-3%",
                "recommendation": "建议优化创意或定向"
            })

        result = {
            "expert": self.name,
            "risks": risks,
            "risk_count": len(risks),
            "recommendation": "建议优先处理高风险项目",
            "confidence": 0.85
        }

        logger.info(f"{self.name}: 风险检查完成，发现 {len(risks)} 个风险")

        return result


# 导出类
__all__ = ['AdsOptimizationExpert']
