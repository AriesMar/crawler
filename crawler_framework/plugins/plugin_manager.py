"""
插件管理器
Plugin manager for the crawler framework
"""

import os
import importlib.util
import inspect
from typing import Dict, List, Any, Type, Optional
from .base_plugin import BasePlugin
from ..utils.logger import get_logger

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.logger = get_logger("PluginManager")
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """
        注册插件
        
        Args:
            plugin: 插件实例
            
        Returns:
            注册是否成功
        """
        try:
            if not isinstance(plugin, BasePlugin):
                self.logger.error(f"插件 {plugin.name} 不是BasePlugin的实例")
                return False
            
            if plugin.name in self.plugins:
                self.logger.warning(f"插件 {plugin.name} 已存在，将被覆盖")
            
            self.plugins[plugin.name] = plugin
            self.logger.info(f"插件 {plugin.name} 注册成功")
            return True
            
        except Exception as e:
            self.logger.error(f"注册插件 {plugin.name} 失败: {str(e)}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        注销插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            注销是否成功
        """
        try:
            if plugin_name not in self.plugins:
                self.logger.warning(f"插件 {plugin_name} 不存在")
                return False
            
            plugin = self.plugins[plugin_name]
            plugin.cleanup()
            del self.plugins[plugin_name]
            
            self.logger.info(f"插件 {plugin_name} 注销成功")
            return True
            
        except Exception as e:
            self.logger.error(f"注销插件 {plugin_name} 失败: {str(e)}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        获取插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            插件实例
        """
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, BasePlugin]:
        """
        获取所有插件
        
        Returns:
            插件字典
        """
        return self.plugins.copy()
    
    def get_enabled_plugins(self) -> Dict[str, BasePlugin]:
        """
        获取所有启用的插件
        
        Returns:
            启用的插件字典
        """
        return {name: plugin for name, plugin in self.plugins.items() 
                if plugin.is_enabled()}
    
    def execute_plugin(self, plugin_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        执行指定插件
        
        Args:
            plugin_name: 插件名称
            data: 输入数据
            
        Returns:
            处理后的数据
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            self.logger.error(f"插件 {plugin_name} 不存在")
            return None
        
        if not plugin.is_enabled():
            self.logger.warning(f"插件 {plugin_name} 已禁用")
            return data
        
        try:
            result = plugin.execute(data)
            self.logger.info(f"插件 {plugin_name} 执行成功")
            return result
        except Exception as e:
            self.logger.error(f"插件 {plugin_name} 执行失败: {str(e)}")
            return data
    
    def execute_all_plugins(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行所有启用的插件
        
        Args:
            data: 输入数据
            
        Returns:
            处理后的数据
        """
        result = data.copy()
        
        for plugin_name, plugin in self.get_enabled_plugins().items():
            try:
                result = plugin.execute(result)
                self.logger.debug(f"插件 {plugin_name} 执行完成")
            except Exception as e:
                self.logger.error(f"插件 {plugin_name} 执行失败: {str(e)}")
        
        return result
    
    def load_plugins_from_directory(self, directory: str) -> int:
        """
        从目录加载插件
        
        Args:
            directory: 插件目录路径
            
        Returns:
            加载的插件数量
        """
        if not os.path.exists(directory):
            self.logger.error(f"插件目录 {directory} 不存在")
            return 0
        
        loaded_count = 0
        
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]
                try:
                    # 动态导入插件模块
                    module_path = os.path.join(directory, filename)
                    spec = importlib.util.spec_from_file_location(plugin_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 查找插件类
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, BasePlugin) and 
                            obj != BasePlugin):
                            plugin_instance = obj()
                            if self.register_plugin(plugin_instance):
                                loaded_count += 1
                                break
                    
                except Exception as e:
                    self.logger.error(f"加载插件 {plugin_name} 失败: {str(e)}")
        
        self.logger.info(f"从目录 {directory} 加载了 {loaded_count} 个插件")
        return loaded_count
    
    def initialize_plugins(self, config: Dict[str, Any]) -> bool:
        """
        初始化所有插件
        
        Args:
            config: 配置字典
            
        Returns:
            初始化是否成功
        """
        success_count = 0
        total_count = len(self.plugins)
        
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin_config = config.get(plugin_name, {})
                if plugin.initialize(plugin_config):
                    success_count += 1
                    self.logger.info(f"插件 {plugin_name} 初始化成功")
                else:
                    self.logger.error(f"插件 {plugin_name} 初始化失败")
            except Exception as e:
                self.logger.error(f"插件 {plugin_name} 初始化异常: {str(e)}")
        
        self.logger.info(f"插件初始化完成: {success_count}/{total_count} 成功")
        return success_count == total_count
    
    def cleanup_all_plugins(self):
        """清理所有插件"""
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin.cleanup()
            except Exception as e:
                self.logger.error(f"清理插件 {plugin_name} 失败: {str(e)}")
        
        self.plugins.clear()
        self.logger.info("所有插件已清理") 