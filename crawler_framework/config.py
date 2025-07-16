"""
配置管理
Configuration management for the crawler framework
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """爬虫框架配置类"""
    
    # 基础配置
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # 请求配置
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 1.0))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///crawler.db')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.getenv('MONGO_DB', 'crawler')
    
    # 文件存储配置
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', './downloads')
    
    # 代理配置
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_LIST = os.getenv('PROXY_LIST', '').split(',') if os.getenv('PROXY_LIST') else []
    
    # 微信公众号配置
    WECHAT_COOKIE = os.getenv('WECHAT_COOKIE', '')
    WECHAT_USER_AGENT = os.getenv('WECHAT_USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    
    @classmethod
    def get_proxy(cls):
        """获取代理配置"""
        if cls.USE_PROXY and cls.PROXY_LIST:
            import random
            return random.choice(cls.PROXY_LIST)
        return None 