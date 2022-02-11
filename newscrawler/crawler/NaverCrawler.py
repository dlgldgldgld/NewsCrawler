if __name__ == "__main__" :
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

    from iCrawler import iCrawler
    from custom_type.urllist import urllist
    from custom_type.outrecord import outrecord
else :
    from crawler.iCrawler import iCrawler
    from custom_type.outrecord import outrecord

import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager



class NaverCrawler ( iCrawler ) :

    def __init__( self ):
        self._driver = webdriver.Chrome(ChromeDriverManager().install())

    def getAddContent(self, url = None ) -> list :
        self._driver.get(url)
        self._driver.implicitly_wait(0.5)

        comm_cnt = None
        intrest_cnt = None
        created_time = None

        comments = self._driver.find_element(By.CSS_SELECTOR, '#articleTitleCommentCount > span.lo_txt')
        time.sleep(0.25)
        if comments.text == '' :
            comm_cnt = None
        else :
            try :
                comm_cnt = comments.text
            except ValueError as e:
                comm_cnt = None

        try :
            self._driver.implicitly_wait(0)
            like_div  = self._driver.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_left > div > a')
            like_tags = like_div.find_element(By.CSS_SELECTOR , 'span.u_likeit_text._count.num' )
        except NoSuchElementException as e :
            pass
        else :
            intrest_cnt = like_tags.text
        


        try : 
            create_time_tag = self._driver.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > span.t11')
        except NoSuchElementException as e :
            pass
        else :
            created_time = create_time_tag.text

        return comm_cnt, intrest_cnt, created_time

    def getNewsItems( self ) -> dict:
        url_lists = self.urlpath
        category_item = list()

        for url in url_lists :
            html = urlopen( url.url )
            bsObj = BeautifulSoup(html.read(), "html.parser")
            headline = bsObj.findAll("a", {"class" : "cluster_text_headline"})
            urllist = []
            for article in headline :
                if 'href' in article.attrs :
                    item = outrecord(url.category, article.text, article.attrs['href'])
                    item.comm_cnt, item.interest_cnt, item.created_time = self.getAddContent( article.attrs['href'] )
                    urllist.append(item)
            
            category_item.extend(urllist)

        return category_item     

if __name__ == "__main__" :
    # initialize Class 
    test = NaverCrawler(urlpath = [urllist('Politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100')])

    # test 1 : getNewsItems test
    items = test.getNewsItems()
    for i in items :
        print (i.getRecByDict())

    # test 2 : getAddContent test
    item = outrecord('hi','hi', 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    item.comm_cnt, item.interest_cnt, item.created_time = test.getAddContent('https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=105&oid=421&aid=0005880721')
    print(item.getRecByDict())