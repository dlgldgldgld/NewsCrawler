from urlsetter import URLSetter_Naver
from urlsetter.URLSetter import URLSetter
from crawler.iCrawler import iCrawler
from crawler.NaverCrawler import NaverCrawler
import time
import csv
import sys

class newscrawler( ) :
    """
        to get url lists by template method pattern.
    """
    def __init__(self, urlsetter : URLSetter, crawler : iCrawler ) :
        self._urlsetter = urlsetter
        self._crawler = crawler

    def init( self ) :
        urllist = self._urlsetter.GetUrlList()
        self._crawler.urlpath = urllist

    def getNewsFeed(self):
        return self._crawler.getNewsItems()

if __name__ == "__main__" :

    crawler_instance = newscrawler( URLSetter_Naver( ), NaverCrawler( ) )
    crawler_instance.init( )
    newsitems = crawler_instance.getNewsFeed()

    if len(newsitems) == 0 :
        exit(0)

    # csv file reader
    outfile_path = ''
    if len(sys.argv) > 1 :
        outfile_path = sys.argv[1] + '/'

    filename = outfile_path + time.strftime('%Y%m%d_%H%M%S') + str('.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile : 
        fieldnames = newsitems[0].getRecByDict().keys()
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )
        
        writer.writeheader()
        for row in newsitems :
            writer.writerow(row.getRecByDict())
    