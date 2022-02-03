import abc

class URLSetter ( metaclass = abc.ABCMeta) :
    @abc.abstractmethod
    def GetUrlList( ) -> list :
        pass
        