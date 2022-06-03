from .URLSetter import URLSetter
from custom_type.urllist import urllist


class URLSetter_Naver(URLSetter):
    def geturllist(self) -> list:
        temp = list()
        temp.append(
            urllist(
                "Politic",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100",
            )
        )
        temp.append(
            urllist(
                "Economic",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101",
            )
        )
        temp.append(
            urllist(
                "Social",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102",
            )
        )
        temp.append(
            urllist(
                "Life&Culture",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103",
            )
        )
        temp.append(
            urllist(
                "It/Science",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105",
            )
        )
        temp.append(
            urllist(
                "World",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104",
            )
        )
        return temp
