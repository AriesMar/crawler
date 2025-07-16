"""
基础爬虫类
Base crawler class for the framework
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from .request_manager import RequestManager
from .data_storage import DataStorage
from ..utils.logger import get_logger

logger = get_logger(__name__)

class BaseCrawler(ABC):
    """基础爬虫类"""
    
    def __init__(self, storage_type: str = 'json'):
        self.request_manager = RequestManager()
        self.storage = DataStorage(storage_type)
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    def parse(self, response) -> Dict[str, Any]:
        """解析响应数据，子类必须实现"""
        pass
    
    @abstractmethod
    def get_urls(self) -> List[str]:
        """获取要爬取的URL列表，子类必须实现"""
        pass
    
    def crawl(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """执行爬虫任务"""
        if urls is None:
            urls = self.get_urls()
        
        results = []
        total_urls = len(urls)
        
        self.logger.info(f"开始爬取 {total_urls} 个URL")
        
        for i, url in enumerate(urls, 1):
            try:
                self.logger.info(f"正在爬取 ({i}/{total_urls}): {url}")
                
                # 发送请求
                response = self.request_manager.get(url)
                
                # 解析数据
                data = self.parse(response)
                
                if data:
                    # 添加URL信息
                    data['url'] = url
                    data['crawled_at'] = self._get_current_time()
                    
                    # 保存数据
                    self.storage.save(data, self.__class__.__name__.lower())
                    results.append(data)
                    
                    self.logger.success(f"成功爬取: {url}")
                else:
                    self.logger.warning(f"解析数据为空: {url}")
                    
            except Exception as e:
                self.logger.error(f"爬取失败: {url} - {str(e)}")
                continue
        
        self.logger.info(f"爬取完成，成功爬取 {len(results)}/{total_urls} 个URL")
        return results
    
    def crawl_batch(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """批量爬取并保存"""
        results = self.crawl(urls)
        
        if results:
            # 批量保存
            self.storage.save_batch(results, f"{self.__class__.__name__.lower()}_batch")
        
        return results
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def close(self):
        """关闭资源"""
        self.request_manager.close()
        self.storage.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 