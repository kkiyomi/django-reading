from django.db import transaction

import time

from setup_django import setup_django

setup_django()
from blog.models import ChapterQUepubs, ChapterV2


class ChapterV2ToQU:

    # moving chapters from ChapterV2 to ChapterQUepubs

    def __init__(self, timed=None):

        self.timed = timed
        self.timer = time.perf_counter()

        self.chapters_qu = ChapterQUepubs.objects.values("number", "novel")
        self.chapters_v2 = ChapterV2.objects.values("id", "number", "novel")
        self.diff_chapter_ids = []

    def chaptersV2_notinQU(self):
        print("\nChapterV2ToQU: > ", len(self.chapters_v2))
        for item in self.chapters_v2:
            if not self.chapters_qu.filter(
                number=item["number"], novel=item["novel"]
            ).exists():
                self.diff_chapter_ids.append(item["id"])

    def move_V2toQU(self, chapter_id):
        try:
            chapter = ChapterV2.objects.get(id=chapter_id)
            new_chap = ChapterQUepubs(
                title=chapter.title,
                number=chapter.number,
                content_path=chapter.content_path,
                folder=chapter.folder,
                novel=chapter.novel,
            )
            new_chap.save()
            chapter.delete()
        except Exception as e:
            print("move_V2toQU")
            print(e)
            pass

    def into_chunks(self, item_list, maxsize=20):
        return [item_list[i : i + maxsize] for i in range(0, len(item_list), maxsize)]

    def timing_out(self):
        if self.timed is None or time.perf_counter() - self.timer < self.timed * 0.9:
            return False
        else:
            return True

    def remove_dupli(self, item):

        if ChapterQUepubs.objects.filter(
            novel=item["novel"], number=item["number"], folder="novel_quepubs/"
        ).exists():
            ChapterQUepubs.objects.filter(id=item["id"]).delete()

    def atomic_chunks(self, item_list, sqlfunction):

        chunks = self.into_chunks(item_list)

        for sublist in chunks:
            with transaction.atomic():
                for item in sublist:
                    sqlfunction(item)
                    if self.timing_out():
                        return

    def remove_duplicates(self, novel_list=None):
        print("\nRemoving duplicates... ")

        queryset = ChapterQUepubs.objects.exclude(folder="novel_quepubs/")

        if novel_list is not None:
            queryset = queryset.filter(novel__title__in=novel_list)

        chapters = queryset.values("id", "novel", "number")

        self.atomic_chunks(chapters, self.remove_dupli)

    def main(self):

        self.chaptersV2_notinQU()

        chapters_v2_ids = [item["id"] for item in self.chapters_v2]
        chunks = self.into_chunks(chapters_v2_ids)

        for chapter_ids in chunks:
            with transaction.atomic():
                for chapter_id in chapter_ids:
                    if chapter_id in self.diff_chapter_ids:
                        self.move_V2toQU(chapter_id)
                    else:
                        chapter = ChapterV2.objects.get(id=chapter_id)
                        chapter.delete()
                    if self.timing_out():
                        return

        # self.remove_duplicates()
