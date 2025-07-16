"""
日志工具
Logging utilities for the crawler framework
"""

import sys
import os
from loguru import logger
from ..config import Config

# 创建日志目录
os.makedirs('logs', exist_ok=True)

# 配置日志
logger.remove()  # 移除默认处理器

# 添加控制台输出
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=Config.LOG_LEVEL,
    colorize=True
)

# 添加文件输出
logger.add(
    "logs/crawler.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=Config.LOG_LEVEL,
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)

def get_logger(name: str = None):
    """获取logger实例"""
    return logger.bind(name=name) if name else logger 