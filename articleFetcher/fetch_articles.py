from dateutil import parser
from feeder.models import FeedLink, Article
import feedparser
import ssl

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


def fetch_articles():

    feedlist = FeedLink.objects.values_list("rss_link", flat=True)
    for feed in feedlist:
        feed = feedparser.parse(feed)

        for item in feed.entries:
            if not Article.objects.filter(title=item.title).exists():
                tags = []
                description = ""
                if "description" in item:
                    description = item.description.lower()
                if "tags" in item:
                    for tag in item["tags"]:
                        if "term" in tag:
                            tags.append(tag["term"].lower())
                        else:
                            tags.append(tag.lower())
                article = Article(
                    title=item.title,
                    description=description,
                    link=item.link,
                    tags=tags,
                )
                article.save()
