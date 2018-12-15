#######
MailLog
#######

How to log the transmission of an outgoing E-Mail:


.. code-block:: python3

    from mailsystem.utils.mail import MailLogger
    from django.core.mail import EmailMultiAlternatives
    from django.contrib.auth.models import User


    user = User.objects.get(pk=1)

    mail = EmailMultiAlternatives(subject="Test-Email",
                                 from_email="foo@example.net",
                                 to=[user.email],
                                 body="This is an Test E-Mail")

    with MailLogger(email_message=mail, reference=user) as msg:
        msg.send()

        msg.