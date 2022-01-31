from urlsetter import URLSetter_Naver

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
    
    for url in urllist :
        print(url.Category)
        print(url.Url)