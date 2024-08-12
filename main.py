from until.CNKISearch import *
from until.ExcelProcessor import *
from until.HtmlPageParser import *
from until.Verify import SliderSolver
from until.WebPageParser import *
from selenium import webdriver
from selenium.webdriver.edge.options import Options

import os
import pickle
import logging

# 配置日志级别
logging.basicConfig(level=logging.INFO)

# 创建Logger
logger = logging.getLogger(__name__)

# 指定日志文件的路径
log_file_path = './your_log_file.log'  # 请将此路径替换为你的日志文件路径

# 创建一个FileHandler来写入日志文件
file_handler = logging.FileHandler(log_file_path)

# 可以设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将FileHandler添加到logger中
logger.addHandler(file_handler)

def append_data_to_excel(data_dict, file_name='data_dict.xls'):
    # 尝试读取已有的Excel文件，如果文件不存在，将创建一个新的DataFrame
    try:
        df = pd.read_excel(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=data_dict.keys())

    # 将新数据转换为DataFrame
    new_data_df = pd.DataFrame([data_dict])

    # 将新数据追加到已有的DataFrame
    df = pd.concat([df, new_data_df], ignore_index=True)

    # 保存更新后的DataFrame回Excel文件
    df.to_excel(file_name, index=False, header=True)

#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# if __name__ == "__main__":
#     try:
#         options = webdriver.EdgeOptions()
#         # 创建 EdgeOptions 对象
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
#         options.add_argument("--referrer-policy=strict-origin-when-cross-origin")
#         driver = webdriver.Edge(options=options)
#
#         start_url = "https://www.cnki.net/"
#         df = pd.read_excel('中医药期刊列表-李敬华-3-23.xlsx')
#
#         # 定义日期范围的起始和结束年份
#         start_year = 2007
#         end_year = 2000
#
#         # 遍历每一行
#         for index, row in df.iterrows():
#             search_query = row['名称']  # 假设列名为 '名称'
#
#             # 生成每年的日期范围
#             for year in range(start_year, end_year - 1, -1):
#                 start_date = datetime(year, 1, 1)
#                 end_date = datetime(year, 12, 31)
#
#                 cnki_search = CNKISearch(driver, start_url, start_date, end_date, search_query)
#                 cnki_search.run_search()
#                 start_url_New = cnki_search.get_article_urls()
#                 save_urls_to_file(start_url_New)
#
#                 file_path = '赵炳南.xls'
#                 processor = ExcelProcessor(file_path)
#                 processor.read_excel_headers()
#                 processor.initialize_data_dict()
#
#                 # 读取文件中的 URL
#                 with open('urls.txt', 'r') as file:
#                     urls = file.readlines()
#
#                 # 遍历 URL 列表
#                 for url in urls:
#                     url = url.strip()  # 去掉每行末尾的换行符
#                     try:
#                         # 处理 URL 的代码
#                         print(f"Processing URL: {url}")
#                         # 设置Edge浏览器的下载目录
#                         download_folder = "D:\\DATA\\cnkiSpider\\pdf_to_download"  # 请将此路径替换为您的下载目录路径
#
#                         # 创建Edge选项对象
#                         options = Options()
#
#                         # 设置下载偏好
#                         options.use_chromium = True
#                         prefs = {
#                             'download.default_directory': download_folder,
#                             'download.prompt_for_download': False,  # 禁用下载前确认
#                             'download.directory_upgrade': True,
#                             'safebrowsing.enabled': True
#                         }
#                         options.add_experimental_option('prefs', prefs)
#
#                         # 创建 EdgeOptions 对象
#                         options.add_argument(
#                             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
#                         options.add_argument("--referrer-policy=strict-origin-when-cross-origin")
#
#                         # 启动Edge浏览器实例
#                         driver = webdriver.Edge(options=options)
#                         time.sleep(5)
#                         driver.get(url)
#                         # 最大化浏览器窗口
#                         driver.maximize_window()
#                         # 检查并解决滑块验证码
#                         solver = SliderSolver(driver)
#                         solver.check_and_solve_captcha()
#
#                         data_dict = processor.get_data_dict()
#                         parser = WebPageParser(driver, data_dict, url, download_folder)
#                         time.sleep(3)
#
#                         parser.parse_and_update()
#                         filename = parser.parse_title()
#                         append_data_to_excel(parser.data_dict)
#                         print("新数据已追加到Excel文件。")
#                         html_file_path = process_row(driver, filename,search_query,start_date)
#                         # html_file_path = process_row()
#                         time.sleep(3)
#                         driver.get(url)
#                         # 最大化浏览器窗口
#                         driver.maximize_window()
#                         # 检查并解决滑块验证码
#                         solver = SliderSolver(driver)
#                         solver.check_and_solve_captcha()
#                         parser.download_pdf("pdf_to_download")
#
#                         try:
#                             # 发送数据到接口
#                             api_url = "https://ai.tcmcds.com/infcn/sys/journal/saveSpiderJournalCNKI"
#                             DOWNLOAD_FOLDER = "'D:\\DATA\\cnkiSpider\\pdf_to_download'"
#                             parser.send_data_to_api(api_url,html_file_path)
#                         except Exception as e:
#                             print(f"处理 URL '{url}' 时发生传送api异常：{e}")
#                         time.sleep(3)
#
#                     except Exception as e:
#                         logger.error(f"处理 URL '{url}' 时发生异常：{e}")
#                 print(f"完成'{search_query}'期刊中的‘{start_date}’年的文章数据爬取任务")
#     except Exception as e:
#         logger.error(f"主程序运行时发生异常：{e}")
#
#     finally:
#         driver.quit()



def load_progress():
    if os.path.exists('progress.pkl'):
        with open('progress.pkl', 'rb') as f:
            return pickle.load(f)
    return {'current_index': 0, 'current_year': start_year}

def save_progress(progress):
    with open('progress.pkl', 'wb') as f:
        pickle.dump(progress, f)

if __name__ == "__main__":
    try:
        options = webdriver.EdgeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
        options.add_argument("--referrer-policy=strict-origin-when-cross-origin")
        driver = webdriver.Edge(options=options)

        start_url = "https://www.cnki.net/"
        df = pd.read_excel('中医药期刊列表-李敬华-3-23.xlsx')

        start_year = 2007
        end_year = 2000

        progress = load_progress()

        for index, row in df.iloc[progress['current_index']:].iterrows():
            search_query = row['名称']
            for year in range(progress['current_year'], end_year - 1, -1):
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31)

                cnki_search = CNKISearch(driver, start_url, start_date, end_date, search_query)
                cnki_search.run_search()
                start_url_New = cnki_search.get_article_urls()
                save_urls_to_file(start_url_New)

                file_path = '赵炳南.xls'
                processor = ExcelProcessor(file_path)
                processor.read_excel_headers()
                processor.initialize_data_dict()

                with open('urls.txt', 'r') as file:
                    urls = file.readlines()

                for url in urls:
                    url = url.strip()
                    try:
                        print(f"Processing URL: {url}")
                        download_folder = "D:\\DATA\\cnkiSpider\\pdf_to_download"

                        options = Options()
                        options.use_chromium = True
                        prefs = {
                            'download.default_directory': download_folder,
                            'download.prompt_for_download': False,
                            'download.directory_upgrade': True,
                            'safebrowsing.enabled': True
                        }
                        options.add_experimental_option('prefs', prefs)
                        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
                        options.add_argument("--referrer-policy=strict-origin-when-cross-origin")

                        driver = webdriver.Edge(options=options)
                        time.sleep(5)
                        driver.get(url)
                        driver.maximize_window()
                        solver = SliderSolver(driver)
                        solver.check_and_solve_captcha()

                        data_dict = processor.get_data_dict()
                        parser = WebPageParser(driver, data_dict, url, download_folder)
                        time.sleep(3)

                        parser.parse_and_update()
                        filename = parser.parse_title()
                        append_data_to_excel(parser.data_dict)
                        print("新数据已追加到Excel文件。")
                        html_file_path = process_row(driver, filename, search_query, start_date)
                        time.sleep(3)
                        driver.get(url)
                        driver.maximize_window()
                        solver = SliderSolver(driver)
                        solver.check_and_solve_captcha()
                        parser.download_pdf("pdf_to_download")

                        try:
                            api_url = "https://ai.tcmcds.com/infcn/sys/journal/saveSpiderJournalCNKI"
                            parser.send_data_to_api(api_url, html_file_path)
                        except Exception as e:
                            print(f"处理 URL '{url}' 时发生传送api异常：{e}")
                        time.sleep(3)

                    except Exception as e:
                        logger.error(f"处理 URL '{url}' 时发生异常：{e}")

                # Save progress after each search query
                progress['current_index'] = index
                progress['current_year'] = year
                save_progress(progress)

            print(f"完成'{search_query}'期刊中的‘{start_date}’年的文章数据爬取任务")

    except Exception as e:
        logger.error(f"主程序运行时发生异常：{e}")

    finally:
        driver.quit()
        save_progress(progress)


