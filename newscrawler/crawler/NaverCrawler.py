if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from iCrawler import iCrawler
<<<<<<< HEAD
else :
    import os 
    
    from crawler.iCrawler import iCrawler
    
from custom_type.urllist import urllist
from custom_type.outrecord import outrecord
=======

else:
    from newscrawler.crawler.iCrawler import iCrawler

from newscrawler.custom_type.urllist import urllist
from newscrawler.custom_type.outrecord import outrecord
>>>>>>> 369384098a22cffcc39935a715d67a8c1b8c10b6

import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager


class NaverCrawler(iCrawler):
    def __init__(self):
        pass

    def getAddContent(self, driver, url=None) -> list:
        driver.get(url)
        driver.implicitly_wait(0.5)

        comm_cnt = None
        intrest_cnt = None
        created_time = None
<<<<<<< HEAD
        
        # 기사의 Comment Count 찾기
        comments = driver.find_element(By.CSS_SELECTOR, '#comment_count')
=======

        comments = driver.find_element(
            By.CSS_SELECTOR, "#articleTitleCommentCount > span.lo_txt"
        )
>>>>>>> 369384098a22cffcc39935a715d67a8c1b8c10b6
        time.sleep(0.25)
        if comments.text == "":
            comm_cnt = None
        else:
            try:
                comm_cnt = comments.text
            except ValueError as e:
                comm_cnt = None

        try:
            driver.implicitly_wait(0)
<<<<<<< HEAD
            # 기사의 반응 갯수 찾기 Count 찾기
            like_tags = driver.find_element(By.CSS_SELECTOR , '#commentFontGroup > div.media_end_head_info_variety_likeit._LIKE_HIDE.as_likeit_improve > div > a > span.u_likeit_text._count.num' )
        except NoSuchElementException as e :
=======
            like_div = driver.find_element(
                By.CSS_SELECTOR,
                "#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_left > div > a",
            )
            like_tags = like_div.find_element(
                By.CSS_SELECTOR, "span.u_likeit_text._count.num"
            )
        except NoSuchElementException as e:
>>>>>>> 369384098a22cffcc39935a715d67a8c1b8c10b6
            pass
        else:
            intrest_cnt = like_tags.text

<<<<<<< HEAD
        try : 
            create_time_tag = driver.find_element(By.CSS_SELECTOR, '#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span')
        except NoSuchElementException as e :
=======
        try:
            create_time_tag = driver.find_element(
                By.CSS_SELECTOR,
                "#main_content > div.article_header > div.article_info > div > span.t11",
            )
        except NoSuchElementException as e:
>>>>>>> 369384098a22cffcc39935a715d67a8c1b8c10b6
            pass
        else:
            created_time = create_time_tag.text

        return comm_cnt, intrest_cnt, created_time

    def getNewsItem(self, url) -> list:
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

<<<<<<< HEAD
if __name__ == "__main__" :
    # initialize Class 
    test = NaverCrawler()
    test.urlpath = [urllist('Politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100')]
    # test 1 : getNewsItems test
    
    items = test.getNewsItem(test.urlpath[0])
    for i in items :
        print (i.getRecByDict())

    # test 2 : getAddContent test
    item = outrecord('hi','hi', 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    item.comm_cnt, item.interest_cnt, item.created_time = test.getAddContent(driver, 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    print(item.getRecByDict())
=======

if __name__ == "__main__":
    # initialize Class
    test = NaverCrawler(
        urlpath=[
            urllist(
                "Politic",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100",
            )
        ]
    )

    # test 1 : getNewsItems test
    items = test.exec()
    for i in items:
        print(i.getRecByDict())

    # test 2 : getAddContent test
    item = outrecord(
        "hi",
        "hi",
        "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721",
    )
    item.comm_cnt, item.interest_cnt, item.created_time = test.getAddContent(
        "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721"
    )
    print(item.getrecbydict())
>>>>>>> 369384098a22cffcc39935a715d67a8c1b8c10b6
