#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架测试
Framework tests
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler_framework import BaseCrawler, RequestManager, DataStorage
from crawler_framework.utils.logger import get_logger
from crawler_framework.utils.helpers import clean_text, extract_domain, validate_url

logger = get_logger(__name__)

class TestCrawler(BaseCrawler):
    """测试爬虫类"""
    
    def get_urls(self):
        """返回测试URL"""
        return ["https://httpbin.org/get", "https://httpbin.org/json"]
    
    def parse(self, response):
        """解析测试响应"""
        try:
            if response.url.endswith('/get'):
                return {
                    'type': 'get_response',
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'url': response.url
                }
            elif response.url.endswith('/json'):
                return {
                    'type': 'json_response',
                    'data': response.json(),
                    'url': response.url
                }
            else:
                return {
                    'type': 'unknown',
                    'url': response.url
                }
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return {}

def test_request_manager():
    """测试请求管理器"""
    logger.info("测试请求管理器...")
    
    try:
        request_mgr = RequestManager()
        
        # 测试GET请求
        response = request_mgr.get("https://httpbin.org/get")
        assert response.status_code == 200
        logger.success("请求管理器GET请求测试通过")
        
        # 测试POST请求
        response = request_mgr.post("https://httpbin.org/post", data={"test": "data"})
        assert response.status_code == 200
        logger.success("请求管理器POST请求测试通过")
        
        request_mgr.close()
        return True
        
    except Exception as e:
        logger.error(f"请求管理器测试失败: {str(e)}")
        return False

def test_data_storage():
    """测试数据存储"""
    logger.info("测试数据存储...")
    
    try:
        # 测试JSON存储
        storage = DataStorage('json')
        test_data = {"test": "data", "number": 123}
        
        result = storage.save(test_data, "test_collection")
        assert result == True
        logger.success("JSON存储测试通过")
        
        # 测试批量存储
        test_data_list = [
            {"id": 1, "name": "test1"},
            {"id": 2, "name": "test2"}
        ]
        
        result = storage.save_batch(test_data_list, "test_batch")
        assert result == True
        logger.success("批量存储测试通过")
        
        storage.close()
        return True
        
    except Exception as e:
        logger.error(f"数据存储测试失败: {str(e)}")
        return False

def test_base_crawler():
    """测试基础爬虫"""
    logger.info("测试基础爬虫...")
    
    try:
        with TestCrawler(storage_type='json') as crawler:
            results = crawler.crawl()
            
            assert len(results) > 0
            logger.success(f"基础爬虫测试通过，成功爬取 {len(results)} 个URL")
            
            # 检查结果格式
            for result in results:
                assert 'url' in result
                assert 'crawled_at' in result
                assert 'type' in result
            
            return True
            
    except Exception as e:
        logger.error(f"基础爬虫测试失败: {str(e)}")
        return False

def test_utils():
    """测试工具函数"""
    logger.info("测试工具函数...")
    
    try:
        # 测试文本清理
        dirty_text = "  这是  一个  测试  文本  \n\n"
        clean_result = clean_text(dirty_text)
        assert clean_result == "这是 一个 测试 文本"
        logger.success("文本清理测试通过")
        
        # 测试域名提取
        url = "https://www.example.com/path?param=value"
        domain = extract_domain(url)
        assert domain == "www.example.com"
        logger.success("域名提取测试通过")
        
        # 测试URL验证
        valid_url = "https://www.example.com"
        invalid_url = "not-a-url"
        assert validate_url(valid_url) == True
        assert validate_url(invalid_url) == False
        logger.success("URL验证测试通过")
        
        return True
        
    except Exception as e:
        logger.error(f"工具函数测试失败: {str(e)}")
        return False

def test_logger():
    """测试日志系统"""
    logger.info("测试日志系统...")
    
    try:
        logger.debug("这是一条调试日志")
        logger.info("这是一条信息日志")
        logger.warning("这是一条警告日志")
        logger.error("这是一条错误日志")
        
        logger.success("日志系统测试通过")
        return True
        
    except Exception as e:
        logger.error(f"日志系统测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    logger.info("=" * 50)
    logger.info("开始爬虫框架测试")
    logger.info("=" * 50)
    
    # 创建必要的目录
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # 运行测试
    tests = [
        ("日志系统", test_logger),
        ("工具函数", test_utils),
        ("请求管理器", test_request_manager),
        ("数据存储", test_data_storage),
        ("基础爬虫", test_base_crawler),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n开始测试: {test_name}")
        try:
            if test_func():
                passed += 1
                logger.success(f"{test_name} 测试通过")
            else:
                logger.error(f"{test_name} 测试失败")
        except Exception as e:
            logger.error(f"{test_name} 测试异常: {str(e)}")
    
    logger.info("=" * 50)
    logger.info(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        logger.success("所有测试通过！爬虫框架工作正常。")
        return 0
    else:
        logger.error("部分测试失败，请检查相关功能。")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 