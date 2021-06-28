import urllib.request
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import tqdm # 진행률 프로세스바
import time
import random
# url정리 필요한 지역이 있으면 아래에 추가하면 됨

area = {
    '마포구 ': 'https://m.land.naver.com/cluster/ajax/articleList?rletTpCd=OR&tradTpCd=B2&z=12&lat=37.563517&lon=126.9084&btm=37.4740639&lft=126.7336487&top=37.6528628&rgt=127.0831513&showR0=&totCnt=595&cortarNo=1144000000'}
area_name = area.keys()
area_url = area.values()
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
# 네이버부동산 크롤링 함수


def land_info(area_name, area_url):
    info_df = pd.DataFrame()
    # url페이지를 range함수로 1~300까지 만들어서 for문 실행
    for i in tqdm.tqdm(range(1, 100)):
        try:
            # 강제로 실행을 멈춤 랜덤함수 사용 3초~7초 무작위 휴식
            time.sleep(random.randrange(3, 7))
            try:
                # 페이지 url생성
                url = area_url + '&page={}'.format(i)
                # 해더 정보 입력(봇이 아님을 인증)
                body = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36',
                }
                r = requests.get(url, headers=body)
                data = json.loads(r.text)
                # 페이지에 정보가 없을 경우 for문 break(매물정보는 1페이당 20개씩 있음)
                if data['more'] == False:
                    break
                else:
                    result = data['body']
                    df = pd.DataFrame(result)
                    info_df = info_df.append(df)
            # 요청할때 response가 없을 경우 60초 휴식후 재실행
            except requests.exceptions.Timeout:
                time.sleep(60)
                url = area_url + '&page={}'.format(i)
                print(url)
                body = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36',
                }
                r = requests.get(url, headers=body)
                data = json.loads(r.text)
                result = data['body']
                df = pd.DataFrame(result)
                info_df = info_df.append(df)


        # 키에러발생(정보가 없거나 오류발생)시 for문 종료
        except KeyError:
            print("KeyError : page {}".format(i))
            break
        # 제이슨파일로 업로드중 에러 발생시 10초 휴식후 재실행
        except JSONDecodeError:
            print("JSONDecodeError : page {}_sleep 10 sconds_restart".format(i))
            time.sleep(10)
            url = area_url + '&page={}'.format(i)
            body = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36',
            }
            r = requests.get(url, headers=body)
            data = json.loads(r.text)
            result = data['body']
            df = pd.DataFrame(result)
            info_df = info_df.append(df)
            # 데이터프레임 정리

    if info_df.empty:
        info_df = '매물정보 없음'
    else:
        # 컬럼정리
        info_df['지역명'] = area_name
        info_df = info_df[['cortarNo', 'atclNo', 'lat', 'lng']]
        info_df = info_df.rename(
            columns={'cortarNo': '지역코드', 'atclNo': '매물코드',"lat": '위도', "lng" : '경도'})
    return info_df

ls = []
total_df = pd.DataFrame()
for name, url in zip(area_name, area_url):
    try:
        time.sleep(random.randrange(1, 2))
        try:
            df = land_info(name, url)
            total_df = total_df.append(df)
        except requests.exceptions.Timeout:
            time.sleep(60)
            df = land_info(name, url)
            total_df = total_df.append(df)
    except KeyError:
        print("KeyError : {}".format(name))
        pass
total_df = total_df.drop_duplicates(['매물코드'])
total_df = total_df.set_index('매물코드')
# print((total_df))
# print(total_df)
total_df.to_csv('./data/oneroom.csv', sep=',', na_rep='NaN')