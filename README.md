[![Build Status](https://travis-ci.org/eieste/django-mail-system.svg?branch=staging)](https://travis-ci.org/eieste/django-mail-system)
[![Documentation Status](https://readthedocs.org/projects/django-mail-system/badge/?version=staging)](https://django-mail-system.readthedocs.io/en/staging/?badge=staging)

 
# django-mail-system

A useful library to create E-Mail templates und log E-Mail transmissions


You can define Templates and Variables for this Templates.
It can be used to send E-Mails.
The whole process is very simple. 

Example:

You have a WebService and you would like to send bill mails to all users every first day of a month, you can do it with the following code:


```
from mailsystem.utils.factory import MailFactory
import datetime

if datetime.now().day == 1:
    for user in User.objects.filter(active=True):
        MailFactory.trigger(reason="billmail", reference=user)
    
```


## Install
```
pip3 install django-mail-system
```
## Usage

Add app to settings.py

```
INSTALLED_APPS = [
    ...,
    mailsystem,
]
```

## Documentation

[Read the Docs](https://django-mail-system.readthedocs.io/)
