from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", NovelHomeListView.as_view(), name="novels_home"),
    path("reading-list/", NovelReadingListView3.as_view(), name="reading_list"),
    path("novel/<slug:slug>/", NovelDetailView.as_view(), name="novel_detail"),
    path(
        "novel/<slug:slug>/<str:chapter_number>",
        ChapterDetailView.as_view(),
        name="novel_chapter",
    ),
    path("genre/<slug:slug>/", genre, name="novel_genre"),
    path("language/<slug:slug>/", LanguageListView.as_view(), name="novel_language"),
    path("status/<slug:slug>/", StatusListView.as_view(), name="novel_status"),
    path("search/", search, name="novel_search"),
    path("accounts/profile/", NovelReadingListView.as_view(), name="profile"),
    path("new/", NovelNewListView.as_view(), name="novel_new"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
