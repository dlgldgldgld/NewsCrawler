from urlsetter import URLSetter_Naver
from crawler.NaverCrawler import NaverCrawler
import time
import csv

class getArray( ) :
    """
        to get url lists by template method pattern.
    """
    def __init__(self, imp):
        self._imp = imp

    def getArray( self ) :
        return self._imp.GetUrlList()

if __name__ == "__main__" :

    mainContent = getArray( URLSetter_Naver( ) )
    urllist = mainContent.getArray( )

    crawler_Test = NaverCrawler(urllist)
    newsitems = crawler_Test.getNewsItems()

    # csv file reader
    filename = time.strftime('%Y%m%d_%H%M%S') + str('.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile :
        if len(newsitems) == 0 : 
            pass 
        
        fieldnames = newsitems[0].getRecByDict().keys()
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        
        writer.writeheader()
        for row in newsitems :
            writer.writerow(row.getRecByDict())
    