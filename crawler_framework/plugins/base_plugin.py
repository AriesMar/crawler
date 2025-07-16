"""
插件基类
Base plugin class for the crawler framework
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..utils.logger import get_logger

class BasePlugin(ABC):
    """插件基类"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.logger = get_logger(f"Plugin.{name}")
        self.enabled = True
        self.config = {}
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        初始化插件
        
        Args:
            config: 插件配置
            
        Returns:
            初始化是否成功
        """
        pass
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行插件逻辑
        
        Args:
            data: 输入数据
            
        Returns:
            处理后的数据
        """
        pass
    
    def cleanup(self) -> bool:
        """
        清理插件资源
        
        Returns:
            清理是否成功
        """
        try:
            self.logger.info(f"插件 {self.name} 清理完成")
            return True
        except Exception as e:
            self.logger.error(f"插件 {self.name} 清理失败: {str(e)}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取插件信息
        
        Returns:
            插件信息字典
        """
        return {
            'name': self.name,
            'version': self.version,
            'enabled': self.enabled,
            'description': getattr(self, 'description', 'No description')
        }
    
    def enable(self):
        """启用插件"""
        self.enabled = True
        self.logger.info(f"插件 {self.name} 已启用")
    
    def disable(self):
        """禁用插件"""
        self.enabled = False
        self.logger.info(f"插件 {self.name} 已禁用")
    
    def is_enabled(self) -> bool:
        """检查插件是否启用"""
        return self.enabled 