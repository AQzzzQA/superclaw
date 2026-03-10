#!/usr/bin/env python3
"""
OpenClaw 与 OpenViking 记忆服务启动脚本
持续运行，提供服务接口
"""

import sys
import os
import asyncio
import signal
import logging
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from openclaw_memory_integration import OpenClawMemoryIntegration

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/openclaw-memory.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MemoryService:
    """记忆服务主类"""

    def __init__(self):
        self.integration = None
        self.running = False

    async def initialize(self):
        """初始化服务"""
        logger.info("初始化 OpenClaw 记忆服务...")

        # 从环境变量读取配置
        workspace = os.getenv("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
        openviking_url = os.getenv("OPENVIKING_URL", "http://localhost:1933")
        api_key = os.getenv("OPENVIKING_API_KEY")
        enable_fallback = os.getenv("OPENVIKING_ENABLE_FALLBACK", "true").lower() == "true"

        # 创建集成实例
        self.integration = OpenClawMemoryIntegration(
            workspace=workspace,
            openviking_url=openviking_url,
            api_key=api_key,
            enable_fallback=enable_fallback
        )

        logger.info(f"记忆服务初始化完成")
        logger.info(f"  - 工作目录: {workspace}")
        logger.info(f"  - OpenViking: {openviking_url}")
        logger.info(f"  - 降级模式: {enable_fallback}")

    async def start(self):
        """启动服务"""
        logger.info("启动 OpenClaw 记忆服务...")
        self.running = True

        # 测试服务
        try:
            stats = await self.integration.get_memory_stats()
            logger.info(f"记忆统计: 本地文件 {stats['local']['file_count']} 个, "
                       f"总大小 {stats['local']['total_size_mb']} MB")
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")

        logger.info("✅ 记忆服务已启动，正在运行...")

    async def stop(self):
        """停止服务"""
        logger.info("停止 OpenClaw 记忆服务...")
        self.running = False

        if self.integration:
            await self.integration.close()

        logger.info("✅ 记忆服务已停止")

    async def loop(self):
        """主循环"""
        while self.running:
            try:
                # 定期健康检查
                stats = await self.integration.get_memory_stats()
                logger.info(f"📊 记忆状态: 本地 {stats['local']['file_count']} 文件, "
                           f"{stats['local']['total_size_mb']} MB | "
                           f"OpenViking: {'✅' if 'openviking' in stats else '⚠️'}")

                # 等待 60 秒
                for _ in range(60):
                    if not self.running:
                        break
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"主循环错误: {e}")
                await asyncio.sleep(5)  # 错误后等待 5 秒

    async def cleanup(self):
        """定期清理旧记忆"""
        logger.info("开始清理旧记忆...")
        deleted = await self.integration.cleanup_old_memories(days=30)
        logger.info(f"清理完成: 删除了 {deleted} 个旧记忆")


# 全局服务实例
service = MemoryService()


async def main():
    """主函数"""
    # 初始化服务
    await service.initialize()

    # 启动服务
    await service.start()

    # 信号处理
    def signal_handler():
        logger.info("收到停止信号...")
        service.running = False

    # 注册信号处理器
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    # 主循环
    try:
        await service.loop()
    except Exception as e:
        logger.error(f"服务异常: {e}")
    finally:
        # 停止服务
        await service.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("收到键盘中断...")
    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)