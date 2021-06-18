import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("debug/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
