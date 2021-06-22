from django.contrib import admin
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from .models import *


class FixedCountPaginator(Paginator):
    @property
    def count(self):
        return 1000


class NovelLinkedListFilter(admin.SimpleListFilter):
    title = _("Linked to Novel model")

    parameter_name = "linked"

    def lookups(self, request, model_admin):
        return (
            ("true", _("Linked")),
            ("false", _("Not Linked")),
        )

    def queryset(self, request, queryset):
        if self.value() == "true":
            return queryset.exclude(novel=None)
        if self.value() == "false":
            return queryset.filter(novel=None)


class ChapterTitleListFilter(admin.SimpleListFilter):
    title = _("Titled chapter")

    parameter_name = "titled"

    def lookups(self, request, model_admin):
        return (
            ("true", _("Titled")),
            ("false", _("Not Titled")),
        )

    def queryset(self, request, queryset):
        if self.value() == "true":
            return queryset.exclude(title="default")
        if self.value() == "false":
            return queryset.filter(title="default")


class ChapterQUepubsListFilter(admin.SimpleListFilter):
    title = _("QU epubs chapter")

    parameter_name = "QUepubs"

    def lookups(self, request, model_admin):
        return (
            ("true", _("QU epubs")),
            ("false", _("Not QU epubs")),
        )

    def queryset(self, request, queryset):
        if self.value() == "true":
            return queryset.filter(folder="novel_quepubs/")
        if self.value() == "false":
            return queryset.exclude(folder="novel_quepubs/")


class SerieAdmin(admin.ModelAdmin):
    list_display = ("number", "novel", "date_posted")
    search_fields = (
        "novel__title",
        "number",
    )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ("folder",)
    fieldsets = ()


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("number", "novel", "date_posted")
    search_fields = (
        "novel_title",
        "number",
    )
    readonly_fields = ()
    list_per_page = 100
    paginator = FixedCountPaginator
    show_full_result_count = False

    filter_horizontal = ()
    list_filter = (
        NovelLinkedListFilter,
        ChapterTitleListFilter,
        ChapterQUepubsListFilter,
        "folder",
    )
    fieldsets = ()


class NovelAdmin(admin.ModelAdmin):
    list_display = (
        "wid",
        "title",
        "original",
        "date_added",
    )
    search_fields = (
        "id",
        "wid",
        "title",
        "dir_name",
    )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ("original",)
    fieldsets = ()


class NovelQuAdmin(admin.ModelAdmin):
    list_display = ("novel_title", "novel", "date_posted")
    search_fields = ("novel_title", "novel__title")
    readonly_fields = ()

    raw_id_fields = ("novel",)
    filter_horizontal = ()
    list_filter = (NovelLinkedListFilter,)
    fieldsets = ()


admin.site.register(Novel, NovelAdmin)
admin.site.register(NovelQu, NovelQuAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
admin.site.register(ChapterV2, SerieAdmin)
admin.site.register(ChapterQUepubs, ChapterAdmin)
