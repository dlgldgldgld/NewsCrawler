if __name__ == "__main__" :
    from iCrawler import iCrawler
else :
    from crawler.iCrawler import iCrawler

from bs4 import BeautifulSoup
from urllib.request import urlopen

class NaverCrawler ( iCrawler ) :

    def __init__(self, urlpath=None):
        super().__init__(urlpath)
        
    def getNewsItems( self ) -> list:
        url_lists = self.urlpath
        for url in url_lists :
            html = urlopen( url.Url )
            bsObj = BeautifulSoup(html.read(), "html.parser")
            headline = bsObj.findAll("a", {"class" : "cluster_text_headline"})
            
            for article in headline :
                if 'href' in article.attrs :
                    title = article.text
                    link = article.attrs['href']
                    print( url.Category, title, link )
