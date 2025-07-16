"""
插件系统
Plugin system for the crawler framework
"""

from .base_plugin import BasePlugin
from .plugin_manager import PluginManager

__all__ = [
    'BasePlugin',
    'PluginManager'
] 