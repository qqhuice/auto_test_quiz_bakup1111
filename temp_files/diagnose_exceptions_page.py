#!/usr/bin/env python3
"""
异常页面诊断脚本
用于分析异常页面的实际元素结构，找出卡顿问题的根源
"""
import sys
from pathlib import Path
from loguru import logger

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.driver_manager import DriverManager
from pages.practice_home_page import PracticeHomePage
from selenium.webdriver.common.by import By
import time


def diagnose_exceptions_page():
    """诊断异常页面的元素结构"""
    logger.info("=== 开始诊断异常页面 ===")
    
    # 创建WebDriver
    driver_manager = DriverManager()
    driver = driver_manager.create_chrome_driver()
    
    try:
        # 1. 打开首页
        logger.info("步骤1: 打开首页")
        home_page = PracticeHomePage(driver)
        home_page.open_page()
        
        # 2. 点击Test Exceptions链接
        logger.info("步骤2: 点击Test Exceptions链接")
        home_page.click_test_exceptions()
        
        # 等待页面加载
        time.sleep(3)
        
        # 3. 获取页面信息
        logger.info("步骤3: 分析页面结构")
        current_url = driver.current_url
        page_title = driver.title
        page_source_length = len(driver.page_source)
        
        logger.info(f"当前URL: {current_url}")
        logger.info(f"页面标题: {page_title}")
        logger.info(f"页面源码长度: {page_source_length}")
        
        # 4. 检查各种可能的标题元素
        title_selectors = [
            ("h1", "H1标签"),
            ("h2", "H2标签"),
            ("h3", "H3标签"),
            (".title", "title类"),
            ("#title", "title ID"),
            ("title", "title标签"),
            ("[data-testid='title']", "data-testid title"),
            (".page-title", "page-title类"),
            (".header", "header类"),
            ("header h1", "header中的h1"),
            ("main h1", "main中的h1"),
            ("div h1", "div中的h1")
        ]
        
        logger.info("=== 检查标题元素 ===")
        for selector, description in title_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for i, element in enumerate(elements):
                        text = element.text.strip()
                        is_displayed = element.is_displayed()
                        logger.info(f"✅ {description}[{i}]: '{text}' (可见: {is_displayed})")
                else:
                    logger.info(f"❌ {description}: 未找到")
            except Exception as e:
                logger.error(f"❌ {description}: 检查失败 - {e}")
        
        # 5. 检查异常页面的关键元素
        key_selectors = [
            ("add_btn", "Add按钮 (ID)"),
            ("row1", "Row1 (ID)"),
            ("row2", "Row2 (ID)"),
            ("instructions", "Instructions (ID)"),
            ("confirmation", "Confirmation (ID)")
        ]
        
        logger.info("=== 检查关键元素 ===")
        for element_id, description in key_selectors:
            try:
                element = driver.find_element(By.ID, element_id)
                text = element.text.strip()
                is_displayed = element.is_displayed()
                tag_name = element.tag_name
                logger.info(f"✅ {description}: '{text}' (标签: {tag_name}, 可见: {is_displayed})")
            except Exception as e:
                logger.info(f"❌ {description}: 未找到 - {e}")
        
        # 6. 检查所有可见的文本元素
        logger.info("=== 检查所有可见文本元素 ===")
        try:
            all_elements = driver.find_elements(By.XPATH, "//*[text()]")
            visible_texts = []
            for element in all_elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text and len(text) > 2:  # 过滤掉很短的文本
                        tag_name = element.tag_name
                        visible_texts.append(f"{tag_name}: '{text}'")
            
            logger.info(f"找到 {len(visible_texts)} 个可见文本元素:")
            for text in visible_texts[:20]:  # 只显示前20个
                logger.info(f"  {text}")
                
        except Exception as e:
            logger.error(f"检查可见文本元素失败: {e}")
        
        # 7. 保存页面源码用于分析
        logger.info("步骤4: 保存页面源码")
        with open("exceptions_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("页面源码已保存到: exceptions_page_source.html")
        
        # 8. 截图
        logger.info("步骤5: 保存诊断截图")
        driver.save_screenshot("exceptions_page_diagnosis.png")
        logger.info("诊断截图已保存到: exceptions_page_diagnosis.png")
        
    except Exception as e:
        logger.error(f"诊断过程中出错: {e}")
        
    finally:
        # 关闭浏览器
        driver_manager.quit_driver()
        logger.info("=== 诊断完成 ===")


if __name__ == "__main__":
    # 配置日志
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:HH:mm:ss} | {level} | {message}",
        level="INFO",
        colorize=True
    )
    
    diagnose_exceptions_page()
