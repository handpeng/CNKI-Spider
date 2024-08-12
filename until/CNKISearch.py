"""
    代码功能：用于实现对从知网进入到高级检索目录下并输入检索条件获取到文章列表的任务

"""
import time
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.edge.options import Options

class CNKISearch:
    def __init__(self, driver, start_url, start_date, end_date, search_query):
        self.start_url = start_url
        self.start_date = start_date.strftime("%Y-%m-%d")  # 转换为字符串
        self.end_date = end_date.strftime("%Y-%m-%d")  # 转换为字符串
        self.driver = driver
        self.search_query = search_query
        self.set_logger()

    def set_logger(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def switch_to_new_window_handle(self):
        # 等待新窗口出现
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )
        # 切换到新窗口
        new_window_handle = None
        for handle in self.driver.window_handles:
            if handle != self.driver.current_window_handle:
                new_window_handle = handle
                break
        self.driver.switch_to.window(new_window_handle)
        self.logger.info("Switched to the new window handle.")

    def run_search(self):
        try:
            # 设置Edge浏览器的下载目录
            download_folder = "D:\\DATA\\cnkiSpider\\pdf_to_download"  # 请将此路径替换为您的下载目录路径

            # 创建Edge选项对象
            options = Options()

            # 设置下载偏好
            options.use_chromium = True
            prefs = {
                'download.default_directory': download_folder,
                'download.prompt_for_download': False,  # 禁用下载前确认
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
            options.add_experimental_option('prefs', prefs)

            # 创建 EdgeOptions 对象
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
            options.add_argument("--referrer-policy=strict-origin-when-cross-origin")

            # 启动Edge浏览器实例
            self.driver = webdriver.Edge(options=options)
            self.driver.get(self.start_url)
            # 最大化浏览器窗口
            self.driver.maximize_window()
            self.logger.info(f"打开页面：{self.start_url}")

            # 添加 cookies
            cookies = [
                {'name': 'Ecp_notFirstLogin', 'value': 'MDlW42'},
                {'name': 'SID_kns_new', 'value': 'kns15128001'},
                {'name': 'SID_restapi', 'value': '018133'},
                {'name': 'Hm_lvt_dcec09ba2227fd02c55623c1bb82776a', 'value': '1721097105'},
                {'name': 'HMACCOUNT', 'value': '49E8229C1B357ED8'},
                {'name': 'Ecp_ClientId', 'value': 'm240716103100239877'},
                {'name': 'Ecp_ClientId_Second', 'value': 'l240716103100114791%7Cm240716103100239877'},  # 修改名称
                {'name': 'Ecp_loginuserbk', 'value': 'zykxy'},
                {'name': 'SID_kxreader_new', 'value': '27017041'},
                {'name': 'cnkiUserKey', 'value': 'dbb5b179-5810-cff2-03e5-e952f1161f98'},
                {'name': 'ASP.NET_SessionId', 'value': 'dxi4enmk1jp3tx1sxwpfcbzp'},
                {'name': 'SID_sug', 'value': '018131'},
                {'name': 'Ecp_ClientIp', 'value': '210.73.61.238'},
                {'name': 'language', 'value': 'CHS'},
                {'name': 'Ecp_Userid', 'value': '5066362'},
                {'name': 'SID_nzkhtml', 'value': '019212'}
            ]
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.logger.info("添加 cookies 完成")

            # 进入高级检索界面并输入搜索内容
            self.driver.find_element(By.CSS_SELECTOR, "#highSearch").click()
            # 切换到新页面的句柄
            self.switch_to_new_window_handle()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="gradetxt"]/dd[3]/div[2]/input')))
            element = self.driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[3]/div[2]/input')
            element.clear()
            element.send_keys(self.search_query)

            # 输入起始日期和终止日期
            self.set_date('datebox0', self.start_date)
            time.sleep(2)
            self.set_date('datebox1', self.end_date)
            time.sleep(1)
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ModuleSearch"]/div[1]/div/div[2]/div/div[1]/div[2]/dl/div/div[1]/dt[1]/span')))
            element.click()

            # 点击检索按钮
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/input')))
            element.click()
            # self.driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/input').click()

        except WebDriverException as e:
            self.logger.error(f"WebDriver 错误: {e}")
        except Exception as e:
            self.logger.error(f"搜索过程中发生错误: {e}")

    def set_date(self, datebox_id, date_str):
        date_xpath = f'//*[@id="{datebox_id}"]'
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, date_xpath)))
        self.driver.execute_script(f"document.evaluate('{date_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute('readonly')")
        element.send_keys(date_str)


    # 获取文章的链接内容
    def get_article_urls(self):
            seen_urls = set()  # 用于存储已见过的URL，以便检查重复
            urls = []
            page_count = 1
            index = 0  # 初始化行索引

            while True:
                time.sleep(3)
                # 获取当前页面的所有行
                rows = self.driver.find_elements(By.XPATH, '//*[@id="gridTable"]/div/div/div/table/tbody/tr')
                # 用于存储当前页的URLs
                current_page_urls = []
                for row in rows[index:]:
                    index += 1
                    links = row.find_elements(By.XPATH, f'td[2]//a')
                    # time.sleep(5)
                    for link in links:
                        url = link.get_attribute('href')
                        if url not in seen_urls:  # 检查URL是否已存在
                            seen_urls.add(url)  # 添加到已见URL集合
                            urls.append(url)
                            current_page_urls.append(url)
                            print(url + '/n')
                            if index >= 20:  # 达到20条链接时退出循环
                                break
                    if index >= 20:
                        break

                print(f"当前页面抓取到 {len(current_page_urls)} 条新文章 URL")

                # 在点击下一页按钮前检查当前页的URLs是否有重复
                if len(current_page_urls) == 0:
                    print("当前页面存在重复的URL，不执行点击下一页的操作")
                    break

                if index >= 20:
                    # 点击下一页按钮
                    try:
                        next_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="PageNext"]'))
                        )
                        next_button.click()
                        time.sleep(3)  # 等待页面加载
                        page_count += 1
                        index = 0  # 重置行索引
                        print(f"点击下一页按钮，加载第 {page_count} 页内容")
                    except Exception as e:
                        print(f"无法点击下一页按钮或没有更多页面可加载: {e}")
                        break
            return urls

def save_urls_to_file(urls, file_path='urls.txt'):
        with open(file_path, 'w', encoding='utf-8') as file:
            for url in urls:
                file.write(url + '\n')  # 每个URL后面添加换行符
