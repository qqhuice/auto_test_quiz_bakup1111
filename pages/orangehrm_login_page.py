"""
OrangeHRM登录页面对象
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger
from pages.base_page import BasePage


class OrangeHRMLoginPage(BasePage):
    """OrangeHRM登录页面对象"""
    
    # 页面元素定位器
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOGIN_FORM = (By.CLASS_NAME, "orangehrm-login-form")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']")
    
    def __init__(self, driver: WebDriver):
        """
        初始化OrangeHRM登录页面对象
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    
    def open_page(self):
        """打开OrangeHRM登录页面"""
        logger.info("正在打开OrangeHRM登录页面...")
        self.open_url(self.url)
        self.wait_for_page_load()
        logger.info("OrangeHRM登录页面已加载完成")
    
    def enter_username(self, username: str):
        """
        输入用户名
        
        Args:
            username: 用户名
        """
        logger.info(f"正在输入用户名: {username}")
        self.input_text(self.USERNAME_FIELD, username)
        logger.info("用户名输入完成")
    
    def enter_password(self, password: str):
        """
        输入密码
        
        Args:
            password: 密码
        """
        logger.info("正在输入密码...")
        self.input_text(self.PASSWORD_FIELD, password)
        logger.info("密码输入完成")
    
    def click_login_button(self):
        """点击登录按钮"""
        logger.info("正在点击登录按钮...")
        self.click_element(self.LOGIN_BUTTON)
        logger.info("已点击登录按钮")
    
    def login(self, username: str, password: str):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def login_with_default_credentials(self):
        """使用默认凭据登录"""
        # OrangeHRM演示站点的默认凭据
        self.login("Admin", "admin123")
    
    def is_on_login_page(self) -> bool:
        """
        验证是否在登录页面
        
        Returns:
            是否在登录页面
        """
        try:
            return (self.is_element_visible(self.LOGIN_FORM) and 
                   self.is_element_visible(self.USERNAME_FIELD) and 
                   self.is_element_visible(self.PASSWORD_FIELD) and 
                   self.is_element_visible(self.LOGIN_BUTTON))
        except Exception as e:
            logger.error(f"验证登录页面失败: {e}")
            return False
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE):
                message = self.get_element_text(self.ERROR_MESSAGE)
                logger.info(f"获取到错误消息: {message}")
                return message
        except Exception as e:
            logger.warning(f"未找到错误消息: {e}")
        return None
    
    def is_error_displayed(self) -> bool:
        """
        验证是否显示错误消息
        
        Returns:
            是否显示错误消息
        """
        try:
            return self.is_element_visible(self.ERROR_MESSAGE)
        except Exception:
            return False
    
    def is_login_successful(self) -> bool:
        """
        验证登录是否成功（通过URL变化判断）
        
        Returns:
            是否登录成功
        """
        try:
            # 等待页面跳转
            import time
            time.sleep(3)
            current_url = self.get_current_url()
            success = "/dashboard/index" in current_url
            logger.info(f"登录验证结果: {success}, 当前URL: {current_url}")
            return success
        except Exception as e:
            logger.error(f"验证登录状态失败: {e}")
            return False
