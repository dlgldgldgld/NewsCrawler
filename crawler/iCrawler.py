import abc

class iCrawler( metaclass = abc.ABCMeta ) :
    
    @abc.abstractmethod
    def getNewsItems( ) -> list :
        pass 

    @abc.abstractmethod
    def __init__( urlpaths = None ):
        pass