#!/usr/bin/env python3
"""
Agency 编排系统
协调智能体间的自动协作
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from agency_manager import AgencyManager, Agent, Task, Collaboration, AgentStatus
from memory_system import MemorySystem, MemoryCategory
from performance_monitor import PerformanceMonitor, SelfOptimizer


@dataclass
class Subtask:
    """子任务"""
    id: str
    parent_id: str
    title: str
    description: str
    required_capability: str
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class TaskDecomposer:
    """任务分解器"""

    def __init__(self, agency: AgencyManager):
        self.agency = agency

    def decompose(self, task: Task) -> List[Subtask]:
        """分解任务为子任务"""
        subtasks = []

        # 根据任务类型分解
        if "代码审查" in task.title or "code review" in task.title.lower():
            subtasks = self._decompose_code_review(task)
        elif "测试" in task.title or "test" in task.title.lower():
            subtasks = self._decompose_test(task)
        elif "文档" in task.title or "document" in task.title.lower():
            subtasks = self._decompose_documentation(task)
        elif "开发" in task.title or "develop" in task.title.lower():
            subtasks = self._decompose_development(task)
        elif "安全" in task.title or "security" in task.title.lower():
            subtasks = self._decompose_security(task)
        else:
            # 默认分解
            subtasks = self._decompose_generic(task)

        return subtasks

    def _decompose_code_review(self, task: Task) -> List[Subtask]:
        """分解代码审查任务"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="代码规范检查",
                description="使用 flake8 检查代码规范",
                required_capability="代码审查"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="代码格式化",
                description="使用 black 格式化代码",
                required_capability="代码格式化"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="类型检查",
                description="使用 mypy 检查类型注解",
                required_capability="类型检查"
            )
        ]

    def _decompose_test(self, task: Task) -> List[Subtask]:
        """分解测试任务"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="编写单元测试",
                description="使用 pytest 编写单元测试",
                required_capability="单元测试"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="运行覆盖率测试",
                description="使用 pytest-cov 检查覆盖率",
                required_capability="覆盖率测试"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="编写集成测试",
                description="编写集成测试用例",
                required_capability="集成测试"
            )
        ]

    def _decompose_documentation(self, task: Task) -> List[Subtask]:
        """分解文档任务"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="编写 README",
                description="编写或更新项目 README",
                required_capability="README编写"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="编写 API 文档",
                description="生成 API 文档",
                required_capability="API文档"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="编写技术文档",
                description="编写详细技术文档",
                required_capability="文档编写"
            )
        ]

    def _decompose_development(self, task: Task) -> List[Subtask]:
        """分解开发任务"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="API 开发",
                description="开发 REST API",
                required_capability="API开发"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="数据库设计",
                description="设计数据库 Schema",
                required_capability="数据库设计"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="性能优化",
                description="优化性能",
                required_capability="性能优化"
            )
        ]

    def _decompose_security(self, task: Task) -> List[Subtask]:
        """分解安全任务"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="安全审计",
                description="使用 safety, bandit 扫描",
                required_capability="安全审计"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="依赖扫描",
                description="扫描依赖库漏洞",
                required_capability="依赖扫描"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="代码安全检查",
                description="检查代码安全问题",
                required_capability="代码安全"
            )
        ]

    def _decompose_generic(self, task: Task) -> List[Subtask]:
        """通用任务分解"""
        return [
            Subtask(
                id=f"{task.id}_1",
                parent_id=task.id,
                title="分析需求",
                description="分析任务需求",
                required_capability=task.required_capabilities[0] if task.required_capabilities else "分析"
            ),
            Subtask(
                id=f"{task.id}_2",
                parent_id=task.id,
                title="实施方案",
                description="制定实施方案",
                required_capability=task.required_capabilities[0] if task.required_capabilities else "实施"
            ),
            Subtask(
                id=f"{task.id}_3",
                parent_id=task.id,
                title="验证结果",
                description="验证实施结果",
                required_capability=task.required_capabilities[0] if task.required_capabilities else "验证"
            )
        ]


class TaskCoordinator:
    """任务协调器"""

    def __init__(self, agency: AgencyManager, memory: MemorySystem, monitor: PerformanceMonitor):
        self.agency = agency
        self.memory = memory
        self.monitor = monitor
        self.active_collaborations: Dict[str, Dict[str, Any]] = {}

    async def coordinate_task(self, task: Task) -> Dict[str, Any]:
        """协调任务执行"""
        print(f"\n🎯 开始协调任务: {task.title}")

        # 检查是否需要协作
        requires_collaboration = len(task.required_capabilities) > 1 or self._is_complex_task(task)

        if requires_collaboration:
            return await self._coordinate_collaboration(task)
        else:
            return await self._coordinate_single(task)

    async def _coordinate_single(self, task: Task) -> Dict[str, Any]:
        """协调单个智能体执行"""
        print(f"👤 单智能体执行模式")

        # 找到最佳智能体
        best_agent_id = self.agency.find_best_agent(task)
        if not best_agent_id:
            return {
                'success': False,
                'error': '没有找到合适的智能体'
            }

        # 分配任务
        self.agency.assign_task(task.id, best_agent_id)

        # 记录到记忆
        self.memory.store(
            agent_id=best_agent_id,
            category=MemoryCategory.TASK,
            content=f"开始执行任务: {task.title}",
            metadata={'task_id': task.id}
        )

        # 模拟执行（实际中会调用智能体）
        await asyncio.sleep(1)

        # 完成任务
        result = f"任务 {task.title} 已完成"
        self.agency.complete_task(task.id, result)

        # 记录性能
        self.monitor.track_task(best_agent_id, duration=2.5, success=True)

        # 记录到记忆
        self.memory.store(
            agent_id=best_agent_id,
            category=MemoryCategory.TASK,
            content=f"完成任务: {task.title}",
            metadata={'task_id': task.id, 'result': result}
        )

        return {
            'success': True,
            'result': result,
            'agent': best_agent_id,
            'duration': 2.5
        }

    async def _coordinate_collaboration(self, task: Task) -> Dict[str, Any]:
        """协调智能体协作"""
        print(f"🤝 协作执行模式")

        # 组建团队
        team = self.agency.build_team(task)
        if len(team) < 1:
            return {
                'success': False,
                'error': '无法组建团队'
            }

        print(f"👥 团队成员: {', '.join(team)}")

        # 分解任务
        decomposer = TaskDecomposer(self.agency)
        subtasks = decomposer.decompose(task)
        print(f"📋 分解为 {len(subtasks)} 个子任务")

        # 分配子任务
        assignments = {}
        for i, subtask in enumerate(subtasks):
            if i < len(team):
                assignments[subtask.id] = team[i]
                print(f"  - {subtask.title} → {team[i]}")

        # 创建协作
        coordinator_id = team[0]
        collab_id = self.agency.create_collaboration(task.id, team, coordinator_id)

        # 执行子任务
        results = []
        total_duration = 0

        for subtask in subtasks:
            agent_id = assignments.get(subtask.id)

            if not agent_id:
                print(f"⚠️ 子任务 {subtask.title} 未分配智能体")
                continue

            # 记录到记忆
            self.memory.store(
                agent_id=agent_id,
                category=MemoryCategory.COLLABORATION,
                content=f"开始执行子任务: {subtask.title}",
                metadata={'task_id': task.id, 'subtask_id': subtask.id}
            )

            # 模拟执行
            await asyncio.sleep(0.5)
            duration = 1.5 + (hash(subtask.id) % 10) / 10
            total_duration += duration

            # 记录结果
            subtask.assigned_to = agent_id
            subtask.status = "completed"
            subtask.result = f"{subtask.title} 已完成"
            subtask.completed_at = datetime.now().isoformat()

            results.append(subtask)

            # 记录性能
            self.monitor.track_task(agent_id, duration=duration, success=True)
            self.monitor.track_collaboration(agent_id, success=True)

            print(f"  ✅ {subtask.title} ({duration:.1f}s)")

        # 完成任务
        result = f"协作任务 {task.title} 已完成，{len(results)} 个子任务全部完成"
        self.agency.complete_task(task.id, result)

        # 完成协作
        collaboration = self.agency.get_collaboration(collab_id)
        if collaboration:
            collaboration.status = "completed"
            collaboration.ended_at = datetime.now().isoformat()
            collaboration.result = result

        # 记录到记忆
        for agent_id in team:
            self.memory.store(
                agent_id=agent_id,
                category=MemoryCategory.COLLABORATION,
                content=f"参与协作: {task.title}",
                metadata={'task_id': task.id, 'collab_id': collab_id}
            )

        return {
            'success': True,
            'result': result,
            'team': team,
            'collaboration_id': collab_id,
            'subtasks': len(results),
            'duration': total_duration
        }

    def _is_complex_task(self, task: Task) -> bool:
        """判断是否为复杂任务"""
        # 任务描述较长
        if len(task.description) > 200:
            return True

        # 优先级较高
        if task.priority > 5:
            return True

        # 包含复杂关键词
        complex_keywords = ['复杂', '复杂度', '多个', '多模块', '集成', '整合', '架构']
        if any(keyword in task.title or keyword in task.description for keyword in complex_keywords):
            return True

        return False


class AgencyOrchestrator:
    """Agency 编排器"""

    def __init__(self):
        self.agency = AgencyManager()
        self.memory = MemorySystem()
        self.monitor = PerformanceMonitor()
        self.optimizer = SelfOptimizer(self.monitor)
        self.coordinator = TaskCoordinator(self.agency, self.memory, self.monitor)

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """处理任务"""
        # 创建任务
        self.agency.create_task(task)

        # 协调执行
        result = await self.coordinator.coordinate_task(task)

        return result

    async def process_task_batch(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """批量处理任务"""
        results = []

        for task in tasks:
            result = await self.process_task(task)
            results.append(result)

        return results

    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'agency': self.agency.get_status_report(),
            'memory': self.memory.get_statistics(),
            'performance': self.monitor.get_statistics(),
            'optimization': self.optimizer.get_optimization_report()
        }

    def get_top_team(self, n: int = 3) -> List[str]:
        """获取最佳团队"""
        top = self.monitor.get_top_performers(n)
        return [agent_id for agent_id, _ in top]

    def generate_team_report(self) -> str:
        """生成团队报告"""
        top = self.monitor.get_top_performers(3)
        stats = self.monitor.get_statistics()

        report = "=== 智能体团队报告 ===\n\n"
        report += f"📊 统计信息:\n"
        report += f"  - 总智能体数: {stats['total_agents']}\n"
        report += f"  - 总任务数: {stats['total_tasks']}\n"
        report += f"  - 完成率: {stats['success_rate']*100:.1f}%\n"
        report += f"  - 平均时长: {stats['avg_duration']:.1f}分钟\n\n"

        report += "🏆 最佳表现者:\n"
        for i, (agent_id, score) in enumerate(top, 1):
            perf = self.monitor.get_agent_performance(agent_id)
            report += f"  {i}. {agent_id}: {score:.3f}\n"
            report += f"     - 成功率: {perf.success_rate*100:.1f}%\n"
            report += f"     - 平均时长: {perf.avg_duration:.1f}分钟\n"
            report += f"     - 完成任务: {perf.completed_tasks}\n\n"

        return report


async def main():
    """主函数"""
    from agency_manager import register_openclaw_agents
    from memory_system import seed_initial_memories
    from performance_monitor import seed_sample_data

    # 初始化系统
    print("🚀 初始化 Agency 编排系统\n")

    register_openclaw_agents(agency_manager.agency)
    seed_initial_memories(agency_manager.memory)
    seed_sample_data(agency_manager.monitor)

    # 创建测试任务
    print("\n" + "="*50)
    print("开始执行测试任务")
    print("="*50 + "\n")

    tasks = [
        Task(
            id="task_001",
            title="代码审查任务",
            description="审查 PR #123 的代码质量",
            required_capabilities=["代码审查", "代码格式化", "类型检查"],
            priority=3
        ),
        Task(
            id="task_002",
            title="测试任务",
            description="为新功能编写完整测试",
            required_capabilities=["单元测试", "覆盖率测试"],
            priority=2
        ),
        Task(
            id="task_003",
            title="文档编写任务",
            description="编写 API 文档和用户指南",
            required_capabilities=["文档编写", "API文档"],
            priority=2
        )
    ]

    # 处理任务
    for task in tasks:
        result = await agency_manager.process_task(task)
        print(f"\n✅ 任务结果: {result.get('result')}")
        if result.get('success'):
            print(f"   执行时长: {result.get('duration', 0):.1f}秒")

    # 打印团队报告
    print("\n" + "="*50)
    print(agency_manager.generate_team_report())
    print("="*50)

    # 生成优化建议
    print("\n" + "="*50)
    print("优化建议")
    print("="*50 + "\n")

    report = agency_manager.optimizer.get_optimization_report()
    for rec in report['recommendations'][:5]:
        print(f"  • {rec['message']}")

    # 打印完整状态
    print("\n" + "="*50)
    print("完整状态")
    print("="*50 + "\n")

    status = agency_manager.get_status()
    import json
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    agency_manager = AgencyOrchestrator()
    asyncio.run(main())
