import os

from requests_html import HTMLSession
from setup_django import setup_django

setup_django()
from blog.models import ChapterQUepubs


class EpubDownloader:
    def __init__(self) -> None:

        self.filename = os.getcwd() + f"\\media\\epubs"
        self.directory = os.listdir(self.filename)
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        self.novel_list = []

    def download_epub(self, data):

        url = data["url"]
        filename = data["fileName"]

        session = HTMLSession()
        resp = session.get(url, headers=self.headers)
        if resp.status_code != 200:
            print("download_epub", resp.status_code)
            return

        filename = os.getcwd() + f"\\media\\epubs\\{filename}"
        with open(filename, "wb") as f:
            f.write(resp.content)

    def clean_data(self, data):
        fileName = data["fileName"].replace(".epub", "").replace("_FIN", "")

        chapter_number = fileName.split("_")[-1]
        novel_title = fileName.replace(f"_{chapter_number}", "")

        return novel_title, chapter_number

    def downloaded(self, novel_title, chapter_number):

        if "-" in chapter_number:
            start, end = chapter_number.split("-")
            numbers = [str(item) for item in range(int(start), int(end))]

            if (
                ChapterQUepubs.objects.filter(
                    novel_title=novel_title,
                    number__in=numbers,
                    folder="novel_quepubs/",
                ).count()
                == len(numbers)
            ):
                return True
            else:
                return False

        if ChapterQUepubs.objects.filter(
            novel_title=novel_title,
            number=chapter_number,
            folder="novel_quepubs/",
        ).exists():
            return True
        else:
            return False

    def download(self, data):
        for item in data:
            novel_title, chapter_number = self.clean_data(item)

            if (
                not self.downloaded(novel_title, chapter_number)
                and item["fileName"] not in self.directory
            ):
                print(novel_title, chapter_number)
                self.download_epub(item)
                self.novel_list.append(novel_title)

        return set(self.novel_list)
