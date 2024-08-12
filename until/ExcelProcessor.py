import pandas as pd

"""'
    代码功能：用于实现对所给的原始数据表头的一个解析功能，主要是为了获取到表头
"""

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = []
        self.data_dict = {}

    def read_excel_headers(self):
        try:
            # 尝试使用 openpyxl 引擎
            df = pd.read_excel(self.file_path, engine='openpyxl')
        except Exception as e:
            try:
                # 如果失败，尝试使用 xlrd 引擎
                df = pd.read_excel(self.file_path, engine='xlrd')
            except Exception as e:
                raise Exception(f"读取Excel文件时发生错误: {e}")

        self.headers = df.columns.tolist()

    def initialize_data_dict(self):
        # 使用表头作为字典的键，值初始化为空字符串
        self.data_dict = {header: '' for header in self.headers}

    def update_data_dict(self, key, value):
        # 更新字典的值
        if key in self.data_dict:
            self.data_dict[key] = value

    def save_data_dict_to_txt(self, output_file='output.txt'):
        # 将字典保存到文本文件，每个键值对占一行
        with open(output_file, 'w', encoding='utf-8') as file:
            for key, value in self.data_dict.items():
                file.write(f"{key}: {value}\n")

    def get_data_dict(self):
        # 返回当前的数据字典
        return self.data_dict