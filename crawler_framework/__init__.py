"""
Python通用爬虫框架
A Universal Python Web Crawler Framework
"""

__version__ = "1.0.0"
__author__ = "Crawler Framework Team"

from .core.base_crawler import BaseCrawler
from .core.request_manager import RequestManager
from .core.data_storage import DataStorage
from .utils.logger import get_logger

__all__ = [
    'BaseCrawler',
    'RequestManager', 
    'DataStorage',
    'get_logger'
] 