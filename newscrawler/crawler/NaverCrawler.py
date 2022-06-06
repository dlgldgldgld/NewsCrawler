if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from iCrawler import iCrawler
else :
    import os 
    
    from crawler.iCrawler import iCrawler
    
from custom_type.urllist import urllist
from custom_type.outrecord import outrecord

import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager


class NaverCrawler(iCrawler):
    def __init__(self):
        pass

    def getAddContent(self, driver, url=None) -> list:
        driver.get(url)
        comm_cnt = None
        intrest_cnt = None
        created_time = None
        
        # 기사의 Comment Count 찾기
        try :
            comments_tag = WebDriverWait(driver, 3).until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, '#comment_count'))
                    )
        except NoSuchElementException as e:
            pass
        else :
            comm_cnt = '0' if not comments_tag.text.isdigit() else comments_tag.text

        try:
            # 기사의 반응 갯수 찾기 Count 찾기
            like_tags = WebDriverWait(driver, 3).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "#commentFontGroup > div.media_end_head_info_variety_likeit._LIKE_HIDE.as_likeit_improve > div > a > span.u_likeit_text._count"))
                )
        except NoSuchElementException as e :
            pass
        else:
            intrest_cnt = like_tags.text

        try : 
            create_time_tag = WebDriverWait(driver, 3).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, '#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span'))
                )
        except NoSuchElementException as e :
            pass
        else:
            created_time = create_time_tag.text

        return comm_cnt, intrest_cnt, created_time

    def getnewsitem(self, url) -> list:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        html = urlopen(url.url)
        bsObj = BeautifulSoup(html.read(), "html.parser")
        headline = bsObj.findAll("a", {"class": "cluster_text_headline"})
        urllist = []
        for article in headline:
            if "href" in article.attrs:
                item = outrecord(url.category, article.text, article.attrs["href"])
                (
                    item.comm_cnt,
                    item.interest_cnt,
                    item.created_time,
                ) = self.getAddContent(driver, article.attrs["href"])
                urllist.append(item)
        return urllist

if __name__ == "__main__" :
    # initialize Class 
    test = NaverCrawler()
    test.urlpath = [urllist('Politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100')]
    # test 1 : getNewsItems test

    items = test.getnewsitem(test.urlpath[0])
    for i in items :
        print (i.getrecbydict())

    # test 2 : getAddContent test
    # item = outrecord('hi','hi', 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # item.comm_cnt, item.interest_cnt, item.created_time = test.getAddContent(driver, 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    # print(item.getrecbydict())
