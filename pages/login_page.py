"""
登录页面页面对象
URL: https://practicetestautomation.com/practice-test-login/
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger
from pages.base_page import BasePage
from config.config_manager import config


class LoginPage(BasePage):
    """登录页面页面对象"""
    
    # 页面元素定位器
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.ID, "error")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".post-title")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    
    def __init__(self, driver: WebDriver):
        """
        初始化登录页面对象
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
        self.url = config.urls.get('login_page', 'https://practicetestautomation.com/practice-test-login/')
        self.login_data = config.login_data
    
    def open_page(self):
        """打开登录页面"""
        logger.info("正在打开登录页面...")
        self.open_url(self.url)
        self.wait_for_page_load()
        logger.info("登录页面已加载完成")
    
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
    
    def click_submit(self):
        """点击提交按钮"""
        logger.info("正在点击提交按钮...")
        self.click_element(self.SUBMIT_BUTTON)
        logger.info("已点击提交按钮")
    
    def login(self, username: str, password: str):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
    
    def login_with_valid_credentials(self):
        """使用有效凭据登录"""
        username = self.login_data.get('valid_username', 'student')
        password = self.login_data.get('valid_password', 'Password123')
        logger.info(f"使用有效凭据登录: {username}")
        self.login(username, password)
    
    def login_with_invalid_username(self):
        """使用无效用户名登录"""
        username = self.login_data.get('invalid_username', 'incorrectUser')
        password = self.login_data.get('valid_password', 'Password123')
        logger.info(f"使用无效用户名登录: {username}")
        self.login(username, password)
    
    def login_with_invalid_password(self):
        """使用无效密码登录"""
        username = self.login_data.get('valid_username', 'student')
        password = self.login_data.get('invalid_password', 'incorrectPassword')
        logger.info(f"使用无效密码登录: {username}")
        self.login(username, password)
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        try:
            message = self.get_element_text(self.ERROR_MESSAGE)
            logger.info(f"获取到错误消息: {message}")
            return message
        except Exception as e:
            logger.warning(f"未找到错误消息元素: {e}")
            return None
    
    def get_success_message(self) -> str:
        """
        获取成功消息
        
        Returns:
            成功消息文本
        """
        try:
            message = self.get_element_text(self.SUCCESS_MESSAGE)
            logger.info(f"获取到成功消息: {message}")
            return message
        except Exception as e:
            logger.warning(f"未找到成功消息元素: {e}")
            return None
    
    def is_login_successful(self) -> bool:
        """
        验证是否登录成功
        
        Returns:
            是否登录成功
        """
        try:
            logout_visible = self.is_element_visible(self.LOGOUT_LINK, timeout=10)
            logger.info(f"登录成功验证结果: {logout_visible}")
            return logout_visible
        except Exception as e:
            logger.info(f"登录失败，未找到登出链接: {e}")
            return False
    
    def is_error_displayed(self) -> bool:
        """
        验证是否显示错误消息
        
        Returns:
            是否显示错误消息
        """
        try:
            error_visible = self.is_element_visible(self.ERROR_MESSAGE, timeout=10)
            logger.info(f"错误消息显示状态: {error_visible}")
            return error_visible
        except Exception as e:
            logger.info(f"未显示错误消息: {e}")
            return False
    
    def logout(self):
        """点击登出链接"""
        if self.is_login_successful():
            logger.info("正在执行登出操作...")
            self.click_element(self.LOGOUT_LINK)
            self.wait_for_page_load()
            logger.info("登出操作完成")
        else:
            logger.warning("未处于登录状态，无法执行登出操作")
    
    def get_page_title_text(self) -> str:
        """
        获取页面标题文本
        
        Returns:
            页面标题文本
        """
        try:
            return self.get_element_text(self.PAGE_TITLE)
        except Exception:
            return self.get_page_title()
    
    def is_page_loaded(self) -> bool:
        """
        验证页面是否正确加载
        
        Returns:
            页面是否正确加载
        """
        try:
            # 检查用户名输入框是否可见
            username_visible = self.is_element_visible(self.USERNAME_FIELD)
            
            # 检查密码输入框是否可见
            password_visible = self.is_element_visible(self.PASSWORD_FIELD)
            
            # 检查提交按钮是否可见
            submit_visible = self.is_element_visible(self.SUBMIT_BUTTON)
            
            is_loaded = username_visible and password_visible and submit_visible
            
            logger.info(f"登录页面加载验证结果: {is_loaded}")
            logger.debug(f"用户名框可见: {username_visible}, 密码框可见: {password_visible}, 提交按钮可见: {submit_visible}")
            
            return is_loaded
            
        except Exception as e:
            logger.error(f"登录页面加载验证失败: {e}")
            return False
    
    def clear_form(self):
        """清空表单并刷新页面以清除错误消息"""
        logger.info("正在清空登录表单...")
        self.input_text(self.USERNAME_FIELD, "", clear_first=True)
        self.input_text(self.PASSWORD_FIELD, "", clear_first=True)

        # 刷新页面以清除任何错误消息
        logger.info("刷新页面以清除错误消息...")
        self.driver.refresh()

        # 等待页面重新加载
        import time
        time.sleep(2)

        logger.info("登录表单已清空，页面已刷新")
