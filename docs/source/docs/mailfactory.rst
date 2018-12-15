############
Mail Factory
############

MailFactory gives you a way to render multiple E-Mails with the same template.
You can define mail-templates with different variables

These templates can be used to create mails. These mails, which are created in this way can contain different subjects.
A mail is also described by a reason(string). If it is necessary to trigger a mail, the reason finds the event that triggers the e-mail sending action


MailTemplate & MailTemplateVariables
------------------------------------

Creates a html E-Mail template. Defines the  variables in this E-Mail template

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
You can create a MailTemplate with the following settings:

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


When this entrys are created you can use this template for any E-Mail.

Mail
----

Now it is possible to create mails. A "Mail" is the template for a specific reason to send a E-Mail
like:

- Registration E-Mail
- Password Forgotten E-Mail
- Welcome E-Mail
- ...

Create a Mail-Entry at the ``Home › Mailsystem › Mails › Add mail`` Admin Page
The subject field is the E-Mail subject.
Select the template created above.
you can create your own generator, or use the default generator

Reason is a slug field. This slug can be used as Identifire in the sourcecode.
The reason is also important for the MailFactory class.


Trigger
-------

Now you are ready to send E-Mails

.. code-block:: python

   from mailsystem.utils.factory import MailFactory, MailMeta

   # Create a MailMeta
   mailmeta = MailMeta(["user@example.de"])

    user = User.objects.get(pk=1)

   # Trigger the E-Mail transmission
   MailFactory.trigger(reason="send_bill", meta=mailmeta, reference=user)


