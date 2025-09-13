"""
截图工具类
负责在测试过程中自动截图并保存
"""
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger
from config.config_manager import config


class ScreenshotUtils:
    """截图工具类"""
    
    def __init__(self, screenshot_dir: str = "screenshots", test_session_name: str = None):
        """
        初始化截图工具

        Args:
            screenshot_dir: 截图保存目录
            test_session_name: 测试会话名称，用于创建子文件夹
        """
        self.base_screenshot_dir = Path(screenshot_dir)
        self.screenshot_config = config.screenshot_config

        # 如果提供了测试会话名称，创建带时间戳的子文件夹
        if test_session_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.screenshot_dir = self.base_screenshot_dir / f"{test_session_name}_{timestamp}"
            logger.info(f"创建测试会话截图目录: {self.screenshot_dir}")
        else:
            self.screenshot_dir = self.base_screenshot_dir

        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """确保截图目录存在"""
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(self, driver: WebDriver, step_name: str, browser_name: str = "browser") -> str:
        """
        截取当前页面截图
        
        Args:
            driver: WebDriver实例
            step_name: 步骤名称
            browser_name: 浏览器名称
            
        Returns:
            截图文件路径
        """
        if not self.screenshot_config.get('enabled', True):
            return None
        
        try:
            # 生成截图文件名
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
            safe_step_name = self._sanitize_filename(step_name)
            filename = f"{safe_step_name}_{browser_name}_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # 截图
            driver.save_screenshot(str(filepath))
            
            logger.info(f"截图已保存: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    def take_failure_screenshot(self, driver: WebDriver, test_name: str, error_message: str, browser_name: str = "browser") -> str:
        """
        截取失败场景的截图
        
        Args:
            driver: WebDriver实例
            test_name: 测试名称
            error_message: 错误信息
            browser_name: 浏览器名称
            
        Returns:
            截图文件路径
        """
        safe_error = self._sanitize_filename(error_message[:50])  # 限制错误信息长度
        step_name = f"FAILURE_{test_name}_{safe_error}"
        return self.take_screenshot(driver, step_name, browser_name)
    
    def take_success_screenshot(self, driver: WebDriver, step_name: str, browser_name: str = "browser") -> str:
        """
        截取成功场景的截图
        
        Args:
            driver: WebDriver实例
            step_name: 步骤名称
            browser_name: 浏览器名称
            
        Returns:
            截图文件路径
        """
        if not self.screenshot_config.get('on_success', True):
            return None
        
        return self.take_screenshot(driver, f"SUCCESS_{step_name}", browser_name)
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除不合法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 移除或替换不合法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 移除多余的空格和下划线
        filename = '_'.join(filename.split())
        
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename
    
    def get_relative_path(self, full_path: str) -> str:
        """
        获取截图的相对路径（用于报告中显示）
        
        Args:
            full_path: 完整路径
            
        Returns:
            相对路径
        """
        if full_path is None:
            return None
        
        # 转换为相对路径
        try:
            path = Path(full_path)
            if path.is_absolute():
                # 尝试获取相对于项目根目录的路径
                project_root = Path.cwd()
                return str(path.relative_to(project_root))
            return str(path)
        except ValueError:
            # 如果无法获取相对路径，返回文件名
            return Path(full_path).name
    
    def cleanup_old_screenshots(self, days: int = 7):
        """
        清理旧的截图文件
        
        Args:
            days: 保留天数
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            for file_path in self.screenshot_dir.glob("*.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"已删除旧截图: {file_path}")
                    
        except Exception as e:
            logger.error(f"清理旧截图时出错: {e}")


# 全局截图工具实例
screenshot_utils = ScreenshotUtils()
