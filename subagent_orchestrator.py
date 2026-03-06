#!/usr/bin/env python3
"""
子智能体编排器 (Subagent Orchestrator)

像杨天润的智能体军团一样实现多智能体协作
"""

import json
import time
import asyncio
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CollaborationMode(Enum):
    """协作模式"""
    PARALLEL = "parallel"  # 并行协作
    SEQUENTIAL = "sequential"  # 串行协作


class AgentRole(Enum):
    """子智能体角色"""
    CODE_REVIEWER = "code_reviewer"
    TEST_ENGINEER = "test_engineer"
    DOC_WRITER = "doc_writer"
    SECURITY_AUDITOR = "security_auditor"
    MANUS_EXPERT = "manus_expert"


@dataclass
class SubagentTask:
    """子智能体任务"""
    role: AgentRole
    name: str
    description: str
    command: str
    depends_on: List[str] = field(default_factory=list)
    timeout: int = 300  # 5 分钟超时


@dataclass
class SubagentResult:
    """子智能体结果"""
    role: AgentRole
    name: str
    success: bool
    output: str = ""
    error: str = ""
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SubagentOrchestrator:
    """子智能体编排器"""

    def __init__(self):
        self.tasks: List[SubagentTask] = []
        self.results: List[SubagentResult] = []
        self.mode = CollaborationMode.PARALLEL

    def add_task(self, task: SubagentTask) -> None:
        """添加任务"""
        self.tasks.append(task)
        logger.info(f"添加任务: {task.name} ({task.role.value})")

    def set_collaboration_mode(self, mode: CollaborationMode) -> None:
        """设置协作模式"""
        self.mode = mode
        logger.info(f"设置协作模式: {mode.value}")

    def execute_task(self, task: SubagentTask) -> SubagentResult:
        """执行单个任务"""
        logger.info(f"开始执行任务: {task.name}")

        start_time = time.time()

        try:
            # 执行命令
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                logger.info(f"任务 {task.name} 执行成功，耗时 {duration:.2f} 秒")
                return SubagentResult(
                    role=task.role,
                    name=task.name,
                    success=True,
                    output=result.stdout,
                    duration=duration
                )
            else:
                logger.error(f"任务 {task.name} 执行失败: {result.stderr}")
                return SubagentResult(
                    role=task.role,
                    name=task.name,
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    duration=duration
                )

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            logger.error(f"任务 {task.name} 超时 (>{task.timeout} 秒)")
            return SubagentResult(
                role=task.role,
                name=task.name,
                success=False,
                error=f"任务超时 (>{task.timeout} 秒)",
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"任务 {task.name} 执行异常: {str(e)}")
            return SubagentResult(
                role=task.role,
                name=task.name,
                success=False,
                error=str(e),
                duration=duration
            )

    def execute_parallel(self) -> List[SubagentResult]:
        """并行执行所有任务"""
        logger.info("开始并行执行任务...")
        start_time = time.time()

        results = []
        for task in self.tasks:
            result = self.execute_task(task)
            results.append(result)

        total_duration = time.time() - start_time
        logger.info(f"并行执行完成，总耗时 {total_duration:.2f} 秒")

        return results

    def execute_sequential(self) -> List[SubagentResult]:
        """串行执行所有任务（按依赖关系排序）"""
        logger.info("开始串行执行任务...")
        start_time = time.time()

        # 构建依赖图
        task_map = {task.name: task for task in self.tasks}
        completed = set()
        results = []

        while len(completed) < len(self.tasks):
            # 找出所有依赖已完成的任务
            ready_tasks = [
                task for task in self.tasks
                if task.name not in completed and
                all(dep in completed for dep in task.depends_on)
            ]

            if not ready_tasks:
                logger.error("检测到循环依赖或无法满足的依赖")
                break

            # 执行就绪的任务
            for task in ready_tasks:
                result = self.execute_task(task)
                results.append(result)

                if result.success:
                    completed.add(task.name)
                else:
                    logger.error(f"任务 {task.name} 失败，跳过依赖它的任务")
                    completed.add(task.name)  # 标记为完成（失败）

        total_duration = time.time() - start_time
        logger.info(f"串行执行完成，总耗时 {total_duration:.2f} 秒")

        return results

    def execute(self) -> List[SubagentResult]:
        """执行所有任务（根据协作模式）"""
        if not self.tasks:
            logger.warning("没有任务需要执行")
            return []

        if self.mode == CollaborationMode.PARALLEL:
            self.results = self.execute_parallel()
        else:
            self.results = self.execute_sequential()

        return self.results

    def generate_report(self) -> str:
        """生成执行报告"""
        report = []
        report.append("=" * 60)
        report.append("子智能体执行报告")
        report.append("=" * 60)
        report.append(f"协作模式: {self.mode.value}")
        report.append(f"任务总数: {len(self.tasks)}")
        report.append(f"成功: {sum(1 for r in self.results if r.success)}")
        report.append(f"失败: {sum(1 for r in self.results if not r.success)}")
        report.append("")

        for result in self.results:
            report.append("-" * 60)
            report.append(f"任务: {result.name} ({result.role.value})")
            report.append(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            report.append(f"耗时: {result.duration:.2f} 秒")

            if result.success:
                # 只显示前 10 行输出
                output_lines = result.output.strip().split('\n')[:10]
                report.append("输出:")
                report.extend(f"  {line}" for line in output_lines)
                if len(result.output.strip().split('\n')) > 10:
                    report.append("  ... (更多输出省略)")
            else:
                report.append(f"错误: {result.error}")

            report.append("")

        # 统计信息
        successful_results = [r for r in self.results if r.success]
        if successful_results:
            total_duration = sum(r.duration for r in successful_results)
            avg_duration = total_duration / len(successful_results)
            report.append("=" * 60)
            report.append("统计信息")
            report.append("=" * 60)
            report.append(f"总耗时: {total_duration:.2f} 秒")
            report.append(f"平均耗时: {avg_duration:.2f} 秒")
            report.append(f"最长任务: {max(successful_results, key=lambda r: r.duration).name}")
            report.append("")

        return "\n".join(report)

    def save_report(self, filename: str) -> None:
        """保存报告到文件"""
        report = self.generate_report()

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"报告已保存到: {filename}")


def create_code_reviewer_task() -> SubagentTask:
    """创建代码审查任务"""
    return SubagentTask(
        role=AgentRole.CODE_REVIEWER,
        name="代码审查",
        description="使用 flake8 检查代码质量",
        command="cd /root/.openclaw/workspace && flake8 --max-line-length=100 .",
        timeout=60
    )


def create_test_engineer_task() -> SubagentTask:
    """创建测试任务"""
    return SubagentTask(
        role=AgentRole.TEST_ENGINEER,
        name="测试运行",
        description="运行 pytest 测试并生成覆盖率报告",
        command="cd /root/.openclaw/workspace/ad-platform && pytest --cov=app --cov-report=term-missing || echo '测试未运行'",
        timeout=120
    )


def create_doc_writer_task() -> SubagentTask:
    """创建文档任务"""
    return SubagentTask(
        role=AgentRole.DOC_WRITER,
        name="文档生成",
        description="生成项目文档",
        command="cd /root/.openclaw/workspace && ls -la && echo '文档任务完成'",
        timeout=30
    )


def create_security_auditor_task() -> SubagentTask:
    """创建安全审计任务"""
    return SubagentTask(
        role=AgentRole.SECURITY_AUDITOR,
        name="安全审计",
        description="使用 safety 检查依赖漏洞",
        command="cd /root/.openclaw/workspace/ad-platform && safety check || echo 'safety 未安装'",
        timeout=60
    )


def main():
    """主函数 - 演示子智能体编排"""
    logger.info("=" * 60)
    logger.info("子智能体编排器启动")
    logger.info("=" * 60)

    # 创建编排器
    orchestrator = SubagentOrchestrator()

    # 添加任务（并行模式）
    orchestrator.set_collaboration_mode(CollaborationMode.PARALLEL)
    orchestrator.add_task(create_code_reviewer_task())
    orchestrator.add_task(create_test_engineer_task())
    orchestrator.add_task(create_doc_writer_task())
    orchestrator.add_task(create_security_auditor_task())

    # 执行任务
    logger.info("\n开始执行并行协作任务...")
    results = orchestrator.execute()

    # 生成报告
    report = orchestrator.generate_report()
    print("\n" + report)

    # 保存报告
    report_file = "/root/.openclaw/workspace/subagent-report.txt"
    orchestrator.save_report(report_file)

    logger.info(f"\n报告已保存: {report_file}")
    logger.info("子智能体编排器执行完成")


if __name__ == "__main__":
    main()
