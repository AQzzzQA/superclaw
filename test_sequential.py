#!/usr/bin/env python3
"""
测试串行协作模式
"""

from subagent_orchestrator import (
    SubagentOrchestrator,
    SubagentTask,
    CollaborationMode,
    AgentRole
)


def test_sequential_mode():
    """测试串行协作模式"""
    print("=" * 60)
    print("测试串行协作模式")
    print("=" * 60)

    # 创建编排器
    orchestrator = SubagentOrchestrator()

    # 创建有依赖关系的任务
    task1 = SubagentTask(
        role=AgentRole.DOC_WRITER,
        name="扫描代码库",
        description="扫描项目代码",
        command="cd /root/.openclaw/workspace && find . -name '*.py' | wc -l",
        timeout=30
    )

    task2 = SubagentTask(
        role=AgentRole.DOC_WRITER,
        name="生成文档",
        description="生成项目文档",
        command="cd /root/.openclaw/workspace && ls -la | head -10",
        depends_on=["扫描代码库"],
        timeout=30
    )

    task3 = SubagentTask(
        role=AgentRole.DOC_WRITER,
        name="检查配置",
        description="检查项目配置",
        command="cd /root/.openclaw/workspace && cat .gitignore 2>/dev/null | head -5",
        depends_on=["生成文档"],
        timeout=30
    )

    # 添加任务
    orchestrator.set_collaboration_mode(CollaborationMode.SEQUENTIAL)
    orchestrator.add_task(task1)
    orchestrator.add_task(task2)
    orchestrator.add_task(task3)

    # 执行任务
    print("\n开始执行串行协作任务...\n")
    results = orchestrator.execute()

    # 生成报告
    report = orchestrator.generate_report()
    print("\n" + report)

    # 保存报告
    report_file = "/root/.openclaw/workspace/subagent-sequential-report.txt"
    orchestrator.save_report(report_file)

    print(f"\n报告已保存: {report_file}")

    # 统计
    successful = sum(1 for r in results if r.success)
    print(f"\n成功率: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")


if __name__ == "__main__":
    test_sequential_mode()
