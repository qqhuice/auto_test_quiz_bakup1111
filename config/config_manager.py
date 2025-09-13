"""
配置管理器
负责读取和管理测试配置参数
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置数据字典
        """
        try:
            # 获取项目根目录
            project_root = Path(__file__).parent.parent
            config_path = project_root / self.config_file
            
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
                return config_data.get('test_config', {})
        except FileNotFoundError:
            print(f"配置文件 {self.config_file} 未找到，使用默认配置")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"配置文件解析错误: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            'browser': {
                'default': 'chrome',
                'headless': False,
                'implicit_wait': 10,
                'explicit_wait': 20
            },
            'urls': {
                'practice_home': 'https://practicetestautomation.com/practice/',
                'login_page': 'https://practicetestautomation.com/practice-test-login/',
                'exceptions_page': 'https://practicetestautomation.com/practice-test-exceptions/'
            },
            'test_data': {
                'login': {
                    'valid_username': 'student',
                    'valid_password': 'Password123',
                    'invalid_username': 'incorrectUser',
                    'invalid_password': 'incorrectPassword'
                }
            }
        }
    
    def get(self, key_path: str, default=None):
        """
        获取配置值
        
        Args:
            key_path: 配置键路径，使用点号分隔，如 'browser.default'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    # 便捷方法
    @property
    def browser_config(self) -> Dict[str, Any]:
        """获取浏览器配置"""
        return self.get('browser', {})
    
    @property
    def urls(self) -> Dict[str, str]:
        """获取URL配置"""
        return self.get('urls', {})
    
    @property
    def test_data(self) -> Dict[str, Any]:
        """获取测试数据"""
        return self.get('test_data', {})
    
    @property
    def login_data(self) -> Dict[str, str]:
        """获取登录测试数据"""
        return self.get('test_data.login', {})
    
    @property
    def screenshot_config(self) -> Dict[str, Any]:
        """获取截图配置"""
        return self.get('screenshot', {})
    
    @property
    def report_config(self) -> Dict[str, Any]:
        """获取报告配置"""
        return self.get('report', {})


# 全局配置实例
config = ConfigManager()
