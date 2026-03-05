"""
日志配置
"""
import logging
import sys
from pathlib import Path
from app.core.settings import settings

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 日志格式
if settings.LOG_FORMAT == "json":
    log_format = (
        '{"time": "%(asctime)s", "level": "%(levelname)s", '
        '"name": "%(name)s", "message": "%(message)s"}'
    )
else:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

date_format = "%Y-%m-%d %H:%M:%S"

# 配置日志处理器
handlers = []

# 控制台输出
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(settings.LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(log_format, date_format))
handlers.append(console_handler)

# 文件输出
file_handler = logging.FileHandler(
    log_dir / f"{settings.APP_NAME}.log",
    encoding="utf-8"
)
file_handler.setLevel(settings.LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(log_format, date_format))
handlers.append(file_handler)

# 配置根日志记录器
logging.basicConfig(
    level=settings.LOG_LEVEL,
    handlers=handlers,
    datefmt=date_format,
    force=True
)

# 创建日志记录器
logger = logging.getLogger(settings.APP_NAME)
