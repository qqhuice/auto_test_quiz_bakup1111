import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

class TestExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://practicetestautomation.com/practice-test-exceptions/")
        time.sleep(1)
        print("浏览器已启动，页面已加载")

    def test_stale_element_reference_exception(self):
        # 1. 滚动到标题处
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)  # 确保滚动完成
        
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
            print("成功捕获异常:", str(e))  # 打印错误提示

            # 显示异常信息面板
            self._show_exception_panel(f"成功捕获StaleElementReferenceException:\n{str(e)}")

            # 确保浏览器窗口在前台
            self.driver.switch_to.window(self.driver.current_window_handle)

            print("异常已显示在浏览器中，等待5秒...")
            time.sleep(5)  # 延长显示时间让用户观察
            # 不重新抛出异常，让测试显示为OK

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
        const panel = document.createElement('div');
        panel.style = `
            position:fixed; top:20px; right:20px;
            width:300px; padding:15px;
            background:#FFF3E0; border:2px solid #FFA000;
            z-index:9999; font-family:Arial;
        `;
        panel.innerHTML = `
            <h3 style="color:#E65100; margin-top:0;">
                异常捕获成功
            </h3>
            <div style="white-space:pre-wrap;">
                {message.replace('`', '\\`')}
            </div>
        `;
        document.body.appendChild(panel);
        """
        self.driver.execute_script(js)

    @classmethod
    def tearDownClass(cls):
        print("测试完成，3秒后关闭浏览器...")
        time.sleep(3)  # 给用户时间观察最终结果
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
