import json
import pandas as pd
from rest_framework.common.abstracts import PrinterBase, ReaderBase, ScraperBase
import googlemaps


class Printer(PrinterBase):

    def dframe(self, this):
        print('*' * 100)
        print(f'1. Target type \n {type(this)} ')
        print(f'2. Target column \n {this.columns} ')
        print(f'3. Target 상위 1개 행\n {this.head()} ')
        print(f'4. Target null 의 갯수\n {this.isnull().sum()}개')
        print('*' * 100)


class Reader(ReaderBase):

    def new_file(self, file) -> str:
        return file.context + file.fname

    def csv(self, file) -> object:
        return pd.read_csv(f'{self.new_file(file)}.csv', encoding='UTF-8', thousands=',')

    def xls(self, file, header, usecols) -> object:
        return pd.read_excel(f'{self.new_file(file)}.xls', header=header, usecols=usecols)

    def json(self, file) -> object:
        return json.load(open(f'{self.new_file(file)}.json', encoding='UTF-8'))

    def gmaps(self) -> object:
        return googlemaps.Client(key='AIzaSyBwiDx_sTL-DwIOJCXnf-BqgVjSRcRkb7A')

class Scraper(ScraperBase):

    def driver(self) -> object:
        return webdriver.Chrome('C:\Users\bitcamp\work_space\django-rest-framework\rest_framework\project\common')

    def auto_login(self):

