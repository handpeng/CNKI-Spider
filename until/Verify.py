# slider_solver.py

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class SliderSolver:
    def __init__(self, driver: webdriver.Edge):
        self.driver = driver

    def solve_slider_captcha(self):
        try:
            # 等待页面加载
            time.sleep(5)  # 根据实际情况调整等待时间

            # 获取背景图和滑块图元素
            background = self.driver.find_element(By.CSS_SELECTOR, '.verify-img-panel')
            slider = self.driver.find_element(By.CSS_SELECTOR, '.verify-sub-block')

            # 提取滑块的 CSS 样式
            slider_style = self.driver.execute_script(
                'return window.getComputedStyle(arguments[0]).getPropertyValue("background-position");', slider
            )
            slider_x = float(slider_style.split(' ')[0].replace('px', ''))
            slider_y = float(slider_style.split(' ')[1].replace('px', ''))

            # 计算滑块拖动的距离
            drag_distance = -slider_x  # 滑块需要向左拖动滑动的距离

            # 执行滑动操作
            action = ActionChains(self.driver)
            action.click_and_hold(slider).move_by_offset(drag_distance, 0).release().perform()

            # 等待验证结果
            time.sleep(5)  # 根据实际情况调整等待时间

        except Exception as e:
            print(f"解决滑块验证码时发生错误：{e}")

    def check_and_solve_captcha(self):
        # 检查是否存在滑块验证码元素
        try:
            if self.driver.find_elements(By.CSS_SELECTOR, '.verify-img-panel'):
                self.solve_slider_captcha()
        except Exception as e:
            print(f"检查滑块验证码时发生错误,不需要进行滑块验证：{e}")

