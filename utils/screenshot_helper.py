"""
截图辅助工具类
"""
import os
import time
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

class ScreenshotHelper:
    """截图辅助类"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        """
        初始化截图辅助类
        
        Args:
            screenshot_dir: 截图保存目录
        """
        self.screenshot_dir = screenshot_dir
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self):
        """确保截图目录存在"""
        try:
            os.makedirs(self.screenshot_dir, exist_ok=True)
            logger.debug(f"截图目录已准备: {self.screenshot_dir}")
        except Exception as e:
            logger.error(f"创建截图目录失败: {e}")
            # 使用默认目录
            self.screenshot_dir = "screenshots"
            os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, driver: WebDriver, description: str, browser_name: str = "chrome") -> str:
        """
        截图并保存
        
        Args:
            driver: WebDriver实例
            description: 截图描述
            browser_name: 浏览器名称
            
        Returns:
            截图文件路径
        """
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{description}_{browser_name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # 保存截图
            driver.save_screenshot(filepath)
            
            logger.info(f"📸 截图已保存: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"截图保存失败: {e}")
            return ""
    
    def take_screenshot_with_timestamp(self, driver: WebDriver, description: str) -> str:
        """
        带时间戳的截图
        
        Args:
            driver: WebDriver实例
            description: 截图描述
            
        Returns:
            截图文件路径
        """
        return self.take_screenshot(driver, description)
    
    def take_failure_screenshot(self, driver: WebDriver, test_name: str, error_msg: str = "") -> str:
        """
        失败时的截图
        
        Args:
            driver: WebDriver实例
            test_name: 测试名称
            error_msg: 错误信息
            
        Returns:
            截图文件路径
        """
        description = f"FAILED_{test_name}"
        if error_msg:
            # 清理错误信息中的特殊字符
            clean_error = "".join(c for c in error_msg[:50] if c.isalnum() or c in (' ', '_', '-'))
            description += f"_{clean_error}"
        
        return self.take_screenshot(driver, description)
    
    def take_success_screenshot(self, driver: WebDriver, test_name: str) -> str:
        """
        成功时的截图
        
        Args:
            driver: WebDriver实例
            test_name: 测试名称
            
        Returns:
            截图文件路径
        """
        description = f"SUCCESS_{test_name}"
        return self.take_screenshot(driver, description)
    
    def cleanup_old_screenshots(self, days_old: int = 7):
        """
        清理旧截图
        
        Args:
            days_old: 保留天数
        """
        try:
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            removed_count = 0
            for filename in os.listdir(self.screenshot_dir):
                filepath = os.path.join(self.screenshot_dir, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        removed_count += 1
            
            if removed_count > 0:
                logger.info(f"已清理 {removed_count} 个旧截图文件")
            
        except Exception as e:
            logger.error(f"清理旧截图失败: {e}")
    
    def get_screenshot_count(self) -> int:
        """
        获取截图数量
        
        Returns:
            截图文件数量
        """
        try:
            if not os.path.exists(self.screenshot_dir):
                return 0
            
            files = [f for f in os.listdir(self.screenshot_dir) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            return len(files)
            
        except Exception as e:
            logger.error(f"获取截图数量失败: {e}")
            return 0
    
    def get_latest_screenshot(self) -> str:
        """
        获取最新的截图文件路径
        
        Returns:
            最新截图文件路径
        """
        try:
            if not os.path.exists(self.screenshot_dir):
                return ""
            
            files = []
            for filename in os.listdir(self.screenshot_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(self.screenshot_dir, filename)
                    files.append((filepath, os.path.getmtime(filepath)))
            
            if not files:
                return ""
            
            # 按修改时间排序，返回最新的
            latest_file = max(files, key=lambda x: x[1])
            return latest_file[0]
            
        except Exception as e:
            logger.error(f"获取最新截图失败: {e}")
            return ""

# 创建全局实例
screenshot_helper = ScreenshotHelper()

# 便捷函数
def take_screenshot(driver: WebDriver, description: str, browser_name: str = "chrome") -> str:
    """便捷的截图函数"""
    return screenshot_helper.take_screenshot(driver, description, browser_name)

def take_failure_screenshot(driver: WebDriver, test_name: str, error_msg: str = "") -> str:
    """便捷的失败截图函数"""
    return screenshot_helper.take_failure_screenshot(driver, test_name, error_msg)

def take_success_screenshot(driver: WebDriver, test_name: str) -> str:
    """便捷的成功截图函数"""
    return screenshot_helper.take_success_screenshot(driver, test_name)
