#!/usr/bin/env python3
"""
性能监控系统
跟踪智能体性能指标并提供优化建议
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum


class MetricType(Enum):
    """指标类型"""
    TASK_COMPLETION = "task_completion"
    SUCCESS_RATE = "success_rate"
    AVG_DURATION = "avg_duration"
    COLLABORATION_SUCCESS = "collaboration_success"


@dataclass
class PerformanceMetric:
    """性能指标"""
    agent_id: str
    metric_type: MetricType
    value: float
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        """转换为字典"""
        return asdict(self)


@dataclass
class AgentPerformance:
    """智能体性能"""
    agent_id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    success_rate: float = 1.0
    avg_duration: float = 0.0
    total_duration: float = 0.0
    total_collaborations: int = 0
    successful_collaborations: int = 0
    collaboration_success_rate: float = 1.0
    last_active: str = ""
    history: List[PerformanceMetric] = field(default_factory=list)

    def add_task(self, duration: float, success: bool):
        """添加任务记录"""
        self.total_tasks += 1

        if success:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1

        # 更新成功率
        self.success_rate = self.completed_tasks / self.total_tasks

        # 更新平均时长
        self.total_duration += duration
        self.avg_duration = self.total_duration / self.completed_tasks if self.completed_tasks > 0 else 0

        # 记录历史
        self.history.append(PerformanceMetric(
            agent_id=self.agent_id,
            metric_type=MetricType.TASK_COMPLETION,
            value=duration,
            metadata={'success': success}
        ))

        # 更新最后活跃时间
        self.last_active = datetime.now().isoformat()

    def add_collaboration(self, success: bool):
        """添加协作记录"""
        self.total_collaborations += 1

        if success:
            self.successful_collaborations += 1

        # 更新协作成功率
        self.collaboration_success_rate = (
            self.successful_collaborations / self.total_collaborations
            if self.total_collaborations > 0 else 1.0
        )

        # 记录历史
        self.history.append(PerformanceMetric(
            agent_id=self.agent_id,
            metric_type=MetricType.COLLABORATION_SUCCESS,
            value=1.0 if success else 0.0
        ))

    def get_score(self) -> float:
        """计算综合评分 (0.0 - 1.0)"""
        # 成功率权重 50%
        score = self.success_rate * 0.5

        # 协作成功率权重 30%
        score += self.collaboration_success_rate * 0.3

        # 效率权重 20%（假设目标时长为5分钟）
        efficiency = min(5.0 / max(self.avg_duration, 1.0), 1.0)
        score += efficiency * 0.2

        return round(score, 3)

    def to_dict(self):
        """转换为字典"""
        data = asdict(self)
        data['score'] = self.get_score()
        return data


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.agents: Dict[str, AgentPerformance] = {}
        self.global_metrics: List[PerformanceMetric] = []

    def get_or_create_performance(self, agent_id: str) -> AgentPerformance:
        """获取或创建性能记录"""
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentPerformance(agent_id=agent_id)

        return self.agents[agent_id]

    def track_task(self, agent_id: str, duration: float, success: bool):
        """跟踪任务"""
        perf = self.get_or_create_performance(agent_id)
        perf.add_task(duration, success)

        # 记录全局指标
        self.global_metrics.append(PerformanceMetric(
            agent_id=agent_id,
            metric_type=MetricType.TASK_COMPLETION,
            value=duration,
            metadata={'success': success}
        ))

    def track_collaboration(self, agent_id: str, success: bool):
        """跟踪协作"""
        perf = self.get_or_create_performance(agent_id)
        perf.add_collaboration(success)

        # 记录全局指标
        self.global_metrics.append(PerformanceMetric(
            agent_id=agent_id,
            metric_type=MetricType.COLLABORATION_SUCCESS,
            value=1.0 if success else 0.0
        ))

    def get_top_performers(self, n: int = 5) -> List[Tuple[str, float]]:
        """获取最佳表现者"""
        scores = [(agent_id, perf.get_score()) for agent_id, perf in self.agents.items()]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def get_agent_performance(self, agent_id: str) -> Optional[AgentPerformance]:
        """获取智能体性能"""
        return self.agents.get(agent_id)

    def get_worst_performers(self, n: int = 5) -> List[Tuple[str, float]]:
        """获取最差表现者"""
        scores = [(agent_id, perf.get_score()) for agent_id, perf in self.agents.items()]
        scores.sort(key=lambda x: x[1])
        return scores[:n]

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.agents:
            return {}

        total_tasks = sum(p.total_tasks for p in self.agents.values())
        total_completed = sum(p.completed_tasks for p in self.agents.values())
        total_failed = sum(p.failed_tasks for p in self.agents.values())
        total_duration = sum(p.total_duration for p in self.agents.values())

        return {
            'total_agents': len(self.agents),
            'total_tasks': total_tasks,
            'completed_tasks': total_completed,
            'failed_tasks': total_failed,
            'success_rate': total_completed / total_tasks if total_tasks > 0 else 0,
            'avg_duration': total_duration / total_completed if total_completed > 0 else 0,
            'top_performers': self.get_top_performers(3),
            'worst_performers': self.get_worst_performers(3)
        }


class SelfOptimizer:
    """自我优化器"""

    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.recommendations: List[Dict[str, Any]] = []

    def analyze_agent(self, agent_id: str) -> List[str]:
        """分析智能体并提供优化建议"""
        perf = self.monitor.get_agent_performance(agent_id)
        if not perf:
            return []

        suggestions = []

        # 检查成功率
        if perf.success_rate < 0.8:
            suggestions.append(f"⚠️ 成功率较低 ({perf.success_rate*100:.1f}%)，建议增加测试用例")
        elif perf.success_rate < 0.9:
            suggestions.append(f"📊 成功率一般 ({perf.success_rate*100:.1f}%)，可优化错误处理")

        # 检查平均时长
        if perf.avg_duration > 10:
            suggestions.append(f"⏱️ 平均时长较长 ({perf.avg_duration:.1f}分钟)，建议优化代码性能")
        elif perf.avg_duration > 5:
            suggestions.append(f"⚡ 平均时长可优化 ({perf.avg_duration:.1f}分钟)")

        # 检查协作成功率
        if perf.collaboration_success_rate < 0.7:
            suggestions.append(f"🤝 协作成功率较低 ({perf.collaboration_success_rate*100:.1f}%)，建议提升沟通能力")

        # 检查任务数量
        if perf.total_tasks < 10:
            suggestions.append("📈 任务经验不足，建议增加更多实践")

        return suggestions

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """生成全局优化建议"""
        self.recommendations = []
        stats = self.monitor.get_statistics()

        # 全局建议
        if stats.get('success_rate', 0) < 0.85:
            self.recommendations.append({
                'type': 'global',
                'level': 'high',
                'message': '整体成功率偏低，建议加强测试和质量控制'
            })

        if stats.get('avg_duration', 0) > 5:
            self.recommendations.append({
                'type': 'global',
                'level': 'medium',
                'message': f'平均任务时长 {stats["avg_duration"]:.1f} 分钟，建议优化流程'
            })

        # 针对性建议
        for agent_id in self.monitor.agents:
            suggestions = self.analyze_agent(agent_id)
            for suggestion in suggestions:
                self.recommendations.append({
                    'type': 'agent',
                    'agent_id': agent_id,
                    'message': suggestion
                })

        return self.recommendations

    def get_optimization_report(self) -> Dict[str, Any]:
        """获取优化报告"""
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.monitor.get_statistics(),
            'recommendations': self.generate_recommendations(),
            'top_performers': self.monitor.get_top_performers(3),
            'worst_performers': self.monitor.get_worst_performers(3)
        }


# 初始化全局监控器
performance_monitor = PerformanceMonitor()
self_optimizer = SelfOptimizer(performance_monitor)


def seed_sample_data(monitor: PerformanceMonitor):
    """初始化样本数据"""

    # Code-Reviewer
    perf = monitor.get_or_create_performance("code-reviewer")
    perf.add_task(2.5, True)
    perf.add_task(3.0, True)
    perf.add_task(2.8, True)
    perf.add_task(3.2, True)
    perf.add_task(2.7, True)
    perf.add_task(2.9, False)
    perf.add_task(2.6, True)
    perf.add_task(3.1, True)
    perf.add_task(2.8, True)
    perf.add_task(2.7, True)
    perf.add_collaboration(True)
    perf.add_collaboration(True)
    perf.add_collaboration(False)

    # Test-Engineer
    perf = monitor.get_or_create_performance("test-engineer")
    perf.add_task(4.5, True)
    perf.add_task(5.0, True)
    perf.add_task(4.8, True)
    perf.add_task(4.2, True)
    perf.add_task(4.7, True)
    perf.add_task(5.2, True)
    perf.add_task(4.6, True)
    perf.add_task(4.9, True)
    perf.add_task(4.4, True)
    perf.add_task(4.8, True)
    perf.add_collaboration(True)
    perf.add_collaboration(True)

    # Frontend-Tester
    perf = monitor.get_or_create_performance("frontend-tester")
    perf.add_task(3.8, True)
    perf.add_task(4.2, True)
    perf.add_task(3.5, True)
    perf.add_task(4.0, True)
    perf.add_task(3.7, True)
    perf.add_task(4.1, True)
    perf.add_task(3.6, True)
    perf.add_task(3.9, True)
    perf.add_task(4.3, True)
    perf.add_task(3.8, True)
    perf.add_collaboration(True)
    perf.add_collaboration(True)

    # Backend-Expert
    perf = monitor.get_or_create_performance("backend-expert")
    perf.add_task(6.5, True)
    perf.add_task(7.0, True)
    perf.add_task(6.8, True)
    perf.add_task(6.2, True)
    perf.add_task(6.7, True)
    perf.add_task(7.2, True)
    perf.add_task(6.9, True)
    perf.add_task(6.4, True)
    perf.add_task(7.1, True)
    perf.add_task(6.6, True)
    perf.add_collaboration(True)
    perf.add_collaboration(True)

    # Security-Auditor
    perf = monitor.get_or_create_performance("security-auditor")
    perf.add_task(5.5, True)
    perf.add_task(6.0, True)
    perf.add_task(5.8, True)
    perf.add_task(5.2, True)
    perf.add_task(5.7, True)
    perf.add_task(6.2, True)
    perf.add_task(5.9, True)
    perf.add_task(5.4, True)
    perf.add_task(6.1, True)
    perf.add_task(5.6, True)
    perf.add_collaboration(True)

    print(f"✅ 已初始化 {len(monitor.agents)} 个智能体的性能数据\n")


if __name__ == "__main__":
    # 初始化性能监控
    seed_sample_data(performance_monitor)

    # 打印统计信息
    print("=== 性能监控统计 ===")
    stats = performance_monitor.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # 打印最佳表现者
    print("\n=== 最佳表现者 ===")
    for agent_id, score in performance_monitor.get_top_performers(3):
        perf = performance_monitor.get_agent_performance(agent_id)
        print(f"{agent_id}: {score:.3f} (成功率: {perf.success_rate*100:.1f}%, 平均时长: {perf.avg_duration:.1f}分钟)")

    # 生成优化建议
    print("\n=== 优化建议 ===")
    report = self_optimizer.get_optimization_report()
    for rec in report['recommendations'][:5]:
        level_emoji = "🔴" if rec.get('level') == 'high' else "🟡"
        print(f"{level_emoji} {rec['message']}")

    # 打印优化报告
    print("\n=== 优化报告 ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))
