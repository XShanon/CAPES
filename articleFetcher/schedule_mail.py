from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags
from feeder.views import get_list
from mail.models import ScheduledMail

from pathlib import Path
import smtplib, ssl

from django.core.mail import send_mail
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(
    sender_email,
    reciever_email,
    password,
    message,
    port,
    searchterm,
    schedule_type,
    mail_obj,
):

    if schedule_type == "monthly" or schedule_type == "weekly":
        article_list = get_list(searchterm)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ",".join(reciever_email)
        message["Subject"] = subject

        BASE_DIR = Path(__file__).resolve().parent.parent
        html_message = loader.render_to_string(
            Path(BASE_DIR, "templates/mail/mail_template.html"),
            {"articles": article_list, "searchterm": searchterm},
        )
        text_content = strip_tags(html_message)
        body = MIMEText(article_list, "html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, list(reciever_email), message.as_string())

        obj = ScheduledMail.objects.get(pk=mail_obj.id)
        obj.status = "Sent"
        obj.save()


def schedule_mail(context, mail_obj):
    send_time = context["send_time"]
    port = context["port"]
    sender_email = context["from"]
    reciever_email = context["to"]
    password = context["user_pswd"]
    article_list = context["articles"]
    subject = context["subject"]
    searchterm = context["searchterm"]
    schedule_type = context["schedule_type"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ",".join(reciever_email)
    message["Subject"] = subject

    BASE_DIR = Path(__file__).resolve().parent.parent
    html_message = loader.render_to_string(
        Path(BASE_DIR, "templates/mail/mail_template.html"),
        {"articles": article_list},
    )
    text_content = strip_tags(html_message)
    body = MIMEText(article_list, "html")

    message.attach(body)
    from datetime import datetime
    from articleFetcher import schedule_mail
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.schedulers.background import BackgroundScheduler

    now_time = datetime.now().replace(tzinfo=None)
    difference = (send_time.replace(tzinfo=None) - now_time).total_seconds()
    if difference <= 0:
        send_mail(
            sender_email,
            reciever_email,
            password,
            message,
            port,
            searchterm,
            schedule_type,
            mail_obj,
        )
    else:
        if schedule_type == "once":
            scheduler = BlockingScheduler()
            scheduler.add_job(
                send_mail,
                "date",
                run_date=send_time,
                args=[
                    sender_email,
                    reciever_email,
                    password,
                    message,
                    port,
                    searchterm,
                    schedule_type,
                    mail_obj,
                ],
            )
        elif schedule_type == "weekly":
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                send_mail,
                "interval",
                weeks=1,
                args=[
                    sender_email,
                    reciever_email,
                    password,
                    message,
                    port,
                    searchterm,
                    schedule_type,
                    mail_obj,
                ],
            )

        elif schedule_type == "monthly":
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                send_mail,
                "interval",
                days=30,
                args=[
                    sender_email,
                    reciever_email,
                    password,
                    message,
                    port,
                    searchterm,
                    schedule_type,
                    mail_obj,
                ],
            )
        scheduler.start()
