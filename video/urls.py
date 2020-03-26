from django.urls import path
from . import views

app_name = "video"

urlpatterns = [
    path("", views.video_list, name="list"),
    path("<str:video_key>/<str:start>", views.video_detail, name='detail'),
    path("search", views.video_search, name="search"),
]
