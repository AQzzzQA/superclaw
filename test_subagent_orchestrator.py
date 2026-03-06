#!/usr/bin/env python3
"""
子智能体编排器单元测试
"""

import unittest
import time
from subagent_orchestrator import (
    SubagentOrchestrator,
    SubagentTask,
    SubagentResult,
    CollaborationMode,
    AgentRole
)


class TestSubagentOrchestrator(unittest.TestCase):
    """子智能体编排器测试"""

    def setUp(self):
        """测试初始化"""
        self.orchestrator = SubagentOrchestrator()

    def test_add_task(self):
        """测试添加任务"""
        task = SubagentTask(
            role=AgentRole.CODE_REVIEWER,
            name="测试任务",
            description="测试描述",
            command="echo 'test'"
        )

        self.orchestrator.add_task(task)

        self.assertEqual(len(self.orchestrator.tasks), 1)
        self.assertEqual(self.orchestrator.tasks[0].name, "测试任务")

    def test_collaboration_mode(self):
        """测试协作模式设置"""
        self.orchestrator.set_collaboration_mode(CollaborationMode.PARALLEL)
        self.assertEqual(self.orchestrator.mode, CollaborationMode.PARALLEL)

        self.orchestrator.set_collaboration_mode(CollaborationMode.SEQUENTIAL)
        self.assertEqual(self.orchestrator.mode, CollaborationMode.SEQUENTIAL)

    def test_execute_simple_task(self):
        """测试执行简单任务"""
        task = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="简单任务",
            description="执行 echo 命令",
            command="echo 'Hello, World!'"
        )

        result = self.orchestrator.execute_task(task)

        self.assertTrue(result.success)
        self.assertIn("Hello, World!", result.output)
        self.assertGreater(result.duration, 0)

    def test_execute_failing_task(self):
        """测试执行失败任务"""
        task = SubagentTask(
            role=AgentRole.CODE_REVIEWER,
            name="失败任务",
            description="执行不存在的命令",
            command="nonexistent_command_12345",
            timeout=1
        )

        result = self.orchestrator.execute_task(task)

        self.assertFalse(result.success)
        self.assertGreater(len(result.error), 0)

    def test_parallel_execution(self):
        """测试并行执行"""
        # 创建多个简单任务
        for i in range(3):
            task = SubagentTask(
                role=AgentRole.DOC_WRITER,
                name=f"任务 {i}",
                description=f"测试任务 {i}",
                command=f"echo '任务 {i} 完成' && sleep 1"
            )
            self.orchestrator.add_task(task)

        self.orchestrator.set_collaboration_mode(CollaborationMode.PARALLEL)

        start_time = time.time()
        results = self.orchestrator.execute()
        duration = time.time() - start_time

        # 并行执行，3 个任务应该 < 3 秒
        self.assertLess(duration, 3.5)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r.success for r in results))

    def test_sequential_execution(self):
        """测试串行执行"""
        # 创建有依赖关系的任务
        task1 = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="任务 1",
            description="第一个任务",
            command="echo '任务 1 完成' && sleep 0.5"
        )

        task2 = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="任务 2",
            description="第二个任务",
            command="echo '任务 2 完成' && sleep 0.5",
            depends_on=["任务 1"]
        )

        task3 = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="任务 3",
            description="第三个任务",
            command="echo '任务 3 完成' && sleep 0.5",
            depends_on=["任务 2"]
        )

        self.orchestrator.add_task(task1)
        self.orchestrator.add_task(task2)
        self.orchestrator.add_task(task3)

        self.orchestrator.set_collaboration_mode(CollaborationMode.SEQUENTIAL)

        start_time = time.time()
        results = self.orchestrator.execute()
        duration = time.time() - start_time

        # 串行执行，3 个任务应该 >= 1.5 秒
        self.assertGreaterEqual(duration, 1.5)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r.success for r in results))

    def test_generate_report(self):
        """测试生成报告"""
        task = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="报告测试",
            description="测试报告生成",
            command="echo '测试输出'"
        )

        self.orchestrator.add_task(task)
        self.orchestrator.execute()

        report = self.orchestrator.generate_report()

        self.assertIn("子智能体执行报告", report)
        self.assertIn("报告测试", report)
        self.assertIn("✅ 成功", report)

    def test_save_report(self):
        """测试保存报告"""
        import os
        import tempfile

        task = SubagentTask(
            role=AgentRole.DOC_WRITER,
            name="保存测试",
            description="测试报告保存",
            command="echo '测试'"
        )

        self.orchestrator.add_task(task)
        self.orchestrator.execute()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            self.orchestrator.save_report(tmp_path)

            self.assertTrue(os.path.exists(tmp_path))

            with open(tmp_path, 'r') as f:
                content = f.read()

            self.assertIn("子智能体执行报告", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSubagentOrchestrator)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
