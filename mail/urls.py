from django.urls import path
from django.views.generic import TemplateView
from .views import AddMailView, Outbox, MailView

urlpatterns = [
    path("", AddMailView.as_view(), name="schedule"),
    path("outbox/", Outbox.as_view(), name="outbox"),
    path("<int:pk>/", MailView.as_view(), name="mailview"),
]
