import abc
from concurrent.futures import ProcessPoolExecutor, as_completed

class iCrawler( metaclass = abc.ABCMeta ) :
    """
        interface for defining crawler.
        initilize common variable and define essential methods.
    """
    @property
    def urlpath( self ) :
        return self._urlpath

    @urlpath.setter
    def urlpath( self, urlpath ) :
        self._urlpath = urlpath

    @abc.abstractmethod
    def getNewsItem(self, url) -> list :
        pass

    def Exec(self) -> list :
        url_lists = self._urlpath
        category_item = list()

        with ProcessPoolExecutor() as e:
            futures = [e.submit(self.getNewsItem, url) for url in url_lists]
            for future in as_completed(futures):
                category_item.extend(future.result())

        return category_item 
