from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_results, name="search_results"),
    path('create_page', views.create_page, name="create_page"),
    path('edit/<str:title>', views.edit_page, name="edit_page"),
    path("<str:title>", views.entry_page, name="entry_page"),
]
