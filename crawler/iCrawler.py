import abc


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
    def getNewsItems( ) -> dict :
        pass 
