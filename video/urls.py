from django.urls import path
from . import views

app_name = "video"

urlpatterns = [
    path("", views.video_list, name="list"),
    path("<int:video_id>/", views.video_detail, name='detail'),
    path("search", views.video_search, name="search"),
]
