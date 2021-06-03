from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.NovelHomeListView.as_view(), name='novels_home'),
    path('home2/', views.NovelReadingListView.as_view(), name='novels_home2'),
    path('reading-list/', views.NovelReadingListView3.as_view(), name='reading_list'),

    path('novel/<slug:slug>/', views.NovelDetailView.as_view(), name='novel_detail'),
    path('novel/<slug:slug>/<str:chapter_number>', views.ChapterDetailView.as_view(), name='novel_chapter'),

    path('genre/<slug:slug>/', views.genre, name='novel_genre'),
    path('language/<slug:slug>/', views.LanguageListView.as_view(), name='novel_language'),
    path('status/<slug:slug>/', views.StatusListView.as_view(), name='novel_status'),
    
    path('search/', views.search, name='novel_search'),
    path('accounts/profile/', views.NovelReadingListView.as_view(), name='profile'),
    path('new/', views.NovelNewListView.as_view(), name='novel_new'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
