#!/usr/bin/env python3
"""
DSP平台安全配置检查清单
快速检查生产环境安全配置是否符合要求
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class SecurityChecker:
    """安全配置检查器"""

    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []

    def check(self):
        """执行所有安全检查"""
        print("🔒 DSP平台安全配置检查")
        print("=" * 60)

        # 1. 环境配置检查
        self.check_environment()

        # 2. 依赖安全检查
        self.check_dependencies()

        # 3. 文件权限检查
        self.check_file_permissions()

        # 4. 数据库配置检查
        self.check_database()

        # 5. 日志配置检查
        self.check_logging()

        # 6. 输出报告
        self.print_report()

    def check_environment(self):
        """检查环境变量配置"""
        print("\n📋 1. 环境配置检查")

        # 检查.env文件
        env_file = Path(".env")
        if not env_file.exists():
            self.warnings.append(".env文件不存在，请创建配置文件")
            return

        env_vars = {}
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()

        # 检查DEBUG模式
        if env_vars.get("DEBUG", "False").lower() == "true":
            self.issues.append("❌ DEBUG模式在生产环境中启用")
        else:
            self.passed.append("✅ DEBUG模式已禁用")

        # 检查JWT密钥
        jwt_secret = env_vars.get("JWT_SECRET_KEY", "")
        if len(jwt_secret) < 32:
            self.issues.append("❌ JWT_SECRET_KEY长度不足（至少32位）")
        elif jwt_secret in ["your-secret-key", "dev-secret-key", "change-in-production"]:
            self.issues.append("❌ JWT_SECRET_KEY使用默认值，请更换")
        else:
            self.passed.append("✅ JWT_SECRET_KEY配置正确")

        # 检查HTTPS强制
        if env_vars.get("FORCE_HTTPS", "False").lower() != "true":
            self.warnings.append("⚠️ HTTPS未强制启用")
        else:
            self.passed.append("✅ HTTPS强制启用")

        # 检查数据库密码强度
        db_password = env_vars.get("DATABASE_PASSWORD", "")
        if len(db_password) < 12:
            self.warnings.append("⚠️ 数据库密码强度不足（建议12位以上）")
        else:
            self.passed.append("✅ 数据库密码强度达标")

        # 检查日志脱敏
        if env_vars.get("LOG_MASKING_ENABLED", "False").lower() != "true":
            self.warnings.append("⚠️ 日志脱敏未启用")
        else:
            self.passed.append("✅ 日志脱敏已启用")

        # 检查Redis密码
        redis_password = env_vars.get("REDIS_PASSWORD", "")
        if not redis_password:
            self.issues.append("❌ Redis未设置密码")
        else:
            self.passed.append("✅ Redis密码已设置")

    def check_dependencies(self):
        """检查依赖安全性"""
        print("\n📋 2. 依赖安全检查")

        # 检查Python依赖
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.passed.append("✅ Python依赖无已知漏洞")
            else:
                self.issues.append(f"❌ Python依赖存在漏洞: {result.stdout[:200]}")
        except FileNotFoundError:
            self.warnings.append("⚠️ safety未安装，跳过Python依赖检查")
        except subprocess.TimeoutExpired:
            self.warnings.append("⚠️ safety检查超时")

        # 检查Node.js依赖（如果存在）
        package_json = Path("frontend/package.json")
        if package_json.exists():
            try:
                result = subprocess.run(
                    ["npm", "audit", "--json"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                # npm audit返回非0表示有问题
                if "vulnerabilities" in result.stdout:
                    import json
                    audit_data = json.loads(result.stdout)
                    vulnerabilities = audit_data.get("vulnerabilities", {})

                    if vulnerabilities:
                        total = sum(v.get("count", 0) for v in vulnerabilities.values())
                        if total > 0:
                            self.issues.append(f"❌ Node.js依赖存在{total}个漏洞")
                        else:
                            self.passed.append("✅ Node.js依赖无已知漏洞")
            except FileNotFoundError:
                self.warnings.append("⚠️ npm未安装，跳过Node.js依赖检查")
            except subprocess.TimeoutExpired:
                self.warnings.append("⚠️ npm audit超时")

    def check_file_permissions(self):
        """检查文件权限"""
        print("\n📋 3. 文件权限检查")

        # 检查敏感文件权限
        sensitive_files = [
            ".env",
            "requirements.txt",
            "backend/requirements.txt"
        ]

        for file_path in sensitive_files:
            file = Path(file_path)
            if file.exists():
                # 获取文件权限
                stat = file.stat()
                mode = oct(stat.st_mode)[-3:]

                # 检查是否过于开放
                if mode in ["777", "775", "666"]:
                    self.issues.append(f"❌ {file_path} 权限过于开放 ({mode})")
                else:
                    self.passed.append(f"✅ {file_path} 权限正常 ({mode})")

        # 检查.env是否在.gitignore中
        gitignore = Path(".gitignore")
        if gitignore.exists():
            with open(gitignore) as f:
                content = f.read()
                if ".env" in content:
                    self.passed.append("✅ .env已在.gitignore中")
                else:
                    self.issues.append("❌ .env未在.gitignore中，可能泄露敏感信息")

    def check_database(self):
        """检查数据库配置"""
        print("\n📋 4. 数据库配置检查")

        # 检查是否使用MySQL
        try:
            import pymysql
            self.passed.append("✅ PyMySQL已安装")
        except ImportError:
            self.warnings.append("⚠️ PyMySQL未安装")

        # 检查SQLAlchemy配置
        config_file = Path("backend/app/core/config.py")
        if config_file.exists():
            content = config_file.read_text()

            # 检查是否使用参数化查询（基本检查）
            if "text(" in content or 'execute("' in content:
                self.warnings.append("⚠️ 检测到可能的原始SQL查询，建议使用ORM参数化查询")
            else:
                self.passed.append("✅ 未发现明显的原始SQL查询")

    def check_logging(self):
        """检查日志配置"""
        print("\n📋 5. 日志配置检查")

        # 检查日志目录
        logs_dir = Path("logs")
        if logs_dir.exists():
            self.passed.append("✅ 日志目录存在")
        else:
            self.warnings.append("⚠️ 日志目录不存在")

        # 检查是否配置了日志脱敏
        config_file = Path("backend/app/core/logging.py")
        if config_file.exists():
            content = config_file.read_text()
            if "mask" in content.lower() or "sensitive" in content.lower():
                self.passed.append("✅ 日志配置包含敏感数据处理")
            else:
                self.warnings.append("⚠️ 日志配置可能未脱敏敏感信息")

    def print_report(self):
        """输出检查报告"""
        print("\n" + "=" * 60)
        print("📊 检查报告")
        print("=" * 60)

        # 统计
        total = len(self.passed) + len(self.warnings) + len(self.issues)
        print(f"\n总检查项: {total}")
        print(f"✅ 通过: {len(self.passed)}")
        print(f"⚠️ 警告: {len(self.warnings)}")
        print(f"❌ 错误: {len(self.issues)}")

        # 详细报告
        if self.issues:
            print("\n❌ 错误项（必须修复）:")
            for issue in self.issues:
                print(f"  {issue}")

        if self.warnings:
            print("\n⚠️ 警告项（建议修复）:")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.passed:
            print("\n✅ 通过项:")
            for item in self.passed[:10]:  # 只显示前10个
                print(f"  {item}")
            if len(self.passed) > 10:
                print(f"  ... 还有{len(self.passed) - 10}项通过")

        # 退出码
        if self.issues:
            print("\n❌ 存在必须修复的错误项，请立即处理")
            sys.exit(1)
        elif self.warnings:
            print("\n⚠️ 存在警告项，建议尽快处理")
            sys.exit(2)
        else:
            print("\n✅ 所有检查项通过！")
            sys.exit(0)


def main():
    """主函数"""
    checker = SecurityChecker()
    checker.check()


if __name__ == "__main__":
    main()
