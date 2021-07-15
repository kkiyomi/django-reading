from setup_django import setup_django

setup_django()
from blog.models import ChapterQUepubs, Novel

from django.db import transaction

import os
from datetime import timedelta
from django.utils import timezone
from requests_html import HTML


class ChapterToQU:
    def __init__(self) -> None:

        self.folder = "novel_quepubs/"
        self.quepubs_path = "media/" + self.folder

    def save_title(self, chapter):

        filename = chapter.content_path
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        title = HTML(html=text).find("h1", first=True)

        if chapter.title == "default":
            chapter.title = title.text
            chapter.save()

    def save_chapter(self, novel_title, chapter_number, chapter_path):
        chapter = ChapterQUepubs(
            novel_title=novel_title,
            number=chapter_number,
            folder=self.folder,
            content_path=chapter_path,
        )
        chapter.save()
        self.save_title(chapter)

        if Novel.objects.filter(dir_name=chapter.novel_title).exists():
            chapter.novel = Novel.objects.get(dir_name=chapter.novel_title)
            chapter.save()

    def nolist(self):

        recent_changes = ChapterQUepubs.objects.filter(
            folder=self.folder, date_posted__gt=timezone.now() - timedelta(days=1)
        ).values("novel_title")

        novel_list = set([item["novel_title"] for item in recent_changes])

        novel_list = [
            "Breeding_Dragons_From_Today",
            "Starting_With_Contract_Pets",
        ]

        return novel_list

    @transaction.atomic
    def addto_db(self, novel_list=None):

        if novel_list is None:
            novel_list = self.nolist()

        for index, novel_title in enumerate(novel_list):
            if novel_title is None:
                continue

            novel_path = self.quepubs_path + novel_title

            chapter_numbers = [
                item["number"]
                for item in ChapterQUepubs.objects.filter(
                    folder=self.folder, novel_title=novel_title
                ).values("number")
            ]

            chapter_len = len(os.listdir(novel_path)) - 1
            # if len(chapter_numbers) == chapter_len:
            #     continue

            print(
                len(novel_list) - index,
                chapter_len - len(chapter_numbers),
                novel_title,
            )

            for chapter in os.listdir(novel_path):
                if "chapter" not in chapter:
                    continue

                chapter_path = novel_path + "/" + chapter
                chapter_number = chapter_path.split("_")[-1].replace(".xhtml", "")

                if chapter_number not in chapter_numbers:
                    try:
                        self.save_chapter(novel_title, chapter_number, chapter_path)
                    except Exception as e:
                        print(novel_title, chapter_number)
                        print(e)
                        pass
