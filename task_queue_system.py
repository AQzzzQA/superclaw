#!/usr/bin/env python3
"""
任务队列系统 (Task Queue System)

Phase 3: 任务队列优化
使用 Celery 实现分布式任务执行
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    LOWEST = 4


@dataclass
class QueuedTask:
    """队列任务"""
    task_id: str
    name: str
    description: str
    command: str
    priority: TaskPriority
    max_retries: int = 3
    retry_count: int = 0
    timeout: int = 300
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    name: str
    success: bool
    output: str = ""
    error: str = ""
    duration: float = 0.0
    retry_count: int = 0


class TaskQueue:
    """任务队列（简化版，不依赖 Celery）"""

    def __init__(self):
        self.queue: List[QueuedTask] = []
        self.completed: Dict[str, TaskResult] = {}
        self.running: Dict[str, QueuedTask] = {}

    def add_task(self, task: QueuedTask) -> None:
        """添加任务到队列"""
        # 按优先级插入
        self.queue.append(task)
        self.queue.sort(key=lambda t: t.priority.value)
        logger.info(f"任务已添加到队列: {task.name} (优先级: {task.priority.name})")

    def get_next_task(self) -> Optional[QueuedTask]:
        """获取下一个任务"""
        if not self.queue:
            return None

        # 检查依赖
        for i, task in enumerate(self.queue):
            if all(dep in self.completed for dep in task.dependencies):
                self.running[task.task_id] = task
                return self.queue.pop(i)

        return None

    def mark_completed(self, result: TaskResult) -> None:
        """标记任务完成"""
        self.completed[result.task_id] = result
        if result.task_id in self.running:
            del self.running[result.task_id]

        if result.success:
            logger.info(f"任务完成: {result.name} (耗时: {result.duration:.2f}s)")
        else:
            logger.warning(f"任务失败: {result.name} (错误: {result.error})")

    def execute_task(self, task: QueuedTask) -> TaskResult:
        """执行任务（模拟）"""
        import subprocess

        logger.info(f"开始执行任务: {task.name}")
        start_time = time.time()

        try:
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                return TaskResult(
                    task_id=task.task_id,
                    name=task.name,
                    success=True,
                    output=result.stdout,
                    duration=duration,
                    retry_count=task.retry_count
                )
            else:
                return TaskResult(
                    task_id=task.task_id,
                    name=task.name,
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    duration=duration,
                    retry_count=task.retry_count
                )

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return TaskResult(
                task_id=task.task_id,
                name=task.name,
                success=False,
                error=f"任务超时 (>{task.timeout} 秒)",
                duration=duration,
                retry_count=task.retry_count
            )
        except Exception as e:
            duration = time.time() - start_time
            return TaskResult(
                task_id=task.task_id,
                name=task.name,
                success=False,
                error=str(e),
                duration=duration,
                retry_count=task.retry_count
            )

    def process_queue(self) -> List[TaskResult]:
        """处理队列中的所有任务"""
        logger.info("=" * 60)
        logger.info("开始处理任务队列")
        logger.info("=" * 60)
        logger.info(f"队列任务数: {len(self.queue)}")

        results = []

        while self.queue or self.running:
            # 获取下一个任务
            task = self.get_next_task()

            if not task:
                # 没有可执行的任务，等待运行中的任务完成
                if not self.running:
                    break
                time.sleep(0.1)
                continue

            # 执行任务
            result = self.execute_task(task)

            # 检查是否需要重试
            if not result.success and result.retry_count < task.max_retries:
                logger.info(f"任务失败，重试 ({result.retry_count + 1}/{task.max_retries})")
                task.retry_count += 1
                self.add_task(task)
            else:
                # 标记完成
                self.mark_completed(result)
                results.append(result)

        logger.info("=" * 60)
        logger.info("任务队列处理完成")
        logger.info("=" * 60)

        return results

    def generate_report(self) -> str:
        """生成队列执行报告"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("任务队列执行报告")
        report_lines.append("=" * 60)
        report_lines.append(f"总任务数: {len(self.completed)}")
        report_lines.append("")

        successful = [r for r in self.completed.values() if r.success]
        failed = [r for r in self.completed.values() if not r.success]

        report_lines.append(f"成功: {len(successful)}")
        report_lines.append(f"失败: {len(failed)}")
        report_lines.append("")

        # 按优先级统计
        priority_stats = {}
        for result in self.completed.values():
            # 查找任务的优先级
            task = None
            for t in self.queue + list(self.running.values()):
                if t.task_id == result.task_id:
                    task = t
                    break

            if task:
                priority = task.priority.name
                if priority not in priority_stats:
                    priority_stats[priority] = {"total": 0, "success": 0}
                priority_stats[priority]["total"] += 1
                if result.success:
                    priority_stats[priority]["success"] += 1

        report_lines.append("")
        report_lines.append("-" * 60)
        report_lines.append("优先级统计:")
        report_lines.append("-" * 60)
        for priority, stats in sorted(priority_stats.items()):
            total = stats["total"]
            success = stats["success"]
            rate = (success / total * 100) if total > 0 else 0
            report_lines.append(f"{priority}: {success}/{total} ({rate:.1f}%)")

        # 统计信息
        total_duration = sum(r.duration for r in self.completed.values())
        avg_duration = total_duration / len(self.completed) if self.completed else 0

        report_lines.append("")
        report_lines.append("-" * 60)
        report_lines.append("统计信息:")
        report_lines.append("-" * 60)
        report_lines.append(f"总耗时: {total_duration:.2f} 秒")
        report_lines.append(f"平均耗时: {avg_duration:.2f} 秒")

        # 最长任务
        if self.completed:
            longest = max(self.completed.values(), key=lambda r: r.duration)
            report_lines.append(f"最长任务: {longest.name} ({longest.duration:.2f}s)")

        return "\n".join(report_lines)

    def save_report(self, filename: str) -> None:
        """保存报告"""
        report = self.generate_report()

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"报告已保存: {filename}")


def main():
    """主函数 - 演示任务队列系统"""
    logger.info("=" * 60)
    logger.info("任务队列系统启动 (Phase 3)")
    logger.info("=" * 60)

    # 创建任务队列
    queue = TaskQueue()

    # 添加测试任务
    tasks = [
        QueuedTask(
            task_id="task_1",
            name="代码扫描",
            description="扫描 Python 文件",
            command="cd /root/.openclaw/workspace && find . -name '*.py' | wc -l",
            priority=TaskPriority.HIGH,
            timeout=30
        ),
        QueuedTask(
            task_id="task_2",
            name="文档检查",
            description="检查文档完整性",
            command="cd /root/.openclaw/workspace && ls -la *.md | wc -l",
            priority=TaskPriority.MEDIUM,
            dependencies=["task_1"],
            timeout=30
        ),
        QueuedTask(
            task_id="task_3",
            name="依赖检查",
            description="检查 Python 依赖",
            command="cd /root/.openclaw/workspace/ad-platform && pip list --outdated | head -5",
            priority=TaskPriority.LOW,
            dependencies=["task_1"],
            timeout=30
        ),
        QueuedTask(
            task_id="task_4",
            name="日志分析",
            description="分析日志文件",
            command="cd /root/.openclaw/workspace && cat .gitignore | wc -l",
            priority=TaskPriority.LOWEST,
            dependencies=["task_2", "task_3"],
            timeout=30
        )
    ]

    # 添加任务到队列
    for task in tasks:
        queue.add_task(task)

    # 处理队列
    results = queue.process_queue()

    # 生成报告
    report = queue.generate_report()
    print("\n" + report)

    # 保存报告
    report_file = "/root/.openclaw/workspace/task-queue-report.txt"
    queue.save_report(report_file)

    logger.info(f"\n报告已保存: {report_file}")
    logger.info("任务队列系统执行完成")


if __name__ == "__main__":
    main()
