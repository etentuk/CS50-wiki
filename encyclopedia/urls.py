from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_results, name="search_results"),
    path("<str:title>", views.entry_page, name="entry_page"),
]
