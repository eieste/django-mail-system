import io
import smtplib
import uuid

from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.db import models

from mailsystem.models import MailLogSession
from mailsystem.utils.streams import RedirectStdStreams


class MailMessage:

    def __init__(self, email_message=None, maillog_session=None):
        self._email_message = email_message
        self._maillog_session = maillog_session

    def send(self):
        data = io.StringIO()
        with RedirectStdStreams(stdout=data, stderr=data):
            self._email_message.send()

        self._maillog_session.logparse(data.getvalue())

    def get_mail_session(self):
        return self._maillog_session


class MailLogger:

    def __init__(self, email_message=None, reference=None):
        assert isinstance(email_message, EmailMessage)
        self._reference = None

        if reference is not None:
            if isinstance(reference, models.Model):
                raise ValueError("Reference is not an Model")
            self._reference = reference

        self.orginal_debuglevel = smtplib.SMTP.debuglevel
        self._email_message = email_message

    def __enter__(self):
        smtplib.SMTP.debuglevel = 9

        self._email_message.extra_headers["mailsystem-reference-uuid"] = uuid.uuid4()
        maillog_session = MailLogSession.objects.create(recipient_email=self._email_message.to[0],
                                                        sender_email=self._email_message.from_email,
                                                        email=self._email_message.body,
                                                        uuid=self._email_message.extra_headers["mailsystem-reference-uuid"]
                                                       )
        if self._reference:
            contenttype = ContentType.objects.get_for_model(model=type(self._reference))
            maillog_session.content_type = contenttype
            maillog_session.reference = self._reference.pk
            maillog_session.save()


        return MailMessage(email_message=self._email_message, maillog_session=maillog_session)

    def __exit__(self, type, value, traceback):
        smtplib.SMTP.debuglevel = self.orginal_debuglevel
