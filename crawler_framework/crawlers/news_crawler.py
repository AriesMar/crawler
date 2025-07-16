"""
新闻网站爬虫
News website crawler
"""

import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from ..core.base_crawler import BaseCrawler
from ..utils.logger import get_logger
from ..utils.helpers import clean_text, extract_domain

logger = get_logger(__name__)

class NewsCrawler(BaseCrawler):
    """新闻网站爬虫"""
    
    def __init__(self, storage_type: str = 'json'):
        super().__init__(storage_type)
        self.description = "通用新闻网站爬虫"
    
    def get_urls(self) -> List[str]:
        """获取要爬取的URL列表"""
        # 这里应该返回实际的新闻网站URL
        return [
            # 示例URL，需要替换为真实的新闻网站URL
            # "https://news.example.com/article1",
            # "https://news.example.com/article2",
        ]
    
    def parse(self, response) -> Dict[str, Any]:
        """解析新闻页面"""
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻信息
            news_data = {
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'author': self._extract_author(soup),
                'publish_time': self._extract_publish_time(soup),
                'category': self._extract_category(soup),
                'tags': self._extract_tags(soup),
                'images': self._extract_images(soup),
                'summary': self._extract_summary(soup),
                'source': extract_domain(response.url),
                'url': response.url
            }
            
            # 清理数据
            news_data = {k: v for k, v in news_data.items() if v is not None}
            
            return news_data
            
        except Exception as e:
            logger.error(f"解析新闻页面失败: {str(e)}")
            return {}
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """提取新闻标题"""
        selectors = [
            'h1',
            '.title',
            '.headline',
            'h1.title',
            'h1.headline',
            '[class*="title"]',
            '[class*="headline"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return clean_text(element.get_text())
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> Optional[str]:
        """提取新闻内容"""
        selectors = [
            '.content',
            '.article-content',
            '.story-content',
            '.post-content',
            '[class*="content"]',
            '[class*="article"]',
            '[class*="story"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # 移除脚本和样式标签
                for script in element(["script", "style"]):
                    script.decompose()
                
                return clean_text(element.get_text())
        
        return None
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """提取作者信息"""
        selectors = [
            '.author',
            '.byline',
            '[class*="author"]',
            '[class*="byline"]',
            '[rel="author"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return clean_text(element.get_text())
        
        return None
    
    def _extract_publish_time(self, soup: BeautifulSoup) -> Optional[str]:
        """提取发布时间"""
        selectors = [
            '.time',
            '.date',
            '.publish-time',
            '[class*="time"]',
            '[class*="date"]',
            'time',
            '[datetime]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # 优先使用datetime属性
                datetime_attr = element.get('datetime')
                if datetime_attr:
                    return datetime_attr
                
                return clean_text(element.get_text())
        
        return None
    
    def _extract_category(self, soup: BeautifulSoup) -> Optional[str]:
        """提取新闻分类"""
        selectors = [
            '.category',
            '.section',
            '[class*="category"]',
            '[class*="section"]',
            '.breadcrumb a'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return clean_text(element.get_text())
        
        return None
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """提取新闻标签"""
        selectors = [
            '.tags a',
            '.tag',
            '[class*="tag"]',
            '.keywords a'
        ]
        
        tags = []
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = clean_text(element.get_text())
                if tag and tag not in tags:
                    tags.append(tag)
        
        return tags[:10]  # 最多返回10个标签
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """提取新闻图片"""
        images = []
        
        # 查找图片标签
        img_elements = soup.find_all('img')
        for img in img_elements:
            src = img.get('src') or img.get('data-src')
            if src:
                # 处理相对URL
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://' + extract_domain(self.current_url) + src
                
                images.append(src)
        
        return images[:10]  # 最多返回10张图片
    
    def _extract_summary(self, soup: BeautifulSoup) -> Optional[str]:
        """提取新闻摘要"""
        selectors = [
            '.summary',
            '.excerpt',
            '.description',
            '[class*="summary"]',
            '[class*="excerpt"]',
            'meta[name="description"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if selector == 'meta[name="description"]':
                    return element.get('content')
                else:
                    return clean_text(element.get_text())
        
        # 如果没有找到摘要，从内容中提取前100个字符
        content = self._extract_content(soup)
        if content:
            return content[:100] + "..." if len(content) > 100 else content
        
        return None
    
    def crawl_news_articles(self, urls: List[str]) -> List[Dict[str, Any]]:
        """爬取新闻文章"""
        results = []
        
        for i, url in enumerate(urls, 1):
            try:
                logger.info(f"正在爬取新闻文章 ({i}/{len(urls)}): {url}")
                
                # 发送请求
                response = self.request_manager.get(url)
                
                # 解析数据
                news_data = self.parse(response)
                
                if news_data:
                    news_data['url'] = url
                    news_data['crawled_at'] = self._get_current_time()
                    
                    # 保存数据
                    self.storage.save(news_data, 'news_articles')
                    results.append(news_data)
                    
                    logger.success(f"成功爬取新闻文章: {url}")
                else:
                    logger.warning(f"解析新闻文章数据为空: {url}")
                    
            except Exception as e:
                logger.error(f"爬取新闻文章失败: {url} - {str(e)}")
                continue
        
        return results 