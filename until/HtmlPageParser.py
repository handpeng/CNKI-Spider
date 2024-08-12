from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import requests
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

"""
    代码功能：用于实现对html的文件按照所需要的处理格式进行整理的需要
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def save_page_source_as_html(driver, file_path):
    """保存页面HTML源代码到本地文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    logger.info(f"页面HTML源代码已保存到：{file_path}")
#
# def save_resources(driver, folder_path):
#     """保存页面中的资源文件（js, css, 图片）到指定文件夹"""
#     resources_folder = os.path.join(folder_path, "全文阅读--XML全文阅读--中国知网_files")
#     os.makedirs(resources_folder, exist_ok=True)
#
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     script_tags = soup.find_all('script', src=True)
#     for script in script_tags:
#         js_url = script['src']
#         save_resource(js_url, resources_folder)
#
#     link_tags = soup.find_all('link', rel='stylesheet', href=True)
#     for link in link_tags:
#         css_url = link['href']
#         save_resource(css_url, resources_folder)
#
#     img_tags = soup.find_all('img', src=True)
#     for img in img_tags:
#         img_url = img['src']
#         save_resource(img_url)


def save_resources(driver, folder_path):
    """保存页面中的资源文件（js, css, 图片）到指定文件夹"""
    resources_folder = os.path.join(folder_path, "全文阅读--XML全文阅读--中国知网_files")
    os.makedirs(resources_folder, exist_ok=True)

    # 获取基础 URL
    global base_url
    base_url = driver.current_url

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 处理 JavaScript 文件
    script_tags = soup.find_all('script', src=True)
    for script in script_tags:
        js_url = script['src']
        save_resource(js_url, resources_folder)

    # 处理 CSS 文件
    link_tags = soup.find_all('link', rel='stylesheet', href=True)
    for link in link_tags:
        css_url = link['href']
        save_resource(css_url, resources_folder)

    # 处理图片文件
    img_tags = soup.find_all('img', src=True)
    for img in img_tags:
        img_url = img['src']
        save_resource(img_url, resources_folder)

def save_resource(resource_url, folder_path=None):
    """保存资源文件到指定文件夹"""
    # 如果 URL 没有 scheme，则将其转换为绝对 URL
    if not resource_url.startswith(('http://', 'https://')):
        resource_url = urljoin(base_url, resource_url)

    try:
        response = requests.get(resource_url)
        response.raise_for_status()  # 如果请求失败，将引发 HTTPError

        # 获取文件名
        resource_name = os.path.basename(resource_url)
        if folder_path:
            file_path = os.path.join(folder_path, resource_name)
        else:
            file_path = resource_name

        # 保存文件
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"Saved resource to {file_path}")

    except Exception as e:
        print(f"Error saving resource {resource_url}: {e}")



# def save_resource(url, folder_path):
#     """保存单个资源文件到指定文件夹"""
#     try:
#         if url.startswith('//'):
#             url = 'https:' + url
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             file_name = url.split('/')[-1]
#             file_path = os.path.join(folder_path, file_name)
#             with open(file_path, 'wb') as file:
#                 file.write(response.content)
#             logger.info(f"保存资源文件成功：{file_name}")
#         else:
#             logger.warning(f"下载资源文件失败：{url}")
#     except Exception as e:
#         logger.error(f"保存资源文件时出错：{str(e)}")

# def slide_to_unlock(driver):
#     """模拟滑块滑动的动作"""
#     try:
#         slider = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "js-handler"))
#         )
#         slider_location = slider.location
#         slider_size = slider.size
#
#         action = ActionChains(driver)
#         action.click_and_hold(slider).perform()
#         time.sleep(1)
#
#         offset_x = slider_size['width'] * 0.9  # 90%的滑块宽度
#         action.move_by_offset(offset_x, 0).perform()
#         action.release().perform()
#
#         time.sleep(3)
#
#     except Exception as e:
#         logger.error(f"滑动操作失败：{str(e)}")

def slide_to_unlock(driver):
    """模拟滑块滑动的动作"""
    try:
        slider = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-handler"]'))
        )
        time.sleep(1)
        # 创建 ActionChains 对象
        action = ActionChains(driver)

        # 按住滑块
        action.click_and_hold(slider).perform()
        time.sleep(3)

        # 设定滑动的目标偏移量
        offset_x = 420  # 你想滑动的距离，单位为像素

        # 滑动到目标位置
        action.move_by_offset(offset_x, 0).perform()
        action.release().perform()

        time.sleep(1)

    except Exception as e:
        logger.error(f"处理滑块时发生异常")


def switch_to_target_window(driver):
    try:
        # 确保有多个窗口
        if len(driver.window_handles) > 1:
            # 切换到最新的窗口
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            logger.info("已切换到新的窗口")
        else:
            logger.error("没有找到足够的窗口进行切换")
    except Exception as e:
        logger.error(f"窗口切换失败：{str(e)}")

def time_down_slider(driver):
    # 方法 2: 逐步滚动
    scroll_pause_time = 2  # 每次下滑的时间间隔

    # 获取页面的总高度
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 向下滚动页面
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 等待页面加载新的内容
        time.sleep(scroll_pause_time)

        # 获取新的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果页面高度没有变化，则退出循环
        if new_height == last_height:
            break
        last_height = new_height

def process_row(driver, file_name, search_query,start_date):
    start_date = start_date.strftime("%Y-%m-%d")
    article_folder = os.path.join(os.getcwd(), f"D:\\DATA\\cnkiSpider\\html\\{search_query}-{start_date}\\{file_name}")
    html_file_path = os.path.join(article_folder, f"全文阅读--XML全文阅读--中国知网.html")

    try:
        # 等待下载链接元素出现并检查文本
        link_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="DownLoadParts"]/div/ul/li[2]/a'))
        )
        link_text = link_element.text
        logger.info(f"下载链接文本：{link_text}")

        if link_text == "在线阅读":
            link_element.click()
            time.sleep(3)
            switch_to_target_window(driver)
            time_down_slider(driver)
            time.sleep(5)

        elif link_text == "HTML阅读":
            link_element.click()
            switch_to_target_window(driver)
            slide_to_unlock(driver)
            time_down_slider(driver)
            time.sleep(3)

        # 确保文章文件夹存在
        os.makedirs(article_folder, exist_ok=True)

        # 保存HTML源代码到本地文件
        save_page_source_as_html(driver, html_file_path)
        time.sleep(3)

        # 保存页面中的资源文件（js, css, 图片）
        save_resources(driver, article_folder)
        time.sleep(5)

    except TimeoutException as e:
        logger.error(f"页面加载超时：{str(e)}")
    except NoSuchWindowException as e:
        logger.error(f"窗口操作异常：{str(e)}")
    except Exception as e:
        logger.error(f"处理行时发生异常：{str(e)}")
    finally:
        logger.info(f"处理文章 '{file_name}' 完成")
        return html_file_path
