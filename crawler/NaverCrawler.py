if __name__ == "__main__" :
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

    from iCrawler import iCrawler
    from custom_type.urllist import urllist
else :
    from crawler.iCrawler import iCrawler

import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager



class NaverCrawler ( iCrawler ) :

    def __init__(self, urlpath=None):
        super().__init__(urlpath)
        self._driver = webdriver.Chrome(ChromeDriverManager().install())

    def getAddContent(self, url = None ) -> list :
        self._driver.get(url)
        self._driver.implicitly_wait(1.0)

        comm_cnt = 0
        intrest_cnt = 0
        
        comments = self._driver.find_element(By.CSS_SELECTOR, '#articleTitleCommentCount > span.lo_txt')
        time.sleep(0.25)
        if comments.text == '' :
            comm_cnt = 0
        else :
            try :
                comm_cnt = int(comments.text.replace(',' , '') )
            except ValueError as e:
                comm_cnt = 0

        try :
            like_tags = self._driver.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_left > div > a > span.u_likeit_text._count.num')
        except NoSuchElementException as e :
            pass
        else :
            intrest_cnt = int(like_tags.text.replace(',' , ''))

        create_time = self._driver.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > span.t11')

        return comm_cnt, intrest_cnt, create_time.text

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
                    item = dict()
                    item['category'] = url.category
                    item['title'] = article.text
                    item['link'] = article.attrs['href']
                    item['comm_cnt'], item['interest_cnt'], item['created_time'] = self.getAddContent( item['link'] )
                    urllist.append(item)
            
            category_item.extend(urllist)

        return category_item     

if __name__ == "__main__" :
    test = NaverCrawler(urlpath = [urllist('Politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100')])
    items = test.getNewsItems()
    for i in items :
        print (i)

    #print(test.getAddContent('https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=100&oid=448&aid=0000350567'))