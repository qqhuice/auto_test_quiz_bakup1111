import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementNotInteractableException,
    InvalidElementStateException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains

class TestAllExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://practicetestautomation.com/practice-test-exceptions/")
        time.sleep(1)
        print("浏览器已启动，页面已加载")

    def test_case1_no_such_element_exception(self):
        """测试用例1: NoSuchElementException"""
        print("\n=== 开始执行Case1: NoSuchElementException ===")
        
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)  # 确保滚动完成
        
        # 2. 定位Add按钮并进行红色高亮
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        self._highlight_element(add_button, "red")
        
        # 3. 点击Add按钮
        add_button.click()
        
        # 4. 尝试查找Row 2输入框(预期失败)
        try:
            row2_input = self.driver.find_element(By.XPATH, "//div[text()='Row 2']/following-sibling::input")
        except NoSuchElementException as e:
            print("Case1成功捕获异常:", str(e))
            
            # 显示异常信息面板
            self._show_exception_panel(f"Case1 - NoSuchElementException:\n{str(e)}")
            
            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            print("Case1异常已显示在浏览器中，等待3秒...")
            time.sleep(3)
            # 不重新抛出异常，让测试显示为OK
        
        print("=== Case1测试完成 ===\n")

    def test_case2_element_not_interactable_exception(self):
        """测试用例2: ElementNotInteractableException - 不可见的Save按钮"""
        print("=== 开始执行Case2: ElementNotInteractableException (不可见按钮) ===")
        
        # 刷新页面重置状态
        self.driver.refresh()
        time.sleep(2)
        
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)
        
        # 2. 定位Add按钮并进行红色高亮
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        self._highlight_element(add_button, "red")
        
        # 3. 点击Add按钮
        add_button.click()
        time.sleep(5)  # 等待Row 2出现
        
        # 4. 在Row 2输入框中输入文本
        try:
            # 使用更准确的定位器
            row2_input = self.driver.find_element(By.CSS_SELECTOR, "#row2 input")
        except:
            # 备用定位器
            row2_input = self.driver.find_element(By.XPATH, "//input[2]")
        
        row2_input.send_keys("Test Text")
        
        # 5. 尝试点击不可见的Save按钮(预期失败)
        try:
            # 第一个Save按钮是不可见的
            save_button = self.driver.find_element(By.XPATH, "//button[text()='Save']")
            self._highlight_element(save_button, "red")
            save_button.click()
        except ElementNotInteractableException as e:
            print("Case2成功捕获异常:", str(e))
            
            # 显示异常信息面板
            self._show_exception_panel(f"Case2 - ElementNotInteractableException:\n{str(e)}")
            
            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            print("Case2异常已显示在浏览器中，等待3秒...")
            time.sleep(3)
            # 不重新抛出异常，让测试显示为OK
        
        print("=== Case2测试完成 ===\n")

    def test_case3_element_not_interactable_disabled_exception(self):
        """测试用例3: ElementNotInteractableException - 禁用元素"""
        print("=== 开始执行Case3: ElementNotInteractableException (禁用元素) ===")
        
        # 刷新页面重置状态
        self.driver.refresh()
        time.sleep(2)
        
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)
        
        # 2. 定位Add按钮并进行红色高亮
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        self._highlight_element(add_button, "red")
        
        # 3. 点击Add按钮
        add_button.click()
        time.sleep(5)  # 等待Row 2出现
        
        # 4. 尝试在禁用的输入框中输入文本(预期失败)
        try:
            # 查找禁用的输入框 - 使用多种定位策略
            try:
                disabled_input = self.driver.find_element(By.XPATH, "//input[@disabled]")
            except:
                # 备用策略：查找Row 2输入框然后尝试操作
                disabled_input = self.driver.find_element(By.CSS_SELECTOR, "#row2 input")
            
            self._highlight_element(disabled_input, "red")
            disabled_input.send_keys("Test Text")
        except ElementNotInteractableException as e:
            print("Case3成功捕获异常:", str(e))
            
            # 显示异常信息面板
            self._show_exception_panel(f"Case3 - ElementNotInteractableException:\n{str(e)}")
            
            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            print("Case3异常已显示在浏览器中，等待3秒...")
            time.sleep(3)
            # 不重新抛出异常，让测试显示为OK
        
        print("=== Case3测试完成 ===\n")

    def test_case4_invalid_element_state_exception(self):
        """测试用例4: InvalidElementStateException - 清除禁用字段"""
        print("=== 开始执行Case4: InvalidElementStateException ===")
        
        # 刷新页面重置状态
        self.driver.refresh()
        time.sleep(2)
        
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)
        
        # 2. 定位Add按钮并进行红色高亮
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        self._highlight_element(add_button, "red")
        
        # 3. 点击Add按钮
        add_button.click()
        time.sleep(5)  # 等待Row 2出现
        
        # 4. 尝试清除禁用的输入字段(预期失败)
        try:
            # 查找禁用的输入框并尝试清除 - 使用多种定位策略
            try:
                disabled_input = self.driver.find_element(By.XPATH, "//input[@disabled]")
            except:
                # 备用策略：查找Row 2输入框然后尝试操作
                disabled_input = self.driver.find_element(By.CSS_SELECTOR, "#row2 input")
            
            self._highlight_element(disabled_input, "red")
            disabled_input.clear()
        except (InvalidElementStateException, ElementNotInteractableException) as e:
            print("Case4成功捕获异常:", str(e))
            
            # 显示异常信息面板
            self._show_exception_panel(f"Case4 - InvalidElementStateException:\n{str(e)}")
            
            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            print("Case4异常已显示在浏览器中，等待3秒...")
            time.sleep(3)
            # 不重新抛出异常，让测试显示为OK
        
        print("=== Case4测试完成 ===\n")

    def test_case5_stale_element_reference_exception(self):
        """测试用例5: StaleElementReferenceException - 元素引用过期"""
        print("=== 开始执行Case5: StaleElementReferenceException ===")
        
        # 刷新页面重置状态
        self.driver.refresh()
        time.sleep(2)
        
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)
        
        # 2. 获取instructions元素的引用
        instructions = self.driver.find_element(By.ID, "instructions")
        self._highlight_element(instructions, "red")
        
        # 3. 定位Add按钮并点击
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        add_button.click()
        time.sleep(5)  # 等待Row 2出现，此时instructions元素被移除
        
        # 4. 尝试与已过期的instructions元素交互(预期失败)
        try:
            # 尝试获取已被移除的元素的文本
            text = instructions.text
        except StaleElementReferenceException as e:
            print("Case5成功捕获异常:", str(e))
            
            # 显示异常信息面板
            self._show_exception_panel(f"Case5 - StaleElementReferenceException:\n{str(e)}")
            
            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            print("Case5异常已显示在浏览器中，等待3秒...")
            time.sleep(3)
            # 不重新抛出异常，让测试显示为OK
        
        print("=== Case5测试完成 ===\n")

    def _highlight_element(self, element, color, duration=2):
        """简单高亮元素"""
        original_style = element.get_attribute("style")
        
        # 红色高亮
        self.driver.execute_script(f"arguments[0].style.border='3px solid {color}';", element)
        time.sleep(duration)
        
        # 恢复原始样式
        self.driver.execute_script(f"arguments[0].style='{original_style}';", element)

    def _show_exception_panel(self, message):
        """显示异常信息面板"""
        js = f"""
        // 移除已存在的面板
        const existingPanel = document.getElementById('exception-panel');
        if (existingPanel) {{
            existingPanel.remove();
        }}
        
        const panel = document.createElement('div');
        panel.id = 'exception-panel';
        panel.style = `
            position:fixed; top:20px; right:20px;
            width:350px; padding:15px;
            background:#FFF3E0; border:2px solid #FFA000;
            z-index:9999; font-family:Arial;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        panel.innerHTML = `
            <h3 style="color:#E65100; margin-top:0; margin-bottom:10px;">
                异常捕获成功
            </h3>
            <div style="white-space:pre-wrap; font-size:12px; line-height:1.4;">
                {message.replace('`', '\\`').replace("'", "\\'")}
            </div>
        `;
        document.body.appendChild(panel);
        """
        self.driver.execute_script(js)

    @classmethod
    def tearDownClass(cls):
        print("=== 所有测试用例执行完成 ===")
        print("测试完成，5秒后关闭浏览器...")
        time.sleep(5)  # 给用户时间观察最终结果
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
