if __name__ == "__main__" :
    from iCrawler import iCrawler
else :
    from crawler.iCrawler import iCrawler

import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

class NaverCrawler ( iCrawler ) :

    def __init__(self, urlpath=None):
        super().__init__(urlpath)
    

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
                    urllist.append(item)
            
            category_item.extend(urllist)

        return category_item     

if __name__ == "__main__" :
    test = NaverCrawler()
    