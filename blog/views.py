from django.shortcuts import render
from django.db.models import Max, F, Count
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from django.db import transaction

from .models import *

from itertools import zip_longest
from random import randint
from requests_html import HTML

import os
import markdown2
import tomd


def pairwise(iterable, n=2):
    a = iter(iterable)
    return zip_longest(*[a for i in range(n)], fillvalue=None)


def get_prev_next(obj, qset):
    assert obj in qset
    qset = list(qset)
    obj_index = qset.index(obj)
    try:
        prev_ch = qset[obj_index - 1]
        if obj_index == 0:
            prev_ch = None
    except IndexError:
        prev_ch = None
    try:
        next_ch = qset[obj_index + 1]
    except IndexError:
        next_ch = None
    return prev_ch, next_ch


class NovelNewListView(ListView):
    model = Novel
    template_name = "blog/home2.html"
    paginate_by = 30
    paginate_orphans = 3

    def get_queryset(self):
        return (
            Novel.objects.exclude(original="None")
            .filter(original="False")
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["novels"] = pairwise(context["page_obj"])
        return context


class NovelReadingListView(ListView):
    model = Novel
    template_name = "blog/home.html"
    paginate_by = 60
    paginate_orphans = 3

    def get_queryset(self):
        path = "C:\\Users\\user\\Desktop\\python\\django_project\\my_reading_list.txt"
        with open(path, "r", encoding="utf-8") as f:
            lists = f.readlines()
        novels = [novel.strip() for novel in lists]
        from django.db.models import Case, When

        preserved = Case(*[When(title=pk, then=pos) for pos, pk in enumerate(novels)])
        queryset = (
            Novel.objects.exclude(original="None")
            .filter(title__in=novels)
            .order_by(preserved)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = "Reading list"
        context["page_title"] = "Reading list"
        context["chapters_model"] = ChapterQUepubs.objects
        context["special"] = True
        return context


class NovelHomeListView(ListView):
    model = Novel
    template_name = "blog/home.html"
    paginate_by = 5 * 2
    paginate_orphans = 4

    def get_queryset(self):
        queryset = (
            Novel.objects.exclude(original="None")
            .annotate(Max("chapterquepubs__date_posted"))
            .order_by("-chapterquepubs__date_posted__max")
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today_date"] = timezone.now
        context["chapters_model"] = ChapterQUepubs.objects
        context["special"] = True
        return context


class NovelReadingListView3(ListView):
    model = Novel
    template_name = "blog/home.html"
    paginate_by = 15 * 2
    paginate_orphans = 4

    def get_queryset(self):
        path = "C:\\Users\\user\\Desktop\\python\\django_project\\my_reading_list.txt"
        with open(path, "r", encoding="utf-8") as f:
            lists = f.readlines()
        novels = [novel.strip() for novel in lists]
        from django.db.models import Case, When

        preserved = Case(*[When(title=pk, then=pos) for pos, pk in enumerate(novels)])
        queryset = (
            Novel.objects.exclude(original="None")
            .filter(title__in=novels)
            .order_by(preserved)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["special"] = True
        context["chapters_model"] = ChapterQUepubs.objects
        return context


class NovelDetailView(DetailView):
    model = Novel
    template_name = "blog/novel.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        slug = self.kwargs["slug"]

        try:
            queryset = queryset.filter(slug=slug)
        except ObjectDoesNotExist:
            queryset = queryset.filter(uid=slug)

        if randint(0, 5) == 2:
            queryset.update(views=F("views") + 6)

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs["slug"]

        try:
            obj = queryset.get(slug=slug)
        except MultipleObjectsReturned:
            for item in queryset.filter(slug=slug).filter(wid="None"):
                item.delete()
            obj = queryset.get(slug=slug)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset_qu = (
            context["object"]
            .chapterquepubs_set.all()
            .extra(select={"myinteger": "CAST(number AS INTEGER)"})
            .order_by("-myinteger")
        )
        queryset_v2 = (
            context["object"]
            .chapterv2_set.all()
            .extra(select={"myinteger": "CAST(number AS INTEGER)"})
            .order_by("-myinteger")
        )

        context["querysets"] = [queryset_qu, queryset_v2]
        context["page_title"] = f"{context['object'].title}"
        return context


class StatusListView(ListView):
    model = Novel
    template_name = "blog/home2.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.kwargs.get("slug"):
            queryset = queryset.filter(status__slug=self.kwargs["slug"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["novels"] = pairwise(context["page_obj"])
        return context


def get_from_epub(chapter):

    filename = chapter.content_path
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    changes = {
        '<p><a epub:type="noteref" href="#n1"></a></p>': "",
        '<p><a epub:type="noteref" href="#n2"></a></p>': "",
        '<p><a epub:type="noteref" href="#n3"></a></p>': "",
        '<p><a epub:type="noteref" href="#n4"></a></p>': "",
        '<p><a epub:type="noteref" href="#n5"></a></p>': "",
        "\n": "",
    }

    if chapter.novel.title == "Closed Beta That Only I Played":
        newchanges = {
            '""': '"</p><p>"',
            '" "': '"</p><p>"',
            '. "': '.</p><p>"',
            '! "': '!</p><p>"',
            '? "': '?</p><p>"',
            ". ": "." + "</p><p>",
            '."': '."' + "</p><p>",
            '?"': '?"' + "</p><p>",
            '!"': '!"' + "</p><p>",
            "]": "]" + "</p><p>",
        }
        changes.update(newchanges)

    for key, value in changes.items():
        text = text.replace(key, value)

    title = HTML(html=text).find("h1", first=True)
    html = HTML(html=text.replace(str(title.html), "")).find("body", first=True)

    if chapter.title == "default":
        chapter.title = title.text
        chapter.save()

    content = html.html.replace(str(title.html), "")

    return content


def treat_text(chapter):

    if chapter.folder == "novel_quepubs/":
        text = get_from_epub(chapter)
        return text

    filename = f"{os.getcwd()}\\{chapter.content_path}"
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    tttt = text

    text = text.replace("<em> ", " <em>").replace(" </em>", "</em> ")
    text = text.replace("<em>", "<i>").replace("</em>", "</i>")
    text = text.replace(chapter.title, "").replace("\n", "")
    text = text.replace("<hr />", "<p>" + "=" * 30 + "</p>")
    text = text.replace("<pirate>", "<pirate hidden>")

    if chapter.folder == "novel_api":
        return text

    # if context['novel'].title == 'The Rise Of A Porter':
    #     text = text.replace('<', '&lt;').replace('>', '&gt;')
    #     text = text.replace('&lt;p&gt;', '<p>').replace('&lt;/p&gt;', '</p>')
    #     text = text.replace('&lt;h3 ', '<h3 ').replace('"buy" &gt;', '"buy" >')
    #     text = text.replace('&lt;/h3&gt;', '</h3>')

    if chapter.folder == "novel_old":
        rr = f"""<h2 class="text-center">{chapter.title}</h2>"""
        tttt = tttt.replace(rr, "")
        tttt = tttt.replace("<br/><br/>", "")

        html = HTML(html=tttt).find("div>div", first=True)
        text = html.html

    return text.replace("<p> </p>", "")


class ChapterDetailView(DetailView):
    model = ChapterQUepubs
    template_name = "blog/chapter.html"

    def get_object(self):

        slug = self.kwargs.get("slug")
        chapter_number = self.kwargs.get("chapter_number")

        if self.queryset is None:
            queryset = self.get_queryset()

        obj = queryset.get(novel__slug=slug, number=chapter_number)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["novel"] = context["object"].novel

        context["chapter"] = context["object"]

        queryset_qu = (
            ChapterQUepubs.objects.filter(novel=context["object"].novel_id)
            .extra(select={"myinteger": "CAST(number AS INTEGER)"})
            .order_by("-myinteger")
        )

        print(context)
        context["querysets"] = queryset_qu

        context["content"] = treat_text(context["chapter"])

        context["page_title"] = f"{context['novel'].title} - {context['chapter'].title}"

        return context


def genre(request, slug):
    novels = pairwise(
        Genre.objects.get(slug=slug)
        .novel_set.all()
        .annotate(Max("chapter__date_posted"))
        .order_by("-chapter__date_posted__max")
    )

    paginator = Paginator(list(novels), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "subtitle": f"{Genre.objects.get(slug=slug).name}",
    }
    return render(request, "blog/home.html", context)


class LanguageListView(ListView):
    model = Novel
    template_name = "blog/home.html"
    paginate_by = 15
    paginate_orphans = 4

    def get_queryset(self):
        queryset = self.model.objects.all()
        slug = self.kwargs["slug"]
        queryset = queryset.filter(language__name=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["novels"] = pairwise(context["page_obj"])
        context["today_date"] = timezone.now
        return context


def search(request):
    results = True
    query = request.GET.get("s")
    novels = ""
    if query:
        novels = Novel.objects.exclude(original="None").filter(
            title__icontains=query.strip()
        )
    paginator = Paginator(list(novels), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "novels": novels,
        "results": results,
        "title": f'Search Results for "{query}"',
    }
    return render(request, "blog/search.html", context)
