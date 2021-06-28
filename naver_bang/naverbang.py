from selenium import webdriver
from bs4 import BeautifulSoup



class Naverbang(object):

    url = 'https://m.land.naver.com/article/info/2115765163?newMobile'
    driver_path = 'chromedriver.exe/chromedriver'

    def scrap(self):
        driver = webdriver.Chrome(self.driver_path)
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ls = soup.find_all('div', {'class': 'detail_location_info'})
        newls = [i.find('em').text for i in ls]
        print(newls)
        driver.close()


Naverbang().scrap()
