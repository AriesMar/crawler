"""
验证工具函数
Validation utility functions
"""

import re
import urllib.parse
from typing import Optional, List, Dict, Any

def validate_url(url: str) -> bool:
    """
    验证URL格式是否正确
    
    Args:
        url: 要验证的URL
        
    Returns:
        是否有效
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 要验证的邮箱
        
    Returns:
        是否有效
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 要验证的手机号
        
    Returns:
        是否有效
    """
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_ip(ip: str) -> bool:
    """
    验证IP地址格式
    
    Args:
        ip: 要验证的IP地址
        
    Returns:
        是否有效
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
    """
    验证日期格式
    
    Args:
        date_str: 日期字符串
        format_str: 日期格式
        
    Returns:
        是否有效
    """
    try:
        from datetime import datetime
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False

def validate_json_structure(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    验证JSON数据结构
    
    Args:
        data: 要验证的数据
        required_fields: 必需字段列表
        
    Returns:
        是否有效
    """
    if not isinstance(data, dict):
        return False
    
    return all(field in data for field in required_fields)

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    验证文件扩展名
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名列表
        
    Returns:
        是否有效
    """
    if not filename:
        return False
    
    extension = filename.lower().split('.')[-1] if '.' in filename else ''
    return extension in [ext.lower() for ext in allowed_extensions]

def validate_string_length(text: str, min_length: int = 0, max_length: int = None) -> bool:
    """
    验证字符串长度
    
    Args:
        text: 要验证的字符串
        min_length: 最小长度
        max_length: 最大长度
        
    Returns:
        是否有效
    """
    if not isinstance(text, str):
        return False
    
    length = len(text)
    if length < min_length:
        return False
    
    if max_length is not None and length > max_length:
        return False
    
    return True

def validate_numeric_range(value: Any, min_value: float = None, max_value: float = None) -> bool:
    """
    验证数值范围
    
    Args:
        value: 要验证的数值
        min_value: 最小值
        max_value: 最大值
        
    Returns:
        是否有效
    """
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        return False
    
    if min_value is not None and num_value < min_value:
        return False
    
    if max_value is not None and num_value > max_value:
        return False
    
    return True

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, str]:
    """
    验证必需字段，返回错误信息
    
    Args:
        data: 要验证的数据
        required_fields: 必需字段列表
        
    Returns:
        错误信息字典
    """
    errors = {}
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors[field] = f"字段 '{field}' 是必需的"
    
    return errors 