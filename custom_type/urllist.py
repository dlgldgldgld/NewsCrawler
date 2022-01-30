class urllist :
    """
        This class deal with url path and it's category.
        ex) 'politic' : 'https://www.naver.news/category=politic/page=1'
    """
    def __init__( self , category : str, url : str ) :
        self._category = category
        self._url = url

    @property
    def Category(self):
        return self._category
    
    @property
    def Url(self):
        return self._url

if __name__ == "__main__" :
    print( 'hello urllist' )
    a = urllist('politic', 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100')
    assert 'politic' == a.Category
    assert 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' == a.Url
    print('test pass')