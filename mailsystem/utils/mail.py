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
        """Alternative EmailMessage OBject
        :param email_message: Orginal EmailMessage or EmailAlternativeMessage
        :param maillog_session: MailLogSession object
        """
        self._email_message = email_message
        self._maillog_session = maillog_session

    def send(self):
        """
            Trigger send method of the orginal EmailMessage Object
            :return:
        """
        data = io.StringIO()
        with RedirectStdStreams(stdout=data, stderr=data):
            self._email_message.send()

        self._maillog_session.logparse(data.getvalue())

    def get_mail_session(self):
        return self._maillog_session


class MailLogger:

    def __init__(self, email_message=None, reference=None):
        """
            create a detailed E-Mail sendlog

            :param email_message: Django EmailMessage Object to send
            :param reference: (optional) Reference for this EMailMessage (eg. Customer databases entry) must be a django Model object
        """
        # Test if email_message is the django EmailMessage object
        assert isinstance(email_message, EmailMessage)
        self._reference = None

        if reference is not None:
            if not isinstance(reference, models.Model):
                raise ValueError("Reference is not an Model")
            self._reference = reference

        self.orginal_debuglevel = smtplib.SMTP.debuglevel
        self._email_message = email_message

    def __enter__(self):
        # Change smtplib debuglevel
        smtplib.SMTP.debuglevel = 9

        # Create an UUID for E-Mail Header
        self._email_message.extra_headers["mailsystem-reference-uuid"] = uuid.uuid4()

        # Create MailLogSession enry
        maillog_session = MailLogSession.objects.create(sender_email=self._email_message.from_email,
                                                        email=self._email_message.body,
                                                        uuid=self._email_message.extra_headers["mailsystem-reference-uuid"]
                                                       )

        maillog_session.add_recipients(self._email_message)



        # Resolve reference o content_type if exists
        if self._reference:
            contenttype = ContentType.objects.get_for_model(model=type(self._reference))
            maillog_session.content_type = contenttype
            maillog_session.reference = self._reference.pk
            maillog_session.save()

        # Return a Represententing Object
        return MailMessage(email_message=self._email_message, maillog_session=maillog_session)

    def __exit__(self, type, value, traceback):
        # Reset smtplib debuglevel to orginal Level
        smtplib.SMTP.debuglevel = self.orginal_debuglevel
