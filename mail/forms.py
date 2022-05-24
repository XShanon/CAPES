from django import forms
from .models import ScheduledMail
from .datetimewidget import MinimalSplitDateTimeMultiWidget


class MailForm(forms.ModelForm):
    class Meta:
        model = ScheduledMail
        exclude = [
            "sender",
            "status",
        ]

        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "max-length": "70",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "max-length": "40000",
                }
            ),
            "recipients_list": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Comma Seperated email-ids",
                }
            ),
            "send_on": MinimalSplitDateTimeMultiWidget(),
        }
