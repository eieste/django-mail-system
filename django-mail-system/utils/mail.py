import io
import sys
import uuid
import smtplib
from maillog.models import MailSession
from maillog.utils.streams import RedirectStdStreams
from django.core.mail import send_mail


class MailMessage:

    def __init__(self, mail, maillog):
        self.mail = mail
        self.maillog = maillog

    def send(self):
        data = io.StringIO()
        with RedirectStdStreams(stdout=data, stderr=data):
            self.mail.send()

        self.maillog.logparse(data.getvalue())


class MailLogger:

    def __init__(self, mail):
        self.orginal_debuglevel = smtplib.SMTP.debuglevel
        self.mail = mail

    def __enter__(self):
        smtplib.SMTP.debuglevel = 9

        self.mail.extra_headers["maillog-reference"] = uuid.uuid4()
        maillog = MailSession.objects.create(recipient_email=self.mail.to[0],
                                             sender_email=self.mail.from_email,
                                             email=self.mail.body,
                                             uuid=self.mail.extra_headers["maillog-reference"]
                                             )
        return MailMessage(self.mail, maillog)

    def __exit__(self, type, value, traceback):
        smtplib.SMTP.debuglevel = self.orginal_debuglevel
