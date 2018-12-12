[![Build Status](https://travis-ci.org/eieste/django-mail-system.svg?branch=master)](https://travis-ci.org/eieste/django-mail-system)

# django-mail-system

Creates a full log of Outgoing E-Mails

## Install

pip3 install django-mail-system

## Usage

Add app to settings.py

```
INSTALLED_APPS = [
    ...,
    maillog,
]
```

In the code:

```
from maillog.utils.mail import MailLogger

from django.core.mail import EmailMultiAlternatives

def sendit():

    mail = EmailMultiAlternatives(subject="Test-Email",
                                 from_email="foo@example.net",
                                 to=["name@example.com"],
                                 body="This is an Test E-Mail")

    with MailLogger(mail) as msg:
        msg.send()
```