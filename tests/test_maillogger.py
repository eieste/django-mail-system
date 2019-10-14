import unittest
from mailsystem.utils.mail import MailLogger
from django.core.mail import EmailMessage
import smtplib


class MailloggerTestCase(unittest.TestCase):

    def test_smtplib_change(self):
        self.assertEqual(smtplib.SMTP.debuglevel, 0)
        with MailLogger(EmailMessage()):
            self.assertEqual(smtplib.SMTP.debuglevel, 9)
        self.assertEqual(smtplib.SMTP.debuglevel, 1)


if __name__ == '__main__':
    unittest.main()
