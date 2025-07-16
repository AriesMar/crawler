#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础使用示例
Basic usage example
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler_framework import WeChatCrawler, NewsCrawler
from crawler_framework.utils.logger import get_logger

logger = get_logger(__name__)

def create_directories():
    """创建必要的目录"""
    directories = ['logs', 'data', 'downloads']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def example_wechat_crawler():
    """微信公众号爬虫示例"""
    logger.info("开始微信公众号爬虫示例")
    
    # 示例URL列表（需要替换为真实的微信公众号文章URL）
    wechat_urls = [
        # 这里需要添加真实的微信公众号文章URL
        # "https://mp.weixin.qq.com/s/example1",
        # "https://mp.weixin.qq.com/s/example2",
    ]
    
    if not wechat_urls:
        logger.warning("请提供真实的微信公众号文章URL")
        return
    
    try:
        # 使用上下文管理器确保资源正确释放
        with WeChatCrawler(storage_type='json') as crawler:
            # 爬取微信公众号文章
            results = crawler.crawl_wechat_articles(wechat_urls)
            
            logger.info(f"成功爬取 {len(results)} 篇文章")
            
            # 打印结果摘要
            for i, article in enumerate(results, 1):
                logger.info(f"文章 {i}:")
                logger.info(f"  标题: {article.get('title', 'N/A')}")
                logger.info(f"  作者: {article.get('author', 'N/A')}")
                logger.info(f"  发布时间: {article.get('publish_time', 'N/A')}")
                logger.info(f"  公众号: {article.get('account_name', 'N/A')}")
                logger.info(f"  内容长度: {len(article.get('content', ''))} 字符")
                logger.info(f"  图片数量: {len(article.get('images', []))}")
                logger.info("---")
    
    except Exception as e:
        logger.error(f"微信公众号爬虫示例失败: {str(e)}")

def example_news_crawler():
    """新闻爬虫示例"""
    logger.info("开始新闻爬虫示例")
    
    # 示例URL列表（需要替换为真实的新闻网站URL）
    news_urls = [
        # 这里需要添加真实的新闻网站URL
        # "https://news.example.com/article1",
        # "https://news.example.com/article2",
    ]
    
    if not news_urls:
        logger.warning("请提供真实的新闻网站URL")
        return
    
    try:
        # 使用上下文管理器确保资源正确释放
        with NewsCrawler(storage_type='csv') as crawler:
            # 爬取新闻文章
            results = crawler.crawl_news_articles(news_urls)
            
            logger.info(f"成功爬取 {len(results)} 篇新闻")
            
            # 打印结果摘要
            for i, news in enumerate(results, 1):
                logger.info(f"新闻 {i}:")
                logger.info(f"  标题: {news.get('title', 'N/A')}")
                logger.info(f"  作者: {news.get('author', 'N/A')}")
                logger.info(f"  发布时间: {news.get('publish_time', 'N/A')}")
                logger.info(f"  分类: {news.get('category', 'N/A')}")
                logger.info(f"  内容长度: {len(news.get('content', ''))} 字符")
                logger.info("---")
    
    except Exception as e:
        logger.error(f"新闻爬虫示例失败: {str(e)}")

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("爬虫框架基础使用示例")
    logger.info("=" * 50)
    
    # 创建必要的目录
    create_directories()
    
    # 运行示例
    example_wechat_crawler()
    example_news_crawler()
    
    logger.info("示例程序执行完成")

if __name__ == "__main__":
    main() 