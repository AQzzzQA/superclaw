#!/usr/bin/env python3
"""
质量控制器 (Quality Controller)

Phase 2: 质量控制系统
负责验证子智能体输出质量并生成质量报告
"""

import json
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QualityMetric(Enum):
    """质量指标"""
    COMPLETENESS = "completeness"  # 完整性
    ACCURACY = "accuracy"  # 准确性
    CLARITY = "clarity"  # 清晰度
    CONSISTENCY = "consistency"  # 一致性
    RELEVANCE = "relevance"  # 相关性


@dataclass
class QualityCheck:
    """质量检查项"""
    metric: QualityMetric
    description: str
    passed: bool
    score: float  # 0.0 - 1.0
    details: str = ""
    suggestions: List[str] = field(default_factory=list)


@dataclass
class QualityReport:
    """质量报告"""
    subagent_name: str
    overall_score: float  # 0.0 - 1.0
    checks: List[QualityCheck]
    grade: str  # A, B, C, D, F
    status: str  # PASSED, FAILED, WARNING
    suggestions: List[str] = field(default_factory=list)


class QualityController:
    """质量控制器"""

    def __init__(self):
        self.reports: Dict[str, QualityReport] = {}

    def check_completeness(self, output: str, subagent_name: str) -> QualityCheck:
        """检查完整性"""
        if not output or len(output.strip()) == 0:
            return QualityCheck(
                metric=QualityMetric.COMPLETENESS,
                description="输出完整性",
                passed=False,
                score=0.0,
                details="输出为空",
                suggestions=["子智能体应该生成有意义的输出"]
            )

        # 检查是否包含关键信息
        output_length = len(output.strip())
        score = min(output_length / 100, 1.0)  # 假设 100 字符为完整

        passed = score >= 0.5

        return QualityCheck(
            metric=QualityMetric.COMPLETENESS,
            description="输出完整性",
            passed=passed,
            score=score,
            details=f"输出长度: {output_length} 字符"
        )

    def check_clarity(self, output: str, subagent_name: str) -> QualityCheck:
        """检查清晰度"""
        if not output:
            return QualityCheck(
                metric=QualityMetric.CLARITY,
                description="输出清晰度",
                passed=False,
                score=0.0,
                details="输出为空"
            )

        # 检查是否有乱码或特殊字符过多
        special_char_ratio = sum(1 for c in output if ord(c) > 127) / len(output)

        # 检查是否有格式良好的结构
        has_structure = (
            '\n' in output or  # 有换行
            ' ' in output  # 有空格
        )

        score = 1.0 - min(special_char_ratio, 0.5)  # 最多扣 0.5 分
        if has_structure:
            score += 0.1

        score = min(score, 1.0)
        passed = score >= 0.6

        suggestions = []
        if special_char_ratio > 0.3:
            suggestions.append("输出包含过多特殊字符，建议检查编码")

        return QualityCheck(
            metric=QualityMetric.CLARITY,
            description="输出清晰度",
            passed=passed,
            score=score,
            details=f"特殊字符比例: {special_char_ratio:.2%}",
            suggestions=suggestions
        )

    def check_consistency(self, output: str, subagent_name: str) -> QualityCheck:
        """检查一致性"""
        if not output:
            return QualityCheck(
                metric=QualityMetric.CONSISTENCY,
                description="输出一致性",
                passed=False,
                score=0.0,
                details="输出为空"
            )

        # 检查格式一致性（缩进、空格等）
        lines = output.split('\n')
        leading_spaces = [len(line) - len(line.lstrip()) for line in lines if line.strip()]

        if len(leading_spaces) < 2:
            return QualityCheck(
                metric=QualityMetric.CONSISTENCY,
                description="输出一致性",
                passed=True,
                score=1.0,
                details="单行输出，无需一致性检查"
            )

        # 检查缩进是否一致
        if len(set(leading_spaces)) == 1:
            score = 1.0
            passed = True
        else:
            # 计算缩进一致性
            unique_indents = len(set(leading_spaces))
        # 计算缩进一致性
        unique_indents = 1  # 默认值
        if len(set(leading_spaces)) == 1:
            score = 1.0
            passed = True
        else:
            # 计算缩进一致性
            unique_indents = len(set(leading_spaces))
            score = 1.0 - (unique_indents - 1) * 0.1
            score = max(score, 0.0)
            passed = score >= 0.7

        return QualityCheck(
            metric=QualityMetric.CONSISTENCY,
            description="输出一致性",
            passed=passed,
            score=score,
            details=f"缩进变体数: {unique_indents}"
        )

    def check_relevance(self, output: str, task_description: str, subagent_name: str) -> QualityCheck:
        """检查相关性"""
        if not output:
            return QualityCheck(
                metric=QualityMetric.RELEVANCE,
                description="输出相关性",
                passed=False,
                score=0.0,
                details="输出为空"
            )

        # 提取任务关键词
        keywords = re.findall(r'\b\w+\b', task_description.lower())
        output_lower = output.lower()

        # 计算匹配关键词数量
        matches = sum(1 for keyword in keywords if keyword in output_lower)

        if len(keywords) == 0:
            return QualityCheck(
                metric=QualityMetric.RELEVANCE,
                description="输出相关性",
                passed=True,
                score=1.0,
                details="任务描述无关键词，无法评估相关性"
            )

        score = matches / len(keywords)
        passed = score >= 0.3

        return QualityCheck(
            metric=QualityMetric.RELEVANCE,
            description="输出相关性",
            passed=passed,
            score=score,
            details=f"关键词匹配: {matches}/{len(keywords)}"
        )

    def generate_quality_report(self, subagent_name: str, output: str,
                             task_description: str) -> QualityReport:
        """生成质量报告"""
        logger.info(f"生成子智能体质量报告: {subagent_name}")

        # 执行所有检查
        checks = []

        # 1. 完整性检查
        completeness_check = self.check_completeness(output, subagent_name)
        checks.append(completeness_check)

        # 2. 清晰度检查
        clarity_check = self.check_clarity(output, subagent_name)
        checks.append(clarity_check)

        # 3. 一致性检查
        consistency_check = self.check_consistency(output, subagent_name)
        checks.append(consistency_check)

        # 4. 相关性检查
        relevance_check = self.check_relevance(output, task_description, subagent_name)
        checks.append(relevance_check)

        # 计算总体评分
        overall_score = sum(check.score for check in checks) / len(checks)

        # 生成等级
        if overall_score >= 0.9:
            grade = 'A'
            status = 'PASSED'
        elif overall_score >= 0.8:
            grade = 'B'
            status = 'PASSED'
        elif overall_score >= 0.7:
            grade = 'C'
            status = 'WARNING'
        elif overall_score >= 0.6:
            grade = 'D'
            status = 'WARNING'
        else:
            grade = 'F'
            status = 'FAILED'

        # 收集所有建议
        all_suggestions = []
        for check in checks:
            all_suggestions.extend(check.suggestions)

        # 生成报告
        report = QualityReport(
            subagent_name=subagent_name,
            overall_score=overall_score,
            checks=checks,
            grade=grade,
            status=status,
            suggestions=all_suggestions
        )

        self.reports[subagent_name] = report
        return report

    def generate_summary_report(self) -> str:
        """生成汇总报告"""
        if not self.reports:
            return "没有可用的质量报告"

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("子智能体质量控制报告")
        report_lines.append("=" * 60)
        report_lines.append("")

        total_score = 0
        passed_count = 0
        warning_count = 0
        failed_count = 0

        for subagent_name, report in self.reports.items():
            report_lines.append("-" * 60)
            report_lines.append(f"子智能体: {report.subagent_name}")
            report_lines.append(f"总体评分: {report.overall_score:.2f} / 1.00")
            report_lines.append(f"等级: {report.grade}")
            report_lines.append(f"状态: {report.status}")
            report_lines.append("")

            for check in report.checks:
                status_icon = "✅" if check.passed else "❌"
                report_lines.append(f"  {status_icon} {check.description}: "
                                f"{check.score:.2f} - {check.details}")

                if check.suggestions:
                    for suggestion in check.suggestions:
                        report_lines.append(f"      💡 {suggestion}")

            report_lines.append("")

            if report.suggestions:
                report_lines.append("  💡 整体建议:")
                for suggestion in report.suggestions:
                    report_lines.append(f"      - {suggestion}")
                report_lines.append("")

            # 统计
            total_score += report.overall_score
            if report.status == 'PASSED':
                passed_count += 1
            elif report.status == 'WARNING':
                warning_count += 1
            else:
                failed_count += 1

        # 汇总统计
        total_subagents = len(self.reports)
        avg_score = total_score / total_subagents if total_subagents > 0 else 0

        report_lines.append("=" * 60)
        report_lines.append("汇总统计")
        report_lines.append("=" * 60)
        report_lines.append(f"子智能体总数: {total_subagents}")
        report_lines.append(f"平均评分: {avg_score:.2f} / 1.00")
        report_lines.append(f"通过: {passed_count}")
        report_lines.append(f"警告: {warning_count}")
        report_lines.append(f"失败: {failed_count}")
        report_lines.append("")

        # 总体评级
        if avg_score >= 0.9:
            overall_grade = 'A - 优秀'
            overall_status = 'PASSED'
        elif avg_score >= 0.8:
            overall_grade = 'B - 良好'
            overall_status = 'PASSED'
        elif avg_score >= 0.7:
            overall_grade = 'C - 中等'
            overall_status = 'WARNING'
        elif avg_score >= 0.6:
            overall_grade = 'D - 较差'
            overall_status = 'WARNING'
        else:
            overall_grade = 'F - 失败'
            overall_status = 'FAILED'

        report_lines.append(f"总体评级: {overall_grade}")
        report_lines.append(f"总体状态: {overall_status}")
        report_lines.append("")

        return "\n".join(report_lines)

    def save_report(self, filename: str) -> None:
        """保存报告到文件"""
        report = self.generate_summary_report()

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"质量报告已保存到: {filename}")


def main():
    """主函数 - 演示质量控制系统"""
    logger.info("=" * 60)
    logger.info("质量控制系统启动 (Phase 2)")
    logger.info("=" * 60)

    # 创建质量控制器
    controller = QualityController()

    # 模拟子智能体输出
    sample_outputs = {
        "代码审查员": "代码审查完成，发现 3 个潜在问题\n1. 缺少 docstring\n2. 行长超过 100\n3. 未使用的导入",
        "测试工程师": "测试运行完成\n- 运行 45 个测试\n- 通过 42 个\n- 失败 3 个\n- 覆盖率: 85%",
        "文档编写员": "文档生成成功\nREADME.md 已更新\nAPI.md 已创建\n贡献指南已完善",
        "安全审计员": "安全审计完成\n发现 1 个中风险漏洞\n0 个高风险漏洞\n建议升级 cryptography 库"
    }

    # 为每个子智能体生成质量报告
    task_descriptions = {
        "代码审查员": "检查代码质量和规范",
        "测试工程师": "运行单元测试并生成覆盖率报告",
        "文档编写员": "生成项目文档",
        "安全审计员": "检查依赖安全漏洞"
    }

    for subagent_name, output in sample_outputs.items():
        task_desc = task_descriptions.get(subagent_name, "")
        report = controller.generate_quality_report(subagent_name, output, task_desc)
        logger.info(f"子智能体 {subagent_name} 质量: {report.overall_score:.2f} ({report.grade})")

    # 生成汇总报告
    summary_report = controller.generate_summary_report()
    print("\n" + summary_report)

    # 保存报告
    report_file = "/root/.openclaw/workspace/quality-report.txt"
    controller.save_report(report_file)

    logger.info(f"\n质量报告已保存: {report_file}")
    logger.info("质量控制系统执行完成")


if __name__ == "__main__":
    main()
