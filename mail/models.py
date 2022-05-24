from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
import os

schedule_choice = (("once", "Once"), ("weekly", "Weekly"), ("monthly", "Monthly"))


class ScheduledMail(models.Model):
    sender = models.EmailField(max_length=255)
    recipients_list = ArrayField(models.EmailField(max_length=255))
    subject = models.CharField(max_length=78)
    body = models.CharField(max_length=40000)
    send_on = models.DateTimeField(default=datetime.today, blank=False)
    status = models.CharField(max_length=32, blank=True)
    schedule_type = models.CharField(
        choices=schedule_choice, default="once", max_length=16
    )

    def get_absolute_url(self):
        return reverse("mail", args=(str(self.id),))

    def __str__(self):
        return self.subject

    class Meta:
        ordering = [
            "-id",
        ]
