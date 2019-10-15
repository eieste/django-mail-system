import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext as _
import enum

class RecipientTypeChoices(enum.Enum):
    TO = "to"
    CC = "cc"
    BCC = "bcc"


class MailLogRecipient(models.Model):
    protocol = models.ForeignKey("MailLogSession", on_delete=models.CASCADE)
    recipient_type = models.CharField(max_length=3, choices=[ (item, item.value) for item in RecipientTypeChoices ])
    address = models.EmailField()


class MailLogSession(models.Model):
    """
        Log the E-Mail transmission
    """
    uuid = models.UUIDField(editable=False, help_text=_("E-Mail header Identificator"))
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    # recipient_email = models.EmailField(max_length=255, help_text=_("E-Mail Empfänger"))
    sender_email = models.EmailField(max_length=255, help_text=_("E-Mail Sender"))
    context = models.TextField(help_text=_("Context, used for E-Mail rendering"))
    email = models.TextField(help_text=_("Full E-Mail"))
    send_at = models.DateTimeField(auto_now=True, help_text=_("Send Timestamp"))

    def add_recipients(self, email_message):
        maillog_recipient_list = []
        for rec_type in [ item.value for item in RecipientTypeChoices ]:

            if hasattr(email_message, rec_type):
                for recipient_address in getattr(email_message, rec_type):
                    maillog_recipient_list.append(
                        MailLogRecipient(protocol=self, recipient_type=rec_type, address=recipient_address)
                    )

        MailLogRecipient.objects.bulk_create(maillog_recipient_list)


    def logparse(self, log):
        """
        Parse a E-Mail sendlog

        :param log: Log string
        :return:
        """
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

    def get_reference(self):
        """
        Resolve saved Reference

        :return Model: Any previously saved Database Object
        """
        model = self.content_type.model_class()
        return model.objects.get(pk=self.reference)

    @classmethod
    def find_by_reference(cls, obj):
        """
            finds the corresponding mail log using the reference
        :param obj: reference that was also specified during creation
        :return: Queryset with all possible matches
        """
        contenttype = ContentType.objects.get_for_model(model=type(obj))
        return MailLogSession.objects.filter(content_type=contenttype, reference=obj.pk)


class MailLogLine(models.Model):
    """
        Single line of transmission log. Linked with MailLogSession.
    """
    protocol = models.ForeignKey(MailLogSession, on_delete=models.CASCADE)
    timestamp = models.TimeField()
    type = models.CharField(max_length=255)
    payload = models.TextField()
    insert = models.DateTimeField(auto_now_add=True)


TEMPLATE_PATH = getattr(settings, "MAILSYSTEM_MAIL_TEMPLATE_PATH", "mailsystem/templates/mailsystem/")


class MailTemplate(models.Model):
    name = models.CharField(max_length=255)
    html_file = models.FilePathField(path=TEMPLATE_PATH, recursive=True, max_length=500)
    alternative_file = models.FilePathField(path=TEMPLATE_PATH, recursive=True, max_length=500)

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
    reason = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.subject


class MailVariable(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.DO_NOTHING)
    mail_template_variable = models.ForeignKey(MailTemplateVariable, on_delete=models.DO_NOTHING)
    content = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.mail_template_variable.name, self.mail)
