"""
请求管理器
Request manager for handling HTTP requests
"""

import time
import random
import requests
from typing import Dict, Any, Optional
from fake_useragent import UserAgent
from ..config import Config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RequestManager:
    """请求管理器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
    
    def _setup_session(self):
        """设置session配置"""
        # 设置默认headers
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 设置代理
        proxy = Config.get_proxy()
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
    
    def get(self, url: str, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self._request('GET', url, headers=headers, **kwargs)
    
    def post(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送POST请求"""
        return self._request('POST', url, data=data, headers=headers, **kwargs)
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """发送请求的核心方法"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                # 更新User-Agent
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                kwargs['headers']['User-Agent'] = self.ua.random
                
                # 设置超时
                kwargs.setdefault('timeout', Config.REQUEST_TIMEOUT)
                
                logger.info(f"发送 {method} 请求到 {url} (尝试 {attempt + 1}/{Config.MAX_RETRIES})")
                
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                
                # 请求延迟
                if Config.REQUEST_DELAY > 0:
                    time.sleep(Config.REQUEST_DELAY + random.uniform(0, 0.5))
                
                logger.success(f"请求成功: {url}")
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{Config.MAX_RETRIES}): {url} - {str(e)}")
                
                if attempt == Config.MAX_RETRIES - 1:
                    logger.error(f"请求最终失败: {url}")
                    raise
                
                # 重试延迟
                time.sleep(2 ** attempt + random.uniform(0, 1))
    
    def close(self):
        """关闭session"""
        self.session.close() 