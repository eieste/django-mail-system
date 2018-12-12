from django.db import models
import re
from django.utils.timezone import datetime


class MailLogSession(models.Model):
    uuid = models.UUIDField(editable=False)
    recipient_email = models.EmailField(max_length=255)
    sender_email = models.EmailField(max_length=255)
    context = models.TextField()
    email = models.TextField()
    send_at = models.DateTimeField(auto_now=True)

    def logparse(self, log):
        line_regex = re.compile(r'(?P<timestamp>[\d+\:]{5,10}\.\d+)\s(?P<linetype>\w+)\:\s(?P<payload>.*)', re.MULTILINE)
        entry_list = []

        for match in line_regex.finditer(log):
            timestamp, linetype, payload= match.groups()
            time = datetime.strptime(timestamp, "%H:%M:%S.%f")
            if not (payload == "" and linetype == ""):

                if type(linetype) is bytes:
                    linetype = linetype.decode("ascii")

                if type(payload) is bytes:
                    payload = payload.decode("ascii")

                entry = MailLogLine(protocol=self, type=linetype, payload=payload, timestamp=time)
                entry_list.append(entry)

            MailLogLine.objects.bulk_create(entry_list)


class MailLogLine(models.Model):
    protocol = models.ForeignKey(MailLogSession, on_delete=models.CASCADE)
    timestamp = models.TimeField()
    type = models.CharField(max_length=255)
    payload = models.TextField()
    insert = models.DateTimeField(auto_now_add=True)


class MailTemplate(models.Model):
    name = models.CharField(max_length=255)
    html_file = models.FilePathField(recursive=True, max_length=500)
    alternative_file = models.FilePathField(recursive=True, max_length=500)

    def __str__(self):
        return self.name


class MailTemplateVariable(models.Model):
    template = models.ForeignKey(MailTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Variablen Name")
    default = models.TextField(default="Undefined Value")

    def __str__(self):
        return self.name


class Mail(models.Model):
    subject = models.CharField(max_length=255, help_text=_("E-Mail Betreff"))
    template = models.ForeignKey(MailTemplate, on_delete=models.DO_NOTHING)
    generator = models.CharField(max_length=255, default="notification.generator.generic.BasicGenerator")

    def __str__(self):
        return { self.subject }


class MailVariable(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.DO_NOTHING)
    mail_template = models.ForeignKey(MailTemplate, on_delete=models.DO_NOTHING)
    content = models.TextField()

    def __str__(self):
        return f"{self.mail_template.name} - {self.mail}"
