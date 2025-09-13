"""
Behave环境配置文件
管理测试的前置和后置操作
"""
import os
import sys
from pathlib import Path
from loguru import logger

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.driver_manager import DriverManager
from utils.screenshot_utils import screenshot_utils


def before_all(context):
    """测试套件开始前的设置"""
    logger.info("=== 开始BDD测试套件 ===")
    
    # 确保必要的目录存在
    Path("reports").mkdir(exist_ok=True)
    Path("screenshots").mkdir(exist_ok=True)
    
    # 设置浏览器
    context.browser_name = os.environ.get('BROWSER', 'chrome')
    logger.info(f"使用浏览器: {context.browser_name}")


def before_scenario(context, scenario):
    """每个场景开始前的设置"""
    logger.info(f"=== 开始场景: {scenario.name} ===")
    
    # 创建WebDriver实例
    context.driver_manager = DriverManager()
    context.driver = context.driver_manager.create_driver(context.browser_name)
    
    # 设置截图工具
    context.screenshot_utils = screenshot_utils
    
    logger.info("WebDriver已创建")


def after_scenario(context, scenario):
    """每个场景结束后的清理"""
    logger.info(f"=== 结束场景: {scenario.name} ===")
    
    # 如果场景失败，截图
    if scenario.status == "failed":
        logger.error(f"场景失败: {scenario.name}")
        
        try:
            screenshot_path = context.screenshot_utils.take_failure_screenshot(
                context.driver,
                scenario.name,
                "场景失败",
                context.browser_name
            )
            
            if screenshot_path:
                logger.info(f"失败截图已保存: {screenshot_path}")
        except Exception as e:
            logger.error(f"保存失败截图时出错: {e}")
    else:
        logger.info(f"场景成功: {scenario.name}")
    
    # 关闭WebDriver
    if hasattr(context, 'driver_manager'):
        context.driver_manager.quit_driver()
        logger.info("WebDriver已关闭")


def after_all(context):
    """测试套件结束后的清理"""
    logger.info("=== BDD测试套件完成 ===")
    
    # 清理旧截图
    screenshot_utils.cleanup_old_screenshots(days=7)
