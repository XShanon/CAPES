from django.db import models
from django.contrib.postgres.fields import ArrayField

class FeedLink(models.Model):
    rss_link = models.URLField(unique=True)

class Article(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField()
    link = models.URLField(max_length=1024)
    tags = ArrayField(models.CharField(max_length=128))
    #tags = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"{self.title}"

