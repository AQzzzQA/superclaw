#!/usr/bin/env python3
"""
Agency 管理系统
负责管理和协调多个智能体的协作
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class AgentStatus(Enum):
    """智能体状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentCapabilities:
    """智能体能力"""
    name: str
    description: str
    proficiency: float  # 0.0 - 1.0


@dataclass
class AgentMetrics:
    """智能体性能指标"""
    tasks_completed: int = 0
    avg_duration: float = 0.0
    success_rate: float = 1.0
    last_active: str = ""


@dataclass
class Agent:
    """智能体定义"""
    id: str
    name: str
    description: str
    capabilities: List[AgentCapabilities]
    status: AgentStatus = AgentStatus.IDLE
    metrics: AgentMetrics = None
    current_task: Optional[str] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = AgentMetrics()

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'capabilities': [asdict(c) for c in self.capabilities],
            'status': self.status.value,
            'metrics': asdict(self.metrics),
            'current_task': self.current_task
        }


@dataclass
class Task:
    """任务定义"""
    id: str
    title: str
    description: str
    required_capabilities: List[str]
    priority: int = 0
    deadline: Optional[str] = None
    status: str = "pending"
    assigned_to: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Collaboration:
    """协作定义"""
    id: str
    task_id: str
    agents: List[str]
    coordinator: str
    status: str = "active"
    started_at: str = ""
    ended_at: Optional[str] = None
    result: Optional[str] = None
    performance: Dict[str, Any] = None

    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()
        if self.performance is None:
            self.performance = {}


class AgencyManager:
    """代理机构管理器"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.collaborations: Dict[str, Collaboration] = {}
        self.task_counter = 0
        self.collaboration_counter = 0

    def register_agent(self, agent: Agent) -> bool:
        """注册智能体"""
        if agent.id in self.agents:
            return False

        self.agents[agent.id] = agent
        print(f"✅ 智能体已注册: {agent.name} ({agent.id})")
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """注销智能体"""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        print(f"❌ 智能体已注销: {agent.name} ({agent_id})")
        del self.agents[agent_id]
        return True

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取智能体"""
        return self.agents.get(agent_id)

    def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]:
        """列出智能体"""
        agents = list(self.agents.values())

        if status:
            agents = [a for a in agents if a.status == status]

        return agents

    def create_task(self, task: Task) -> str:
        """创建任务"""
        self.tasks[task.id] = task
        print(f"📋 任务已创建: {task.title} ({task.id})")
        return task.id

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """分配任务给智能体"""
        if task_id not in self.tasks:
            return False

        if agent_id not in self.agents:
            return False

        task = self.tasks[task_id]
        agent = self.agents[agent_id]

        # 检查智能体是否具备所需能力
        agent_capabilities = [c.name for c in agent.capabilities]
        if not all(cap in agent_capabilities for cap in task.required_capabilities):
            print(f"⚠️ 智能体 {agent.name} 不具备完成任务 {task.title} 所需的能力")
            return False

        # 分配任务
        task.assigned_to = agent_id
        task.status = "assigned"
        agent.current_task = task_id
        agent.status = AgentStatus.BUSY

        print(f"✅ 任务已分配: {task.title} → {agent.name}")
        return True

    def find_best_agent(self, task: Task) -> Optional[str]:
        """找到最适合完成任务的智能体"""
        candidates = []

        for agent_id, agent in self.agents.items():
            if agent.status != AgentStatus.IDLE:
                continue

            # 检查能力匹配
            agent_capabilities = [c.name for c in agent.capabilities]
            if not all(cap in agent_capabilities for cap in task.required_capabilities):
                continue

            # 计算匹配度
            match_score = 0
            for req_cap in task.required_capabilities:
                for agent_cap in agent.capabilities:
                    if agent_cap.name == req_cap:
                        match_score += agent_cap.proficiency

            candidates.append((agent_id, match_score))

        if not candidates:
            return None

        # 选择匹配度最高的智能体
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def build_team(self, task: Task) -> List[str]:
        """为任务自动组建团队"""
        required_capabilities = task.required_capabilities

        # 找到具备所需能力的所有智能体
        candidates = []
        for agent_id, agent in self.agents.items():
            if agent.status != AgentStatus.IDLE:
                continue

            agent_capabilities = [c.name for c in agent.capabilities]
            matches = [cap for cap in required_capabilities if cap in agent_capabilities]

            if matches:
                candidates.append((agent_id, len(matches)))

        # 按匹配度排序
        candidates.sort(key=lambda x: x[1], reverse=True)

        # 选择最佳团队（确保覆盖所有所需能力）
        team = []
        covered = set()

        for agent_id, _ in candidates:
            if len(team) >= 3:  # 最多3个智能体
                break

            agent = self.agents[agent_id]
            agent_capabilities = [c.name for c in agent.capabilities]

            # 检查这个智能体能提供什么新能力
            new_capabilities = set(agent_capabilities) - covered

            if new_capabilities or len(team) < 2:  # 至少2个智能体
                team.append(agent_id)
                covered.update(agent_capabilities)

            if covered >= set(required_capabilities):
                break

        return team

    def create_collaboration(self, task_id: str, agent_ids: List[str], coordinator_id: str) -> str:
        """创建协作"""
        if task_id not in self.tasks:
            return None

        if not all(agent_id in self.agents for agent_id in agent_ids):
            return None

        if coordinator_id not in agent_ids:
            return None

        # 更新任务状态
        task = self.tasks[task_id]
        task.status = "in_progress"
        task.assigned_to = coordinator_id

        # 更新智能体状态
        for agent_id in agent_ids:
            agent = self.agents[agent_id]
            agent.status = AgentStatus.BUSY
            agent.current_task = task_id

        # 创建协作
        self.collaboration_counter += 1
        collab_id = f"collab_{self.collaboration_counter}"

        collaboration = Collaboration(
            id=collab_id,
            task_id=task_id,
            agents=agent_ids,
            coordinator=coordinator_id
        )

        self.collaborations[collab_id] = collaboration

        print(f"🤝 协作已创建: {collab_id} (任务: {task.title}, 团队: {len(agent_ids)}个智能体)")
        return collab_id

    def complete_task(self, task_id: str, result: str) -> bool:
        """完成任务"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        task.assigned_to = None

        # 更新智能体状态
        for agent_id, agent in self.agents.items():
            if agent.current_task == task_id:
                agent.current_task = None
                agent.status = AgentStatus.IDLE

                # 更新性能指标
                agent.metrics.tasks_completed += 1

                # 计算任务时长
                start = datetime.fromisoformat(task.created_at)
                end = datetime.fromisoformat(task.completed_at)
                duration = (end - start).total_seconds() / 60  # 分钟

                # 更新平均时长
                n = agent.metrics.tasks_completed
                agent.metrics.avg_duration = (
                    (agent.metrics.avg_duration * (n - 1) + duration) / n
                )

                agent.metrics.last_active = datetime.now().isoformat()

        print(f"✅ 任务已完成: {task.title} (结果: {result[:50]}...)")
        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """任务失败"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = "failed"

        # 更新智能体状态和成功率
        for agent_id, agent in self.agents.items():
            if agent.current_task == task_id:
                agent.current_task = None
                agent.status = AgentStatus.ERROR

                # 更新成功率
                n = agent.metrics.tasks_completed + 1
                agent.metrics.success_rate = (
                    (agent.metrics.success_rate * agent.metrics.tasks_completed) / n
                )

        print(f"❌ 任务失败: {task.title} (错误: {error[:50]}...)")
        return True

    def get_collaboration(self, collab_id: str) -> Optional[Collaboration]:
        """获取协作"""
        return self.collaborations.get(collab_id)

    def list_collaborations(self, status: Optional[str] = None) -> List[Collaboration]:
        """列出协作"""
        collaborations = list(self.collaborations.values())

        if status:
            collaborations = [c for c in collaborations if c.status == status]

        return collaborations

    def get_status_report(self) -> Dict[str, Any]:
        """获取状态报告"""
        return {
            'agents': {
                'total': len(self.agents),
                'idle': len([a for a in self.agents.values() if a.status == AgentStatus.IDLE]),
                'busy': len([a for a in self.agents.values() if a.status == AgentStatus.BUSY]),
                'error': len([a for a in self.agents.values() if a.status == AgentStatus.ERROR]),
            },
            'tasks': {
                'total': len(self.tasks),
                'pending': len([t for t in self.tasks.values() if t.status == 'pending']),
                'assigned': len([t for t in self.tasks.values() if t.status == 'assigned']),
                'in_progress': len([t for t in self.tasks.values() if t.status == 'in_progress']),
                'completed': len([t for t in self.tasks.values() if t.status == 'completed']),
                'failed': len([t for t in self.tasks.values() if t.status == 'failed']),
            },
            'collaborations': {
                'total': len(self.collaborations),
                'active': len([c for c in self.collaborations.values() if c.status == 'active']),
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'agents': {k: v.to_dict() for k, v in self.agents.items()},
            'tasks': {k: asdict(v) for k, v in self.tasks.items()},
            'collaborations': {k: asdict(v) for k, v in self.collaborations.items()},
            'status': self.get_status_report()
        }


# 初始化全局管理器
agency_manager = AgencyManager()


def register_openclaw_agents(manager: AgencyManager):
    """注册 OpenClaw 智能体天团"""

    # Code-Reviewer
    manager.register_agent(Agent(
        id="code-reviewer",
        name="代码审查员",
        description="检查代码质量和规范",
        capabilities=[
            AgentCapabilities("代码审查", "使用 flake8, black, mypy 检查代码", 0.95),
            AgentCapabilities("代码格式化", "使用 black 格式化代码", 0.95),
            AgentCapabilities("类型检查", "使用 mypy 检查类型注解", 0.90),
        ]
    ))

    # Test-Engineer
    manager.register_agent(Agent(
        id="test-engineer",
        name="测试工程师",
        description="编写和运行单元测试",
        capabilities=[
            AgentCapabilities("单元测试", "使用 pytest 编写测试", 0.95),
            AgentCapabilities("覆盖率测试", "使用 pytest-cov 检查覆盖率", 0.95),
            AgentCapabilities("集成测试", "编写集成测试", 0.85),
        ]
    ))

    # Frontend-Tester
    manager.register_agent(Agent(
        id="frontend-tester",
        name="前端测试专家",
        description="自动化浏览器测试",
        capabilities=[
            AgentCapabilities("浏览器自动化", "使用 Agent Browser 操作浏览器", 0.95),
            AgentCapabilities("UI测试", "测试用户界面交互", 0.90),
            AgentCapabilities("API测试", "测试前端API集成", 0.90),
        ]
    ))

    # Backend-Expert
    manager.register_agent(Agent(
        id="backend-expert",
        name="后端开发专家",
        description="后端API开发",
        capabilities=[
            AgentCapabilities("API开发", "使用 FastAPI 开发REST API", 0.95),
            AgentCapabilities("数据库设计", "设计数据库Schema", 0.90),
            AgentCapabilities("性能优化", "优化后端性能", 0.85),
        ]
    ))

    # Security-Auditor
    manager.register_agent(Agent(
        id="security-auditor",
        name="安全审计员",
        description="检查安全漏洞",
        capabilities=[
            AgentCapabilities("安全审计", "使用 safety, bandit 扫描漏洞", 0.95),
            AgentCapabilities("依赖扫描", "扫描依赖库漏洞", 0.95),
            AgentCapabilities("代码安全", "检查代码安全问题", 0.90),
        ]
    ))

    # Documentation-Writer
    manager.register_agent(Agent(
        id="documentation-writer",
        name="文档编写员",
        description="编写技术文档",
        capabilities=[
            AgentCapabilities("文档编写", "编写 Markdown 文档", 0.95),
            AgentCapabilities("API文档", "生成 API 文档", 0.90),
            AgentCapabilities("README编写", "编写项目 README", 0.95),
        ]
    ))

    print(f"\n✅ 已注册 {len(manager.agents)} 个智能体到 Agency 系统\n")


if __name__ == "__main__":
    # 初始化 Agency 系统
    register_openclaw_agents(agency_manager)

    # 打印状态
    print("=== Agency 系统状态 ===")
    status = agency_manager.get_status_report()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    # 列出所有智能体
    print("\n=== 智能体列表 ===")
    for agent in agency_manager.list_agents():
        print(f"{agent.name} ({agent.id}): {agent.status.value}")
        for cap in agent.capabilities:
            print(f"  - {cap.name} (熟练度: {cap.proficiency*100:.0f}%)")

    # 创建测试任务
    task = Task(
        id="task_001",
        title="代码审查任务",
        description="审查 PR #123 的代码质量",
        required_capabilities=["代码审查", "代码格式化"],
        priority=1
    )

    agency_manager.create_task(task)

    # 分配任务
    best_agent_id = agency_manager.find_best_agent(task)
    if best_agent_id:
        agency_manager.assign_task(task.id, best_agent_id)

    # 完成任务
    agency_manager.complete_task(task.id, "代码审查完成，发现3个问题")

    # 打印最新状态
    print("\n=== 最新状态 ===")
    status = agency_manager.get_status_report()
    print(json.dumps(status, indent=2, ensure_ascii=False))
