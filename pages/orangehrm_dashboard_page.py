"""
OrangeHRM仪表板页面对象
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger
from pages.base_page import BasePage


class OrangeHRMDashboardPage(BasePage):
    """OrangeHRM仪表板页面对象"""
    
    # 页面元素定位器
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    SIDEBAR_MENU = (By.CLASS_NAME, "oxd-main-menu")
    MENU_ITEMS = (By.XPATH, "//ul[@class='oxd-main-menu']/li")
    CLAIMS_MENU_ITEM = (By.XPATH, "//span[text()='Claim']")
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown")
    
    def __init__(self, driver: WebDriver):
        """
        初始化仪表板页面对象
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    
    def is_on_dashboard_page(self) -> bool:
        """
        验证是否在仪表板页面
        
        Returns:
            是否在仪表板页面
        """
        try:
            return (self.is_element_visible(self.DASHBOARD_HEADER) and 
                   self.is_element_visible(self.SIDEBAR_MENU) and
                   "/dashboard/index" in self.get_current_url())
        except Exception as e:
            logger.error(f"验证仪表板页面失败: {e}")
            return False
    
    def click_sidebar_menu_item(self, menu_text: str):
        """
        点击左侧菜单项
        
        Args:
            menu_text: 菜单文本
        """
        logger.info(f"正在点击左侧菜单项: {menu_text}")
        
        try:
            # 等待侧边栏加载
            self.wait_for_element_visible(self.SIDEBAR_MENU)
            
            # 查找菜单项
            menu_item_locator = (By.XPATH, f"//span[text()='{menu_text}']")
            menu_item = self.wait_for_element_clickable(menu_item_locator)
            
            # 滚动到菜单项并点击
            self.scroll_to_element(menu_item_locator)
            menu_item.click()
            
            logger.info(f"已点击菜单项: {menu_text}")
            self.wait_for_page_load()
            
        except Exception as e:
            logger.error(f"点击菜单项失败: {menu_text} - {e}")
            raise
    
    def click_claims_menu(self):
        """点击Claims菜单"""
        self.click_sidebar_menu_item("Claim")
    
    def get_all_menu_items(self) -> list:
        """
        获取所有可见的菜单项
        
        Returns:
            菜单项元素列表
        """
        return self.find_elements(self.MENU_ITEMS)
    
    def is_menu_item_visible(self, menu_text: str) -> bool:
        """
        验证菜单项是否存在
        
        Args:
            menu_text: 菜单文本
            
        Returns:
            菜单项是否可见
        """
        try:
            menu_item_locator = (By.XPATH, f"//span[text()='{menu_text}']")
            return self.is_element_visible(menu_item_locator)
        except Exception as e:
            logger.warning(f"检查菜单项可见性失败: {menu_text} - {e}")
            return False
    
    def get_current_user(self) -> str:
        """
        获取当前用户信息
        
        Returns:
            当前用户信息
        """
        try:
            if self.is_element_visible(self.USER_DROPDOWN):
                return self.get_element_text(self.USER_DROPDOWN)
        except Exception as e:
            logger.warning(f"获取当前用户信息失败: {e}")
        return None
    
    def wait_for_dashboard_load(self):
        """等待仪表板完全加载"""
        logger.info("等待仪表板页面完全加载...")
        self.wait_for_element_visible(self.DASHBOARD_HEADER)
        self.wait_for_element_visible(self.SIDEBAR_MENU)
        self.wait_for_page_load()
        logger.info("仪表板页面已完全加载")
