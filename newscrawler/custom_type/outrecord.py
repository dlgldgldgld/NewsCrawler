from datetime import datetime
import re


class outrecord:
    def __init__(self, category=None, title=None, link=None):
        self._category = category
        self._title = title
        self._link = link
        self._comm_cnt = 0
        self._interest_cnt = 0
        self._created_time = None
        pass

    @property
    def comm_cnt(self) -> int:
        return self._comm_cnt

    @comm_cnt.setter
    def comm_cnt(self, comm_cnt: str) -> None:
        if comm_cnt == None or comm_cnt == "댓글":
            self._comm_cnt = 0
            return

        cnt = comm_cnt.replace(",", "")
        self._comm_cnt = int(cnt)

    @property
    def interest_cnt(self) -> int:
        return int(self._interest_cnt)

    @interest_cnt.setter
    def interest_cnt(self, interest_cnt: str) -> None:
        if interest_cnt == None:
            self._interest_cnt = 0
            return

        cnt = interest_cnt.replace(",", "")
        self._interest_cnt = cnt

    @property
    def created_time(self):
        return self._created_time

    @created_time.setter
    def created_time(self, created_time):
        # ex)
        # 1) 2022.02.03. 오전 11:52,
        # 2) 2022.02.03. 오후 1:54
        created_time = re.sub("오전", "AM", created_time)
        created_time = re.sub("오후", "PM", created_time)

        self._created_time = datetime.strptime(created_time, "%Y.%m.%d. %p %I:%M")

    def getrecbydict(self):
        item = dict()
        item["category"] = self._category
        item["title"] = self._title
        item["created_time"] = self._created_time.strftime("%Y.%m.%d %I:%M %p")
        item["interest_cnt"] = self._interest_cnt
        item["comm_cnt"] = self._comm_cnt
        item["link"] = self._link
        return item


if __name__ == "__main__":
    a = outrecord(None, None, None)
    a.created_time = "2022.02.03. 오전 11:52"
    print(a.created_time.strftime("%Y.%m.%d %I:%M %p"))
    a.created_time = "2022.02.03. 오후 1:54"
    print(a.created_time.strftime("%Y.%m.%d %I:%M %p"))
