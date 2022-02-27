import abc


class URLSetter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def geturllist() -> list:
        pass
