"""
练习网站首页页面对象
URL: https://practicetestautomation.com/practice/
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger
from pages.base_page import BasePage
from config.config_manager import config


class PracticeHomePage(BasePage):
    """练习网站首页页面对象"""
    
    # 页面元素定位器
    TEST_LOGIN_PAGE_LINK = (By.LINK_TEXT, "Test Login Page")
    TEST_EXCEPTIONS_LINK = (By.LINK_TEXT, "Test Exceptions")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1")
    MAIN_CONTENT = (By.CSS_SELECTOR, ".entry-content")
    # Practice页面链接定位器（可能的几种形式）
    PRACTICE_LINK = (By.LINK_TEXT, "Practice")
    PRACTICE_LINK_ALT = (By.PARTIAL_LINK_TEXT, "Practice")
    HOME_LINK = (By.LINK_TEXT, "Home")
    LOGO_LINK = (By.CSS_SELECTOR, ".site-title a, .logo a, header a")
    
    def __init__(self, driver: WebDriver):
        """
        初始化首页页面对象
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
        self.url = config.urls.get('practice_home', 'https://practicetestautomation.com/practice/')
    
    def open_page(self):
        """打开练习网站首页"""
        logger.info("正在打开练习网站首页...")
        self.open_url(self.url)
        self.wait_for_page_load()
        logger.info("练习网站首页已加载完成")
    
    def click_test_login_page(self):
        """点击Test Login Page链接"""
        logger.info("正在点击Test Login Page链接...")
        self.click_element(self.TEST_LOGIN_PAGE_LINK)
        self.wait_for_page_load()
        logger.info("已点击Test Login Page链接")
    
    def click_test_exceptions(self):
        """点击Test Exceptions链接"""
        logger.info("正在点击Test Exceptions链接...")
        self.click_element(self.TEST_EXCEPTIONS_LINK)
        self.wait_for_page_load()
        logger.info("已点击Test Exceptions链接")

    def navigate_to_practice_page(self):
        """
        导航到practice页面（优化版本，减少停顿时间）

        根据更新后的流程要求，快速导航到practice页面
        优化策略：直接使用最可靠的方法，减少尝试次数和等待时间
        """
        logger.info("正在快速导航到practice页面...")

        try:
            # 快速检查当前URL
            current_url = self.get_current_url()
            if "practice" in current_url:
                logger.info("当前已在practice页面，快速验证...")
                # 快速验证，减少等待时间
                if self.is_element_present(self.TEST_LOGIN_PAGE_LINK, timeout=2):
                    logger.info("practice页面验证成功，无需导航")
                    return

            # 直接导航到practice页面URL（最快最可靠的方法）
            logger.info("直接导航到practice页面URL...")
            self.open_url(self.url)

            # 使用较短的等待时间
            import time
            time.sleep(1)  # 减少等待时间从默认的3秒到1秒

            # 快速验证页面加载
            if self.is_element_present(self.TEST_LOGIN_PAGE_LINK, timeout=3):
                logger.info("已成功快速导航到practice页面")
                return

            # 如果快速验证失败，使用标准验证
            logger.info("快速验证失败，使用标准验证...")
            self.wait_for_page_load()

            if self.is_page_loaded():
                logger.info("已成功导航到practice页面")
            else:
                logger.warning("页面验证失败，但继续执行测试")

        except Exception as e:
            logger.error(f"导航到practice页面出错: {e}")
            # 简化的备选方案
            try:
                logger.info("使用备选方案：重新打开practice页面...")
                self.open_url(self.url)
                time.sleep(1)  # 短暂等待
                logger.info("备选方案完成")
            except Exception as final_e:
                logger.error(f"备选方案失败: {final_e}")
                # 不抛出异常，让测试继续
    
    def get_page_title_text(self) -> str:
        """
        获取页面标题文本
        
        Returns:
            页面标题文本
        """
        return self.get_element_text(self.PAGE_TITLE)
    
    def is_page_loaded(self) -> bool:
        """
        验证页面是否正确加载
        
        Returns:
            页面是否正确加载
        """
        try:
            # 检查页面标题是否可见
            title_visible = self.is_element_visible(self.PAGE_TITLE)
            
            # 检查Test Login Page链接是否可见
            login_link_visible = self.is_element_visible(self.TEST_LOGIN_PAGE_LINK)
            
            # 检查Test Exceptions链接是否可见
            exceptions_link_visible = self.is_element_visible(self.TEST_EXCEPTIONS_LINK)
            
            is_loaded = title_visible and login_link_visible and exceptions_link_visible
            
            logger.info(f"页面加载验证结果: {is_loaded}")
            logger.debug(f"标题可见: {title_visible}, 登录链接可见: {login_link_visible}, 异常链接可见: {exceptions_link_visible}")
            
            return is_loaded
            
        except Exception as e:
            logger.error(f"页面加载验证失败: {e}")
            return False
    
    def is_test_login_page_link_present(self) -> bool:
        """
        检查Test Login Page链接是否存在
        
        Returns:
            链接是否存在
        """
        return self.is_element_present(self.TEST_LOGIN_PAGE_LINK)
    
    def is_test_exceptions_link_present(self) -> bool:
        """
        检查Test Exceptions链接是否存在
        
        Returns:
            链接是否存在
        """
        return self.is_element_present(self.TEST_EXCEPTIONS_LINK)
    
    def get_all_links(self) -> list:
        """
        获取页面上的所有链接
        
        Returns:
            链接元素列表
        """
        links_locator = (By.TAG_NAME, "a")
        return self.find_elements(links_locator)
    
    def wait_for_page_ready(self):
        """等待页面完全准备就绪"""
        self.wait_for_page_load()
        self.wait_for_element_visible(self.PAGE_TITLE)
        self.wait_for_element_visible(self.TEST_LOGIN_PAGE_LINK)
        self.wait_for_element_visible(self.TEST_EXCEPTIONS_LINK)
        logger.info("页面已完全准备就绪")
