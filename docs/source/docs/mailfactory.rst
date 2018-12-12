############
Mail Factory
############

MailFactory gives you a way to Render multiple E-Mails with the same Template.
You can define Mail-Templates with Variables

This Templates can be used to create Mails. This Mails contains the subject.
A mail had also a Reason(string). Reason describes the event that triggers the E-Mail Send Action


MailTemplate & MailTemplateVariables
------------------------------------

Create an html E-Mail Template. Define Variables in this E-Mail Template

.. code-block:: HTML

    <html>
        <head>
        </head>
        <body>
            <table>
                <tr>
                    <td>
                        {{ greeting }}
                    </td>
                </tr>
                <tr>
                    <td>
                        {{ content }}
                    </td>
                </tr>
                <tr>
                    <td>
                        {{ signature }}
                    </td>
                </tr>
            </table>
        </body>
    </html>

Register this Template in Database. You can use the ``Home › Mailsystem › Mail templates`` Adminpage
You can create an MailTemplate with the following settings:

**Add mail template**
- **Name:** Default Template
- **Html file:** Select the html E-Mail Template
- **Alternative file:**

Alternative file can be used as Template for E-Mail Text message.
This two files should be have the Same Variables

**MAIL TEMPLATE VARIABLES**
 - | **name:** greeting
   | **default:** hi
 - | **name:** content
   | **default:** No Text
 - | **name:** signature
   | **default:** Sincerely


When this entrys are created you can use this Template for any E-Mail.

Mail
----

Now it's possible to Create Mails. A "Mail" is the template for a specific Reason to send an E-Mail
like:

- Registration E-Mail
- Password Forgotten E-Mail
- Welcome E-Mail
- ...

Create an Mail-Entry at the ``Home › Mailsystem › Mails › Add mail`` Admin Page
The Subject field is the E-Mail Subject.
Select the template created above.
you can create your own generator, or use the Default generator

Reason is a slug field. This slug can be used as Identifire in the sourcecode.
The Reason is also importent for the MailFactory class.


Trigger
-------

Now you are ready to send E-Mails

.. code-block:: python

   from mailsystem.utils.factory import MailFactory, MailMeta

   a = MailMeta(["user@example.de"])

   MailFactory.trigger(reason="blubbern", meta=a, reference={"name":"foo"})
   MailFactory.trigger(reason="blubbern", meta=a, reference={"name":"foo"})


