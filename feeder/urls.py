from django.urls import path
from django.views.generic import TemplateView
from .views import home, fetchfeed, AddFeed

urlpatterns = [
    path("", home, name="home"),
    path("feed/", fetchfeed, name="fetchfeed"),
    path("create/", AddFeed.as_view(), name="createfeedlink"),
]
