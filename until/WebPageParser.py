import time
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
"""
    代码功能：用于实现对每一个文章的html页面的字段解析，获取对应的信息保存到表格中

"""


class WebPageParser:
    def __init__(self, driver, data_dict, url, download_folder):
        self.driver = driver
        self.data_dict = data_dict
        self.url = url
        self.download_folder = download_folder

    def parse_year(self):
        try:
            # 尝试获取当前元素
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div[2]/div[1]'))
            )
            self.data_dict['Year'] = element.text.strip()
            time.sleep(2)
        except Exception as e:
            # 如果当前元素不存在，尝试获取备用元素
            alternative_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/span/a[2]'))
            )
            self.data_dict['Year'] = alternative_element.text.strip()
            time.sleep(2)

    def parse_journal(self):
        try:
            # 尝试获取当前元素
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/span/a[1]'))
            )
            self.data_dict['Journal'] = element.text.strip()
            time.sleep(2)
        except Exception as e:
            # 如果当前元素不存在，尝试获取备用元素
            alternative_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/span/a[1]'))
            )
            self.data_dict['Journal'] = alternative_element.text.strip()
            time.sleep(2)


    def parse_sub_head(self):
        try:
            # 找到包含“分类号”的元素
            classification_element = self.driver.find_element(By.XPATH, '//*[contains(text(), "基金资助")]')

            # 找到“分类号”后面的 <p> 元素
            next_p_element = classification_element.find_element(By.XPATH, 'following-sibling::p')
            self.data_dict['Subject Headings'] = next_p_element.text
            time.sleep(2)
        except Exception as e:
            print("没有基金资助栏目")

    def parse_sub_head_pages(self):
        try:
            # 找到包含“分类号”的元素
            classification_element = self.driver.find_element(By.XPATH, '//*[contains(text(), "页码")]')
            # 提取并打印 <p> 元素的文本内容
            self.data_dict['Pages'] = classification_element.text.split('：')[1]
            # print(classification_element.text.split('：')[1])
            time.sleep(2)

        except Exception as e:
            print("没有页码项目")

#Subject Headings
    def parse_title(self):
        try:
            # 尝试获取当前元素
            element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div[3]/div[1]/div/h1'))
            )
            self.data_dict['Title'] = element.text
            time.sleep(2)
            return element.text

        except Exception as e:
            # 如果当前元素不存在，尝试获取备用元素
            alternative_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[3]/div[1]/div/h1'))
            )
            self.data_dict['Title'] = alternative_element.text
            time.sleep(2)
            return alternative_element.text

    def parse_author(self):
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="authorpart"]'))
        )
        self.data_dict['Author'] = element.text.strip()
        time.sleep(2)
    def parse_author_address(self):
        try:
            # 尝试获取当前元素
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div[3]/div[1]/div/h3[2]'))
            )
            self.data_dict['Author Address'] = element.text.strip()
            time.sleep(2)
        except Exception as e:
            # 如果当前元素不存在，尝试获取备用元素
            alternative_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[3]/div[1]/div/h3[2]/span/a'))
            )
            self.data_dict['Author Address'] = alternative_element.text.strip()
            time.sleep(2)

    def parse_num_classificy(self):
        # 找到包含“分类号”的元素
        classification_element = self.driver.find_element(By.XPATH, '//*[contains(text(), "分类号")]')

        # 找到“分类号”后面的 <p> 元素
        next_p_element = classification_element.find_element(By.XPATH, 'following-sibling::p')
        self.data_dict['Num of Bibliographies'] = next_p_element.text
        time.sleep(2)


    def parse_abstract(self):
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ChDivSummary"]'))
        )
        self.data_dict['Abstract'] = element.text.strip()
        time.sleep(2)

    def parse_keywords(self):
        try:
            # 尝试获取当前元素
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div[3]/div[3]/p'))
            )
            self.data_dict['Keywords'] = element.text.strip()
            time.sleep(2)
        except Exception as e:
            # 如果当前元素不存在，尝试获取备用元素
            alternative_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[3]/div[3]/p'))
            )
            self.data_dict['Keywords'] = alternative_element.text.strip()
            time.sleep(2)

    def parse_and_update(self):
        self.parse_year()
        self.parse_journal()
        self.parse_title()
        self.parse_author()
        self.parse_author_address()
        self.parse_abstract()
        self.parse_keywords()
        self.parse_sub_head_pages()
        self.parse_sub_head()
        self.parse_num_classificy()
        # 假设 URL 是通过构造函数传递的
        self.data_dict['URL'] = self.url

    def download_pdf(self, download_folder):
        # 确保下载文件夹存在
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        try:
            # 等待PDF按钮可点击并进行点击
            pdf_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pdfDown"]'))
            )
            pdf_button.click()
            print("PDF下载已启动，正在等待文件保存...")
            # 等待通知元素出现
            notification = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, '//*[@id="ChDivSummary"]'))  # 替换为您的通知类名
            )

            # 创建动作链对象
            actions = ActionChains(self.driver)
            # 模拟鼠标移动到通知元素上并点击
            actions.move_to_element(notification).click().perform()
            print(f"PDF下载完成，文件保存在：{download_folder}")
        except Exception as e:
            print(f"下载PDF时发生错误: {e}")

    def get_latest_pdf_file(self):
        """
        从下载目录中获取最新的 PDF 文件名
        """
        pdf_files = [file for file in os.listdir(self.download_folder) if file.lower().endswith('.pdf')]
        if not pdf_files:
            print("没有找到 PDF 文件")
            return ''

        # 获取最新修改的 PDF 文件
        latest_file = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(self.download_folder, f)))
        # print(latest_file)
        return latest_file

    #调用接口代码
    def send_data_to_api(self, api_url,html_file_path):
        headers = {
            'Content-Type': 'application/json'
        }
        # 附件路径处理
        # 获取最新 PDF 文件名
        pdf_file_name = self.get_latest_pdf_file()
        if not pdf_file_name:
            print("无法获取 PDF 文件名，终止 API 请求")
            return
        file_path = f'D:\\DATA\\cnkiSpider\\pdf_to_download\\{pdf_file_name}'  # 替换为实际路径
        # 构造请求数据
        payload = {
            'cnTitle': self.data_dict.get('Title', ''),
            'enTitle': self.data_dict.get('English Title', ''),  # 如果你有英文标题数据，可以填入这里
            'author': self.data_dict.get('Author', ''),
            'authorAffiliation':self.data_dict.get('Author Address', ''),
            'cnDigest':self.data_dict.get('Abstract', ''),
            'keyWord':self.data_dict.get('Keywords', ''),
            'classNum':self.data_dict.get('Num of Bibliographies', ''),
            'fundingCategory':self.data_dict.get('Subject Headings', ''),
            'enDigest':self.data_dict.get('Caption', ''),
            'source':self.data_dict.get('Journal', ''),
            'year':self.data_dict.get('Year', ''),
            'volume':self.data_dict.get('Number of Volumes', ''),
            'stage':self.data_dict.get('Issue', ''),
            'page':self.data_dict.get('Pages', ''),
            'dataType':self.data_dict.get('Social Science Category', ''),
            'levelone':self.data_dict.get('Tertiary Title', ''),
            'leveltwo':self.data_dict.get('Translated Tertiary Title', ''),
            'fileName':pdf_file_name,
            'filePath':file_path,
            'htmlPath':html_file_path,
            'oaId':self.data_dict.get('Accession Number', ''),
            'remark1':self.data_dict.get('URL', '')

        }

        # 发送 POST 请求
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response_data = response.json()

            if response_data.get('code') == 0:
                print("数据成功提交至API")
            else:
                print(f"API返回错误：{response_data.get('msg')}")
        except requests.RequestException as e:
            print(f"请求发生错误：{e}")
