"""
微信公众号爬虫
WeChat Official Account article crawler
"""

import re
import time
import json
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from ..core.base_crawler import BaseCrawler
from ..config import Config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class WeChatCrawler(BaseCrawler):
    """微信公众号文章爬虫"""
    
    def __init__(self, storage_type: str = 'json'):
        super().__init__(storage_type)
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={Config.WECHAT_USER_AGENT}')
            
            # 设置代理
            proxy = Config.get_proxy()
            if proxy:
                chrome_options.add_argument(f'--proxy-server={proxy}')
            
            # 自动下载并设置ChromeDriver
            driver_path = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(driver_path, options=chrome_options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            logger.info("Chrome浏览器驱动初始化成功")
            
        except Exception as e:
            logger.error(f"Chrome浏览器驱动初始化失败: {str(e)}")
            raise
    
    def get_urls(self) -> List[str]:
        """获取要爬取的URL列表"""
        # 这里可以返回一些示例的微信公众号文章URL
        # 实际使用时，你需要提供真实的微信公众号文章URL
        return [
            # 示例URL，需要替换为真实的微信公众号文章URL
            # "https://mp.weixin.qq.com/s/example1",
            # "https://mp.weixin.qq.com/s/example2",
        ]
    
    def parse(self, response) -> Dict[str, Any]:
        """解析微信公众号文章页面"""
        try:
            # 对于微信公众号文章，我们需要使用Selenium来获取动态内容
            url = response.url
            return self._parse_wechat_article(url)
        except Exception as e:
            logger.error(f"解析微信公众号文章失败: {str(e)}")
            return {}
    
    def _parse_wechat_article(self, url: str) -> Dict[str, Any]:
        """解析微信公众号文章"""
        try:
            self.driver.get(url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rich_media_content"))
            )
            
            # 滚动页面以加载所有内容
            self._scroll_page()
            
            # 获取文章信息
            article_data = {
                'title': self._get_title(),
                'author': self._get_author(),
                'publish_time': self._get_publish_time(),
                'content': self._get_content(),
                'summary': self._get_summary(),
                'images': self._get_images(),
                'tags': self._get_tags(),
                'read_count': self._get_read_count(),
                'like_count': self._get_like_count(),
                'account_name': self._get_account_name(),
                'account_id': self._get_account_id(),
            }
            
            # 清理数据
            article_data = {k: v for k, v in article_data.items() if v is not None}
            
            return article_data
            
        except TimeoutException:
            logger.error(f"页面加载超时: {url}")
            return {}
        except Exception as e:
            logger.error(f"解析文章失败: {url} - {str(e)}")
            return {}
    
    def _scroll_page(self):
        """滚动页面以加载所有内容"""
        try:
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 滚动到页面顶部
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        except Exception as e:
            logger.warning(f"页面滚动失败: {str(e)}")
    
    def _get_title(self) -> Optional[str]:
        """获取文章标题"""
        try:
            title_element = self.driver.find_element(By.CLASS_NAME, "rich_media_title")
            return title_element.text.strip()
        except NoSuchElementException:
            return None
    
    def _get_author(self) -> Optional[str]:
        """获取作者信息"""
        try:
            author_element = self.driver.find_element(By.CLASS_NAME, "rich_media_meta_text")
            return author_element.text.strip()
        except NoSuchElementException:
            return None
    
    def _get_publish_time(self) -> Optional[str]:
        """获取发布时间"""
        try:
            time_element = self.driver.find_element(By.CLASS_NAME, "rich_media_meta_text")
            time_text = time_element.text.strip()
            # 提取时间信息
            time_match = re.search(r'\d{4}-\d{2}-\d{2}', time_text)
            if time_match:
                return time_match.group()
            return time_text
        except NoSuchElementException:
            return None
    
    def _get_content(self) -> Optional[str]:
        """获取文章内容"""
        try:
            content_element = self.driver.find_element(By.CLASS_NAME, "rich_media_content")
            return content_element.text.strip()
        except NoSuchElementException:
            return None
    
    def _get_summary(self) -> Optional[str]:
        """获取文章摘要"""
        try:
            # 尝试获取文章摘要
            summary_element = self.driver.find_element(By.CLASS_NAME, "rich_media_meta_desc")
            return summary_element.text.strip()
        except NoSuchElementException:
            # 如果没有摘要，从内容中提取前100个字符
            content = self._get_content()
            if content:
                return content[:100] + "..." if len(content) > 100 else content
            return None
    
    def _get_images(self) -> List[str]:
        """获取文章中的图片URL"""
        try:
            content_element = self.driver.find_element(By.CLASS_NAME, "rich_media_content")
            img_elements = content_element.find_elements(By.TAG_NAME, "img")
            
            images = []
            for img in img_elements:
                src = img.get_attribute("data-src") or img.get_attribute("src")
                if src:
                    images.append(src)
            
            return images
        except NoSuchElementException:
            return []
    
    def _get_tags(self) -> List[str]:
        """获取文章标签"""
        try:
            # 微信公众号文章通常没有明显的标签
            # 这里可以根据内容关键词提取标签
            content = self._get_content()
            if content:
                # 简单的关键词提取（实际项目中可以使用更复杂的NLP方法）
                keywords = ['技术', '产品', '运营', '设计', '营销', '数据', 'AI', '人工智能']
                tags = [kw for kw in keywords if kw in content]
                return tags[:5]  # 最多返回5个标签
            return []
        except Exception:
            return []
    
    def _get_read_count(self) -> Optional[int]:
        """获取阅读数"""
        try:
            # 微信公众号文章的阅读数通常需要特殊权限才能获取
            # 这里返回None，实际使用时可能需要其他方法
            return None
        except Exception:
            return None
    
    def _get_like_count(self) -> Optional[int]:
        """获取点赞数"""
        try:
            # 微信公众号文章的点赞数通常需要特殊权限才能获取
            # 这里返回None，实际使用时可能需要其他方法
            return None
        except Exception:
            return None
    
    def _get_account_name(self) -> Optional[str]:
        """获取公众号名称"""
        try:
            account_element = self.driver.find_element(By.CLASS_NAME, "rich_media_meta_nickname")
            return account_element.text.strip()
        except NoSuchElementException:
            return None
    
    def _get_account_id(self) -> Optional[str]:
        """获取公众号ID"""
        try:
            # 从URL中提取公众号ID
            url = self.driver.current_url
            match = re.search(r'__biz=([^&]+)', url)
            if match:
                return match.group(1)
            return None
        except Exception:
            return None
    
    def crawl_wechat_articles(self, urls: List[str]) -> List[Dict[str, Any]]:
        """爬取微信公众号文章"""
        results = []
        
        for i, url in enumerate(urls, 1):
            try:
                logger.info(f"正在爬取微信公众号文章 ({i}/{len(urls)}): {url}")
                
                article_data = self._parse_wechat_article(url)
                
                if article_data:
                    article_data['url'] = url
                    article_data['crawled_at'] = self._get_current_time()
                    
                    # 保存数据
                    self.storage.save(article_data, 'wechat_articles')
                    results.append(article_data)
                    
                    logger.success(f"成功爬取微信公众号文章: {url}")
                else:
                    logger.warning(f"解析微信公众号文章数据为空: {url}")
                    
            except Exception as e:
                logger.error(f"爬取微信公众号文章失败: {url} - {str(e)}")
                continue
        
        return results
    
    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
        super().close() 