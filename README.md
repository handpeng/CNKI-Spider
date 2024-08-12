# CNKI Article Scraper

## 项目概述

本项目实现了一个用 Python 编写的 CNKI（中国知网）文章抓取工具。通过高级检索功能，本工具可以根据用户指定的搜索条件，抓取满足条件的文章列表及其详细信息，包括标题、作者、摘要等，并将文章的 PDF 文件下载到指定的文件夹。

## 功能

1. **高级检索**：在 CNKI 的高级检索界面中输入搜索条件（关键词、日期范围等），执行检索操作。
2. **文章链接抓取**：抓取符合条件的文章链接，并处理分页以获取所有文章链接。
3. **文章信息解析**：解析每篇文章的 HTML 页面，提取相关信息，如标题、作者、摘要等。
4. **PDF 下载**：下载文章的 PDF 文件，并保存到指定的下载目录。
5. **数据上传**：将抓取到的文章信息及相关文件上传至指定的 API 接口。
6. **反爬机制设置**：实现对爬取html部分时的滑块滑动加载以及对长时间爬取后会出现的系统验证缺口背景图类的反反爬
7. **断点续传和恢复机制**：设定发生断电等意外情况，导致的爬虫将会从头开始对检索信息进行检索的问题进行机制配置

## 环境要求

- Python 3.x
- Selenium
- Requests
- Edge WebDriver（用于驱动 Microsoft Edge 浏览器）

## 安装与使用

### 安装依赖

确保已经安装了必要的 Python 库。可以通过以下命令安装：

```bash
pip install selenium requests
```

### 配置 WebDriver

下载 Microsoft Edge WebDriver，并确保其版本与安装的 Edge 浏览器匹配。将 WebDriver 的路径添加到系统 PATH 中。

### 配置和运行

1. **配置搜索参数**：

   在 `CNKISearch` 类中，设置 `start_url`、`start_date`、`end_date` 和 `search_query` 以定义检索条件。

2. **运行程序**：

   创建一个 `CNKISearch` 实例并调用 `run_search()` 方法来执行搜索，抓取文章链接并下载 PDF 文件。

3. **解析文章**：

   使用 `WebPageParser` 类来解析每篇文章的 HTML 页面，并提取相关信息。

4. **上传数据**：

   调用 `send_data_to_api` 方法，将文章信息及文件上传至指定的 API 接口。

### 示例代码

以下是一个简单的使用示例：

```python
from selenium import webdriver
from datetime import datetime
from your_module import CNKISearch, WebPageParser  # 请将 your_module 替换为实际的模块名

# 创建 WebDriver 实例
driver = webdriver.Edge()

# 定义搜索参数
start_url = 'https://search.cnki.com.cn/'
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
search_query = '人工智能'

# 创建 CNKISearch 实例并执行搜索
searcher = CNKISearch(driver, start_url, start_date, end_date, search_query)
searcher.run_search()

# 获取文章链接
urls = searcher.get_article_urls()

# 解析文章并上传数据
for url in urls:
    driver.get(url)
    parser = WebPageParser(driver, {}, url, 'D:\\DATA\\cnkiSpider\\pdf_to_download')
    parser.parse_and_update()
    parser.download_pdf('D:\\DATA\\cnkiSpider\\pdf_to_download')
    parser.send_data_to_api('http://example.com/api', 'path_to_html_file')
```
### 项目运行

将该代码copy下载后：
1) 请先按要求配置浏览器的驱动版本，将代码中对应的cookie信息替换成您的可以访问CNKI的cookie信息；
2) 直接在对应的python环境下点击运行main.py文件即可
3) API接口部分根据个人需要进行使用

## 注意事项

- **Cookies**：确保提供的 cookies 有效，避免因身份验证失败导致抓取失败。
- **网页结构**：知网网页结构可能会发生变化，需要根据实际情况调整 XPath。
- **API**：根据实际 API 接口的要求调整 `send_data_to_api` 方法中的数据字段。

## 贡献

欢迎对本项目进行贡献。请提交 Pull Request 或者创建 Issue 以报告 bug 或建议改进。

## 许可证

本项目遵循 MIT 许可证。详情请参阅 LICENSE 文件。
