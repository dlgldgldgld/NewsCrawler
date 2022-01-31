import abc


class iCrawler( metaclass = abc.ABCMeta ) :
    """
        interface for defining crawler.
        initilize common variable and define essential methods.
    """
    def __init__( self, urlpath = None ):
        self._urlpath = urlpath

    @property
    def urlpath( self ) :
        return self._urlpath

    @abc.abstractmethod
    def getNewsItems( ) -> dict :
        pass 
