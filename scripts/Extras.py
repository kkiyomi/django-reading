from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import time
from BookInfo import BookInfo
from setup_django import setup_django

setup_django()
from blog.models import ChapterQUepubs, NovelQu, Novel


class Utils:
    def __init__(self, timed=None):

        self.timed = timed
        self.timer = time.perf_counter()

    def timing_out(self):
        if self.timed is None or time.perf_counter() - self.timer < self.timed * 0.9:
            return False
        else:
            return True

    def into_chunks(self, item_list, maxsize=20):
        return [item_list[i : i + maxsize] for i in range(0, len(item_list), maxsize)]

    def atomic_chunks(self, item_list, sqlfunction):
        chunks = self.into_chunks(item_list)

        for sublist in chunks:
            with transaction.atomic():
                for item in sublist:
                    sqlfunction(item)
                    if self.timing_out():
                        return

    def link_novel_chapter(self, chapter):
        chapter.novel = chapter.novel_qu.novel
        chapter.save()

    def link_novel_novelqu(self, novelqu):
        try:
            novelqu.novel = Novel.objects.get(dir_name=novelqu.novel_title)
            novelqu.save()
        except ObjectDoesNotExist:
            novel = Novel(title=novelqu.novel_title.replace("_", " "))
            novel.save()
            BookInfo().getInfo(novel)
        except Exception as e:
            print(novelqu.novel_title)
            print(e)
            pass

    def fix_missing(self):
        novelqus = NovelQu.objects.filter(novel=None)
        print("\nextras novelqus", len(novelqus))
        self.atomic_chunks(novelqus, sqlfunction=self.link_novel_novelqu)

        chapters = (
            ChapterQUepubs.objects.filter(novel=None, folder="novel_quepubs/")
            .exclude(novel_qu=None)
            .exclude(novel_qu__novel=None)
        )
        print("extras chapters", len(chapters))
        self.atomic_chunks(chapters, sqlfunction=self.link_novel_chapter)
