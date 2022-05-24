from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from .models import ScheduledMail
from .forms import MailForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags
from articleFetcher import schedule_mail
from django.shortcuts import redirect

from pathlib import Path
from feeder.views import get_list
import smtplib, ssl

from django.core.mail import send_mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Outbox(LoginRequiredMixin, ListView):
    model = ScheduledMail
    template_name = "mail/outbox.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["mails"] = ScheduledMail.objects.filter(sender=self.request.user.email)
        return context


class MailView(LoginRequiredMixin, DetailView):
    model = ScheduledMail
    template_name = "mail/index.html"


class AddMailView(LoginRequiredMixin, CreateView):
    model = ScheduledMail
    form_class = MailForm
    success_url = "/"
    template_name = "mail/add.html"

    def get_initial(self):
        article_list = self.request.session.get("articles")
        searchterm = self.request.session.get("searchterm")
        BASE_DIR = Path(__file__).resolve().parent.parent
        html_message = loader.render_to_string(
            Path(BASE_DIR, "templates/mail/mail_template.html"),
            {"articles": article_list, "searchterm": searchterm},
        )
        return {"body": html_message}

    def form_valid(self, form):
        form.instance.sender = self.request.user.email
        obj = form.save()
        article_list = self.request.session.get("articles")
        context = {}
        context["from"] = self.request.user.email
        context["to"] = form.instance.recipients_list
        context["subject"] = form.instance.subject
        context["user_pswd"] = self.request.user.gapps_key
        context["port"] = 465
        context["send_time"] = form.instance.send_on
        context["articles"] = form.instance.body
        context["searchterm"] = self.request.session.get("searchterm")
        context["schedule_type"] = form.instance.schedule_type
        from articleFetcher import schedule_mail

        mailobj = ScheduledMail.objects.get(pk=obj.id)
        mailobj.status = "Scheduled"
        mailobj.save()
        schedule_mail.schedule_mail(context, obj)
        return redirect("home")

        """
        BASE_DIR = Path(__file__).resolve().parent.parent
        html_message = loader.render_to_string(
            Path(BASE_DIR, "templates/mail/mail_template.html"),
            {"articles": article_list},
        )
        text_content = strip_tags(html_message)
        body = MIMEText(body, "html")

        message.attach(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(message["From"], message["To"], message.as_string())
        """
