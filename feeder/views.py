from django.views.generic import ListView, CreateView
from django.shortcuts import render
from django.core.management import call_command
import feedparser
from django.forms.models import model_to_dict
from .models import FeedLink, Article
from .forms import AddFeedForm
from io import StringIO
import json
import itertools


def get_list(searchterm):
    context = {}
    context["articles"] = []
    articles_list = Article.objects.values()

    for article in articles_list:
        if (
            searchterm in article["title"].lower()
            or searchterm in article["description"].lower()
        ):
            context["articles"].append(article)
        for tag in article["tags"]:
            if searchterm in tag:
                context["articles"].append(article)

    posts = len(context["articles"])

    context["articles"] = [a[0] for a in itertools.groupby(context["articles"])]
    return context["articles"][:15]


def home(request):
    return render(request, "base.html")


def fetchfeed(request):
    searchterm = request.POST.get("searchterm")
    if not searchterm:
        searchterm = "news"
    context = {"articles": get_list(searchterm)}
    request.session["articles"] = context["articles"]
    request.session["searchterm"] = searchterm
    return render(
        request,
        "fetch.html",
        {"articles": context["articles"][:15], "searchterm": searchterm},
    )


class AddFeed(CreateView):
    model = FeedLink
    form_class = AddFeedForm
    success_url = "/"
