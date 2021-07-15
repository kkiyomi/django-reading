from django.utils.text import slugify
from requests_html import HTMLSession

import os
import json

from setup_django import setup_django

setup_django()

from blog.models import Novel, ChapterQUepubs

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}
mobile_headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}


class BookInfo:
    def __init__(self, session=None):

        self.session = session
        if session is None:
            self.session = self.getSession()

        self._csrfToken = self.session.cookies["_csrfToken"]
        self.webnovel_uuid = self.session.cookies["webnovel_uuid"].split("_")[0]

    def getSession(self, url=None, headers=None):

        if url is None:
            url = "https://www.webnovel.com/book/8662546605001405"

        if headers is None:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
            }

        session = HTMLSession()
        resp = session.get(url, headers=headers)

        if resp.status_code != 200:
            print("getSession", resp.status_code)

        return session

    def getBookId(self, novel):
        if novel.wid != "None":
            return

        url = f"https://www.webnovel.com/search?keywords={novel.title}"

        resp = self.session.get(url, headers=headers)
        if resp.status_code != 200:
            print("getBookId", resp.status_code)

        ori = resp.html.find(f'a[href*="/book/{novel.slug}"]', first=True)
        bookId = ori.attrs["data-bookid"]

        novel.wid = bookId
        novel.save()

    def CheckOriginal(self, novel):
        if novel.original != "None":
            return

        bookId = novel.wid

        list_url = f"https://www.webnovel.com/go/pcm/bookReview/get-reviews?_csrfToken={self._csrfToken}&bookId={bookId}&pageIndex=1&pageSize=30&orderBy=1&novelType=0&needSummary=1&_={self.webnovel_uuid}"

        resp = self.session.get(list_url, headers=headers)
        if resp.status_code != 200:
            print("CheckOriginal 2", resp.status_code)

        json_resp = json.loads(str(resp.text))

        bookType = json_resp["data"]["bookStatisticsInfo"]["bookType"]

        novel.original = "True" if bookType == 2 else "False"
        novel.save()

    def CheckTitle(self, novel):

        bookId = novel.wid

        list_url = f"https://www.webnovel.com/go/pcm/bookReview/get-reviews?_csrfToken={self._csrfToken}&bookId={bookId}&pageIndex=1&pageSize=30&orderBy=1&novelType=0&needSummary=1&_={self.webnovel_uuid}"

        resp = self.session.get(list_url, headers=headers)
        if resp.status_code != 200:
            print("CheckTitle", resp.status_code)

        json_resp = json.loads(str(resp.text))

        bookName = json_resp["data"]["bookStatisticsInfo"]["bookName"]

        if novel.title != bookName:
            novel.title = bookName
            novel.save()

    def get_book_detail(self, novel):

        bookId = novel.wid
        url = (
            "https://m.webnovel.com/book/the-wicked-cultivation-game_20178482005547505"
        )
        session = self.getSession(url=url, headers=mobile_headers)

        list_url = f'https://m.webnovel.com/go/pcm/book/get-book-detail?_csrfToken={session.cookies["_csrfToken"]}&bookId={bookId}'

        cookies = {
            "QDReport_referrer": f"https://m.webnovel.com/book/{bookId}",
            "webnovel-content-language": "en",
        }
        for key, value in cookies.items():
            session.cookies.set(key, value)

        resp = session.get(list_url, headers=mobile_headers, cookies=session.cookies)
        if resp.status_code != 200:
            print("get_book_detail", resp.status_code)

        json_resp = json.loads(str(resp.text))

        bookName = json_resp["data"]["bookInfo"]["bookName"]
        print(novel.id, bookName)

        if novel.description == "N/A":
            novel.description = json_resp["data"]["bookInfo"]["description"]
            novel.save()

        # if novel.author == "N/A":
        #     novel.author = json_resp["data"]["bookInfo"]["authorName"]
        #     novel.save()

    def getBookCover(self, novel):
        if novel.image != "default.jpg":
            return

        bookId = novel.wid
        url = f"https://img.webnovel.com/bookcover/{bookId}/300/300.jpg"

        resp = self.session.get(url, headers=headers)
        if resp.status_code != 200:
            print("getBookCover", resp.status_code)

        outputpath = os.getcwd() + f"\\media\\novel_pics\\{slugify(novel.title)}.png"
        with open(outputpath, "wb") as f:
            f.write(resp.content)

        novel.image = f"\\novel_pics\\{slugify(novel.title)}.png"
        novel.save()

    def getInfo(self, novel):
        try:
            self.getBookId(novel)
            self.CheckTitle(novel)
            self.CheckOriginal(novel)
            self.getBookCover(novel)
            self.get_book_detail(novel)
        except Exception as e:
            print(novel.title)
            print(e)
            pass


if __name__ == "__main__":
    novel = Novel.objects.get(wid="16732928106157405")
    bi = BookInfo()
    for novel in (
        Novel.objects.filter(description="N/A").exclude(wid="None").order_by("-id")
    ):
        try:
            bi.get_book_detail(novel)
        except:
            pass
