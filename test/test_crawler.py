import unittest
from unittest.mock import patch 

class test_Navercrawler(unittest.TestCase):
    def test_getRecByDict(self):
        from newscrawler.crawler.NaverCrawler import NaverCrawler, urllist
        test = NaverCrawler()
        test.urlpath = [ urllist('Politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100') ]
        items = test.Exec()
        self.assertTrue(len(items) > 0)
        