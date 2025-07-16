"""
辅助工具函数
Helper utility functions
"""

import re
import hashlib
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, Any

def clean_text(text: str) -> str:
    """
    清理文本内容
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()\[\]{}"\'-]', '', text)
    
    return text

def extract_domain(url: str) -> Optional[str]:
    """
    从URL中提取域名
    
    Args:
        url: 完整URL
        
    Returns:
        域名
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc
    except Exception:
        return None

def generate_filename(prefix: str = "crawler", extension: str = "json") -> str:
    """
    生成文件名
    
    Args:
        prefix: 文件名前缀
        extension: 文件扩展名
        
    Returns:
        生成的文件名
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def extract_urls_from_text(text: str) -> list:
    """
    从文本中提取URL
    
    Args:
        text: 包含URL的文本
        
    Returns:
        URL列表
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)

def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename.strip('_.')

def calculate_hash(content: str) -> str:
    """
    计算内容的MD5哈希值
    
    Args:
        content: 要计算哈希的内容
        
    Returns:
        MD5哈希值
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并两个字典，dict2的值会覆盖dict1的值
    
    Args:
        dict1: 第一个字典
        dict2: 第二个字典
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    result.update(dict2)
    return result

def chunk_list(lst: list, chunk_size: int) -> list:
    """
    将列表分块
    
    Args:
        lst: 要分块的列表
        chunk_size: 每块的大小
        
    Returns:
        分块后的列表
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}" 