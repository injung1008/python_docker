from rest_framework.common.services import Reader, Printer, Scraper
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from glob import glob
import re

driver = webdriver.chrome()

'''
문제정의
셀프 주유소는 정말 저렴할까?
4-1 Selenium 사용하기
4-2 서울시 구별 주유소 가격 정보 얻기
4-5. 구별 주유 가격에 대한 데이터의 정리

4-4 셀프 주유소는 정말 저렴한지 boxplot으로 확인하기

4-5 서울시 구별 주유 가격 확인하기
4-6 서울시 주유 가격 상하위 10개 주유소 지도에 표기하기
'''

class Service():

    def __init__(self):
        self.file = FileDTO()
        self.reader = Reader()
        self.printer = Printer()
        self.scraper = Scraper()

    def get_url(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        scraper = self.scraper
        f.url = 'https://www.opinet.co.kr/searRgSelect.do'
        driver = scraper.driver()
        print(driver.get(file.url))

        gu_list_raw = driver.find_element_by_xpath("""//*[@id="SIGUNGU_NM0"]""")
        gu_list = gu_list_raw.find_element_by_tag_name("option")
        gu_names = [option.geattribute("value") for option in gu_list]
        gu_names.remove('')
        print(gu_names)

    def gas_station_price_info(self):
        # print(glob('./data/지역_위치별*.xls'))
        station_files = glob('./data/지역_위치별*.xls')
        tmp_raw = []
        for i in station_files:
            t = pd.read_excel(i, 2)
            tmp_raw.append(t)
        station_raw = pd.concat(tmp_raw)
        station_raw.info()
        '''
        print("*"*100)
        print(station_raw.head(2))
        print(station_raw.tail(2))
        '''

        stations = pd.DataFrame({'Oil_store':station_raw['상호'],
                                 '주소':station_raw['주소'],
                                 '가격':station_raw['휘발유'],
                                 '셀프':station_raw['셀프여부'],
                                 '상표':station_raw['상표'],
                                 })

        print(stations.head())
        stations['구'] = [ i.split()[1] for i in stations['주소']]
        stations['구'].unique()
        # print(stations[stations['구']=='서울특별시'])
        stations[stations['구'] == '서울특별시'] = '성동구'
        stations['구'].unique()
        # print(stations[stations['가격'] == '-'])

        stations = stations[stations['가격'] != '-']
        p=re.compile('^[0-9]+$')
        temp_stations = []
        for i in stations:
            temp_stations.append(stations[stations['가격'] != p.match()])  # 가격안에 성동구가 들어있어서 제외시켜야한다


        stations['가격'] = [float(i) for i in stations['가격']]
        stations.reset_index(inplace=True)
        del stations['index']
        printer.dframe(stations)


if __name__ == '__main__':
    s = Service()
    # s.get_url()
    s.gas_station_price_info()


