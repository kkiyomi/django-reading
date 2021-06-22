from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
import os


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="", editable=False, max_length=200)

    def save(self, *args, **kwargs):
        if self.slug == "":
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Language(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="", editable=False, max_length=200)

    def save(self, *args, **kwargs):
        if self.slug == "":
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Status(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="", editable=False, max_length=200)

    def save(self, *args, **kwargs):
        if self.slug == "":
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Status, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Novel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="N/A")
    author = models.CharField(max_length=20, default="N/A")
    language = models.ForeignKey(
        Language, default=1, on_delete=models.SET_NULL, null=True
    )
    status = models.ForeignKey(Status, default=1, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=20, default="N/A")
    image = models.ImageField(
        default="default.jpg", upload_to="novel_pics", max_length=500
    )
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(default="", editable=False, max_length=200)
    date_added = models.DateTimeField(default=timezone.now)
    genres = models.ManyToManyField(Genre)
    uid = models.CharField(default="", editable=False, max_length=100)
    original = models.CharField(default="None", max_length=100)
    wid = models.CharField(default="None", max_length=100)

    dir_name = models.CharField(default="", max_length=200)

    def save(self, *args, **kwargs):

        if self.slug == "":
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        redict = {
            " ": "_",
            "'": "",
            ":": "",
            ",": "",
            "?": "",
            "!": "",
            "[": "",
            "]": "",
            "’": "",
        }
        if (
            self.dir_name == ""
            or set(redict.keys()).intersection(set(self.dir_name)) != set()
        ):
            self.dir_name = self.title
            for key, value in redict.items():
                self.dir_name = self.dir_name.replace(key, value)

        self.uid = uuid.uuid4().hex

        super(Novel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class NovelQu(models.Model):
    novel_title = models.CharField(max_length=500, default="default")
    novel = models.OneToOneField(
        Novel, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_posted = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        try:
            if self.novel_title != "default":
                novel = Novel.objects.filter(dir_name=self.novel_title)
                if len(novel) != 0:
                    self.novel = novel[0]
        except Exception as e:
            pass

        super(NovelQu, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.novel_title}"


class ChapterV2(models.Model):
    title = models.CharField(max_length=500)
    number = models.CharField(max_length=100)
    content_path = models.CharField(max_length=500, default="default")
    folder = models.CharField(max_length=500, default="novel_chapters")
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    in_other = models.CharField(max_length=100, default="default")

    def save(self, *args, **kwargs):
        root = "C:\\Users\\user\\Desktop\\python\\django_project\\media"
        path = f"\\novel_pics\\{slugify(self.novel.title)}.png"
        if self.novel.image != path and os.path.exists(root + path):
            self.novel.image = path
        elif not os.path.exists(root + path):
            self.novel.image = "default.jpg"

        self.novel.save()
        super(ChapterV2, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.novel.title}  - Chapter {self.number}"


class ChapterQUepubs(models.Model):
    novel_title = models.CharField(max_length=500, default="default")
    title = models.CharField(max_length=500, default="default")
    number = models.CharField(max_length=100)
    content_path = models.CharField(max_length=500, default="default")
    folder = models.CharField(max_length=500, default="novel_quepub/")
    date_posted = models.DateTimeField(default=timezone.now)

    novel = models.ForeignKey(Novel, on_delete=models.SET_NULL, blank=True, null=True)
    novel_qu = models.ForeignKey(
        NovelQu, on_delete=models.SET_NULL, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.novel_title == "default" and self.novel is not None:
            self.novel_title = self.novel.dir_name

        if self.novel_qu is None:
            self.novel_qu, _ = NovelQu.objects.get_or_create(
                novel_title=self.novel_title
            )

        super(ChapterQUepubs, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.novel_title}  - Chapter {self.number}"
