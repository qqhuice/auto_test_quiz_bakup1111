"""
基础页面类
所有页面对象的基类，提供通用的页面操作方法
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
from config.config_manager import config


class BasePage:
    """基础页面类"""
    
    def __init__(self, driver: WebDriver):
        """
        初始化基础页面
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get('browser.explicit_wait', 20))
        self.actions = ActionChains(driver)
    
    def open_url(self, url: str):
        """
        打开指定URL
        
        Args:
            url: 目标URL
        """
        logger.info(f"正在打开URL: {url}")
        self.driver.get(url)
        logger.info(f"已打开URL: {url}")
    
    def get_current_url(self) -> str:
        """
        获取当前页面URL
        
        Returns:
            当前页面URL
        """
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.driver.title
    
    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        查找单个元素
        
        Args:
            locator: 元素定位器 (By.ID, "element_id")
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        if timeout is None:
            timeout = config.get('browser.explicit_wait', 20)
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"找到元素: {locator}")
            return element
        except TimeoutException:
            logger.error(f"查找元素超时: {locator}")
            raise
    
    def find_elements(self, locator: tuple, timeout: int = None) -> list:
        """
        查找多个元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            WebElement列表
        """
        if timeout is None:
            timeout = config.get('browser.explicit_wait', 20)
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"查找元素超时: {locator}")
            return []
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        等待元素可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        if timeout is None:
            timeout = config.get('browser.explicit_wait', 20)
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"元素已可见: {locator}")
            return element
        except TimeoutException:
            logger.error(f"等待元素可见超时: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        等待元素可点击
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        if timeout is None:
            timeout = config.get('browser.explicit_wait', 20)
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"元素可点击: {locator}")
            return element
        except TimeoutException:
            logger.error(f"等待元素可点击超时: {locator}")
            raise
    
    def click_element(self, locator: tuple, timeout: int = None):
        """
        点击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        logger.info(f"已点击元素: {locator}")
    
    def input_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
        """
        输入文本
        
        Args:
            locator: 元素定位器
            text: 要输入的文本
            clear_first: 是否先清空
            timeout: 超时时间
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"已输入文本 '{text}' 到元素: {locator}")
    
    def get_element_text(self, locator: tuple, timeout: int = None) -> str:
        """
        获取元素文本
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            元素文本
        """
        element = self.wait_for_element_visible(locator, timeout)
        text = element.text
        logger.debug(f"获取元素文本: {locator} -> '{text}'")
        return text
    
    def get_element_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """
        获取元素属性
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            timeout: 超时时间
            
        Returns:
            属性值
        """
        element = self.wait_for_element_visible(locator, timeout)
        value = element.get_attribute(attribute)
        logger.debug(f"获取元素属性: {locator}.{attribute} -> '{value}'")
        return value
    
    def is_element_present(self, locator: tuple) -> bool:
        """
        检查元素是否存在
        
        Args:
            locator: 元素定位器
            
        Returns:
            是否存在
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        检查元素是否可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否可见
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator: tuple, timeout: int = None):
        """
        滚动到元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"已滚动到元素: {locator}")
    
    def wait_for_page_load(self, timeout: int = 30):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            logger.info("页面加载完成")
        except TimeoutException:
            logger.warning("等待页面加载超时")
    
    def go_back(self):
        """返回上一页"""
        self.driver.back()
        logger.info("已返回上一页")
    
    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
        logger.info("已刷新页面")
